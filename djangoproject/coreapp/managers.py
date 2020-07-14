from django.db import models, transaction
from django.db.models import QuerySet, Count, Case, When

from coreapp.consts_db import *


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

    def with_reacts_count(self):
        return self.annotate(react_count=Count(Case(When(postreact__react=0, then=0), default=1)))

    def with_comments_count(self):
        return self.annotate(comment_count=Count('postcomment'))

    def approved_only(self):
        return self.filter(approval_status=ApprovalStatus.APPROVED)


class PostManager(models.Manager):
    def __init__(self, approval_status=None, *args, **kwargs):
        self.approval_status = approval_status
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        qs = PostQuerySet(model=self.model, using=self._db)
        if self.approval_status is not None:
            qs = qs.filter(approval_status=self.approval_status)
        return qs

    def get_related_posts(self, post_id: int) -> QuerySet:
        return self.get_queryset().related_with(post_id)

    @classmethod
    def factory(cls, model, approval_status=None):
        manager = cls(approval_status)
        manager.model = model
        return manager

    @transaction.atomic
    def create(self, **kwargs):
        """
        Overwritten to maintain nested template reference concept
        """
        template_id = kwargs.pop('template_id', None)
        template = kwargs.pop('template', None)
        keywords = kwargs.pop('keywords', [])

        if template is not None:
            template_id = template.id if template.template_id is None else template.template_id
        elif template_id is not None:
            template = self.get_queryset().get(id=template_id)
            template_id = template.id if template.template_id is None else template.template_id
        obj = super().create(**kwargs, template_id=template_id)
        if keywords:
            obj.keywords.set(keywords)
        return obj


class PostReactQuerySet(models.QuerySet):
    def like(self):
        return self.filter(react=Reacts.LIKE)

    def love(self):
        return self.filter(react=Reacts.LOVE)

    def haha(self):
        return self.filter(react=Reacts.HAHA)

    def angry(self):
        return self.filter(react=Reacts.ANGRY)

    def sad(self):
        return self.filter(react=Reacts.SAD)

    def unreacted(self):
        return self.filter(react=Reacts.NONE)

    def of_user(self, user_id):
        return self.filter(user_id=user_id)

    def of_post(self, post_id):
        return self.filter(post_id=post_id)

    def without_removed_reacts(self):
        return self.exclude(react=Reacts.NONE)

    def react_counts(self):
        return self.values('react').annotate(count=Count('user'))

    def of_approved_posts(self):
        return self.filter(post__approval_status=ApprovalStatus.APPROVED)


class PostReactManager(models.Manager):
    """create is modified to support update or create by default"""
    def __init__(self, post_id=None, *args, **kwargs):
        self.post_id = post_id
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        qs = PostReactQuerySet(model=self.model, using=self._db)
        if self.post_id is not None:
            qs = qs.filter(post_id=self.post_id)
        return qs

    @classmethod
    def factory(cls, model, post_id=None):
        manager = cls(post_id)
        manager.model = model
        return manager

    def reacts_count_map(self, post_id: int) -> dict:
        """
        :returns a dict with as ({'WOW': 1})
        """
        rset = {}
        for q in self.get_queryset().of_post(post_id).without_removed_reacts().react_counts().values_list('react',
                                                                                                          'count'):
            rset[Reacts(q[0]).label] = q[1]
        return rset

    def react_user(self, post_id: int, user_id: int) -> QuerySet:
        return self.get_queryset().of_post(post_id).all().without_removed_reacts().of_user(user_id=user_id)

    def create(self, **kwargs):
        react = kwargs.pop('react')
        obj, created = super().update_or_create(
            **kwargs,
            defaults={'react': react},
        )
        return obj
