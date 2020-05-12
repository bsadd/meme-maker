class Reacts:
    __slots__ = ()
    NONE = 0
    UPVOTE = 1
    DOWNVOTE = 2
    MAX = DOWNVOTE

    REACT_NAMES = {0: 'NONE', 1: 'UPVOTE', 2: 'DOWNVOTE'}
    REACT_VALUE = {'NONE': 0, 'UPVOTE': 1, 'DOWNVOTE': 2}

    @staticmethod
    def react_choices():
        REACT_TYPES = ((Reacts.NONE, 'None'), (Reacts.UPVOTE, 'Up-vote'), (Reacts.DOWNVOTE, 'Down-vote'))
        return REACT_TYPES

    @staticmethod
    def is_valid_react(react):
        if react is None:
            return False
        return Reacts.NONE <= react <= Reacts.MAX


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
