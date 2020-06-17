from django.db import models
from django.db.models import QuerySet

from memesbd.consts_db import *


class PostQuerySet(models.QuerySet):
    def uploaded_by(self, author_id: int) -> QuerySet:
        return self.filter(author_id=author_id)

    def moderated_by(self, moderator_id: int) -> QuerySet:
        return self.filter(moderator_id=moderator_id)

    def created_from(self, template_id: int) -> QuerySet:
        return self.filter(template_id=template_id)

    def related_with(self, post_id: int) -> QuerySet:
        """TODO: optimize"""
        template_id = self.get(id=post_id).template_id
        if template_id is None:
            return self.filter(template_id=post_id)
        else:
            return self.filter(template_id=template_id).exclude(id=post_id)

    def approved_by(self, moderator_id: int) -> QuerySet:
        return self.filter().filter(moderator_id=moderator_id)

    def rejected_by(self, moderator_id: int) -> QuerySet:
        return self.filter(moderator_id=moderator_id)


class PostManager(models.Manager):
    def __init__(self, approval_status=None, *args, **kwargs):
        self.approval_status = approval_status
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        qs = PostQuerySet(model=self.model, using=self._db)
        if self.approval_status is not None:
            qs = qs.filter(approval_status=self.approval_status)
        return qs

    @classmethod
    def factory(cls, model, approval_status=None):
        manager = cls(approval_status)
        manager.model = model
        return manager




class PendingPostManager(models.Manager):
    def get_queryset(self):
