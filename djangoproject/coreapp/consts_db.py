"""
Contains constants/wrapper classes for database model's fields like CHOICE_FIELD etc.
"""


class Reacts:
    """TODO: convert to enum"""
    NONE, LIKE, LOVE, HAHA, WOW, SAD, ANGRY = range(0, 7)
    __MAX = ANGRY

    REACT_NAMES = dict(
        [(NONE, 'NONE'), (LIKE, 'LIKE'), (LOVE, 'LOVE'), (HAHA, 'HAHA'), (WOW, 'WOW'), (SAD, 'SAD'), (ANGRY, 'ANGRY')])
    REACT_VALUE = dict(
        [('NONE', NONE), ('LIKE', LIKE), ('LOVE', LOVE), ('HAHA', HAHA), ('WOW', WOW), ('SAD', SAD), ('ANGRY', ANGRY)])

    @staticmethod
    def react_choices():
        REACT_TYPES = tuple(Reacts.REACT_NAMES.items())
        return REACT_TYPES

    @staticmethod
    def is_valid_react(react):
        if react is None:
            return False
        return Reacts.NONE <= react <= Reacts.__MAX


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
