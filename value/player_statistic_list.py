from enum import Enum, auto


class PlayerStatisticList(Enum):
    ALLIES_DEAD_THIS_GAME = auto()
    ALLIES_DEAD_THIS_ROUND = auto()
    ALLIES_SUMMONED_THIS_ROUND = auto()
    KEYWORDS_ALLIES_GAINED = auto()

    def resolve():
        ...