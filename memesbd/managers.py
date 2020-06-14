from django.db import models
from memesbd.consts_db import *


class ApprovedPostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(approval_status=ApprovalStatus.APPROVED)


class PendingPostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(approval_status=ApprovalStatus.PENDING)
