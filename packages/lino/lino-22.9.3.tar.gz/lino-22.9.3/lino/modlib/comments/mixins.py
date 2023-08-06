# -*- coding: UTF-8 -*-
# Copyright 2015-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models
from django.db.models import Q

from lino.api import dd, rt, _

from .roles import PrivateCommentsReader

class Commentable(dd.Model):
    class Meta(object):
        abstract = True

    create_comment_template = _("Created a new {model}.")

    def on_commented(self, comment, ar, cw):
        pass

    def get_rfc_description(self, ar):
        return ''

    def get_comment_group(self):
        return None

    # def get_create_comment(self, ar):
    #     return None

    # write_comment_on_create = False

    def save_new_instance(self, ar):
        super().save_new_instance(ar)
        if rt.settings.SITE.loading_from_dump or not dd.is_installed('comments'):
            return

        if self.create_comment_template is not None:
            txt = self.create_comment_template.format(
                model=self.__class__._meta.verbose_name)
            # txt = self.get_create_comment(ar)
            comment = rt.models.comments.Comment(body=txt, owner=self)
            comment.on_create(ar)
            comment.full_clean()
            comment.save_new_instance(ar)
            # print("20220916 save_new_instance() created", comment, txt)

    @classmethod
    def get_comments_filter(cls, user):
        if user.user_type.has_required_roles([PrivateCommentsReader]):
            return None
        if user.is_anonymous:
            return Q(private=False)
        return Q(private=False) | Q(user=user)

    def is_comment_private(self, comment, ar):
        """Whether the given comment should be private."""
        return dd.plugins.comments.private_default
