"""
Contains constants/wrapper classes for database model's fields like CHOICE_FIELD etc.
"""
from django.db import models


class Reacts(models.IntegerChoices):
    NONE, LIKE, LOVE, HAHA, WOW, SAD, ANGRY = range(0, 7)


class ApprovalStatus(models.TextChoices):
    PENDING = 'p'
    APPROVED = 'a'
    REJECTED = 'r'
