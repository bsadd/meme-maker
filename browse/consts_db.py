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
