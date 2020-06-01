"""
Contains constants/wrapper classes for database model's fields like CHOICE_FIELD etc.
"""


class Reacts:
    __slots__ = ()
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


class TextPositions:
    HEAD = 'h'
    TAIL = 't'
    OVER = 'o'

    @staticmethod
    def position_choices():
        # TEXT_POSITIONS = (
        #     (TextPositions.EXTRA_TOP, 'Above image'), (TextPositions.EXTRA_BOTTOM, 'Below Image'),
        #     (TextPositions.TOP, 'Top on image'), (TextPositions.BOTTOM, 'Bottom on image'),
        #     (TextPositions.CUSTOM, 'Custom Position'))
        TEXT_POSITIONS = (
            (TextPositions.HEAD, 'Above Image'),
            (TextPositions.TAIL, 'Below Image'),
            (TextPositions.OVER, 'Over Image')
        )
        return TEXT_POSITIONS

    @staticmethod
    def is_valid_position(position):
        return position in [p[0] for p in TextPositions.position_choices()]


class ApprovalStatus:
    __slots__ = ()
    PENDING = 'p'
    APPROVED = 'a'
    REJECTED = 'r'
    __MAX = REJECTED

    STATUS_NAMES = {PENDING: 'PENDING', APPROVED: 'APPROVED', REJECTED: 'REJECTED'}
    STATUS_VALUE = {'PENDING': PENDING, 'APPROVED': APPROVED, 'REJECTED': REJECTED}

    @staticmethod
    def approval_status():
        STATUS = (
            (ApprovalStatus.PENDING, 'Pending'),
            (ApprovalStatus.APPROVED, 'Approved'),
            (ApprovalStatus.REJECTED, 'Rejected'))
        return STATUS

    @staticmethod
    def is_valid_status(status):
        if status is None:
            return False
        return ApprovalStatus.PENDING <= status <= ApprovalStatus.__MAX
