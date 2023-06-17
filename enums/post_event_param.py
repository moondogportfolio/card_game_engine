from enum import Enum, auto


class PostEventParam(Enum):
    TARGET = auto()
    SKILL_ORIGIN = auto()
    SUPPORTER = auto()
    VALUE = auto()
    CREATED_CARD = auto()
    EQUIPMENT = auto()
    TARGET_KILLED = auto()
    STRIKER = auto()
    
    def resolve(self, postevent, *args, **kwargs):
        return getattr(postevent, self.name.lower())