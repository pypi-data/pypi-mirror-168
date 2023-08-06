# -*- coding: UTF-8 -*-
# Copyright 2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import os
import time
import json
import pickle
import asyncio
import schedule
from pathlib import Path

from django.conf import settings
from django.utils import timezone
from django.core.exceptions import SynchronousOnlyOperation
from channels.db import database_sync_to_async


try:
    from pywebpush import webpush, WebPushException
except ImportError:
    webpush = None

from channels.consumer import AsyncConsumer

import logging
import socketserver
import struct

d_logger = logging.getLogger('linod')
logger = logging.getLogger(__name__)
logger.propagate = True

class LogReceiver(asyncio.BufferedProtocol):
    # Tailored from: https://gist.github.com/1st1/1c606e5b83ef0e9c41faf21564d75ad7
    def connection_made(self, transport) -> None:
        self.transport = transport
        self._msg_size = None
        self._new_buffer(4)

    def _new_buffer(self, size):
        self.buffer = bytearray(size)
        self.pos = 0

    def get_buffer(self, sizehint: int) -> bytearray:
        return self.buffer

    def buffer_updated(self, nbytes: int) -> None:
        self.pos += nbytes

        if self._msg_size is None:
            if self.pos == 4:
                self._msg_size = struct.unpack('>L', self.buffer)[0]
                self._new_buffer(self._msg_size)
        else:
            if int(self.pos) == int(self._msg_size):
                msg = self.buffer
                self._new_buffer(4)
                self._msg_size = None

                self.message_received(msg)

    def message_received(self, data: bytes) -> None:
        data = pickle.loads(data)
        record = logging.makeLogRecord(data)
        d_logger.handle(record)
        self.transport.close()

class LinodConsumer(AsyncConsumer):

    async def log_server(self, event=None):
        asyncio.ensure_future(self.async_log_server())

    async def async_log_server(self):
        loop = asyncio.get_running_loop()
        server = await loop.create_unix_server(lambda : LogReceiver(), self.get_log_sock())
        async with server:
            await server.serve_forever()

    def get_log_sock(self):
        log_sock = str(Path(settings.SITE.project_dir) / 'log_sock')
        try:
            os.unlink(log_sock)
        except OSError:
            pass
        return log_sock

    async def send_push(self, event):
        # logger.info("Push to %s : %s", user or "everyone", data)
        data = event['data']
        user = event['user_id']
        if user is not None:
            user = settings.SITE.models.users.User.objects.get(pk=user)
        kwargs = dict(
            data=json.dumps(data),
            vapid_private_key=settings.SITE.plugins.notify.vapid_private_key,
            vapid_claims={
                'sub': "mailto:{}".format(settings.SITE.plugins.notify.vapid_admin_email)
            }
        )
        if user is None:
            subs = settings.SITE.models.notify.Subscription.objects.all()
        else:
            subs = settings.SITE.models.notify.Subscription.objects.filter(user=user)
        for sub in subs:
            sub_info = {
                'endpoint': sub.endpoint,
                'keys': {
                    'p256dh': sub.p256dh,
                    'auth': sub.auth,
                },
            }
            try:
                req = webpush(subscription_info=sub_info, **kwargs)
            except WebPushException as e:
                if e.response.status_code == 410:
                    sub.delete()
                else:
                    raise e

    async def run_schedule(self, event=None):
        asyncio.ensure_future(self._run_schedule())

    async def _run_schedule(self):
        logger.info("Running schedule")
        n = len(schedule.jobs)
        if n == 0:
            logger.info("This site has no scheduled jobs.")
            return
        logger.info(f"{n} scheduled jobs:")
        for i, job in enumerate(schedule.jobs, 1):
            logger.info(f"[{i}] {repr(job)}")
        s = 0
        while True:
            await database_sync_to_async(schedule.run_pending)()
            await asyncio.sleep(1)