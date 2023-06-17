from enum import Enum, auto


class GameStateEnums(Enum):
    GAME_START = auto()
    ROUND_START = auto()
    MAIN_PHASE = auto()
    ROUND_END = auto()