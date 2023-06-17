
from enum import Enum, auto


class EventQueryParamGetter(Enum):
    INSTANCES = auto()
    DISTINCT_ROUNDS = auto()
    
    


class EventQueryTimeframe(Enum):
    THIS_ROUND = auto()
    LAST_ROUND = auto()
    ENTIRE_GAME = auto()