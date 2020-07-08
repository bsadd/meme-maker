"""
Contains constants/wrapper classes for database model's fields like CHOICE_FIELD etc.
"""
from django.db import models


class Reacts(models.IntegerChoices):
    NONE, LIKE, LOVE, HAHA, WOW, SAD, ANGRY = range(0, 7)


class ApprovalStatus:
    PENDING = 'p'
    APPROVED = 'a'
    REJECTED = 'r'
    __MAX = REJECTED

    STATUS_NAMES = {PENDING: 'PENDING', APPROVED: 'APPROVED', REJECTED: 'REJECTED'}
    STATUS_VALUE = {'PENDING': PENDING, 'APPROVED': APPROVED, 'REJECTED': REJECTED}

    @staticmethod
    def approval_status():
        STATUS = (
            (ApprovalStatus.PENDING, 'PENDING'),
            (ApprovalStatus.APPROVED, 'APPROVED'),
            (ApprovalStatus.REJECTED, 'REJECTED'))
        return STATUS

    @staticmethod
    def is_valid_status(status):
        if status is None:
            return False
        return ApprovalStatus.PENDING <= status <= ApprovalStatus.__MAX
