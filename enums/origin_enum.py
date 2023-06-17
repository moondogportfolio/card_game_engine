from __future__ import annotations
from enum import Enum, auto
from typing import TYPE_CHECKING, Callable, Dict


if TYPE_CHECKING:
    from card_classes.cardarchetype import CardArchetype
    from events.base_event import BaseEvent, BaseTargetEvent
    from card_classes.cardarchetype import CardArchetype
    from events.base_event import BaseEvent


class OriginEnum(Enum):
    ALLY = auto()
    OPPONENT = auto()
    SELF = auto()
    T_ALLY_O_ALLY = auto()
    T_SELF = auto()
    T_SELF_O_OPPO = auto()
    T_SELF_O_ALLY = auto()
    T_OPPO = auto()
    T_ALLY = auto()
    T_SELFCLASS = auto()
    O_ALLY = auto()
    O_OPPO = auto()
    
    T_OPPO_O_ALLY = auto()
    T_OPPO_O_OPPO = auto()
    T_OPPO_O_SELF = auto()
    O_SELF = auto()
    S_STRIKER = auto()
    T_OPPONEXUS = auto()
    T_OPPONEXUS_O_ALLY = auto()
    T_SELF_STRIKER_OPPO = auto()

    SUPPORTER_SELF = auto()

    def get_longhand(self):
        return tp_dict[self]
    
tp_dict: Dict[OriginEnum, Callable[[BaseEvent|BaseTargetEvent, CardArchetype]], bool] = {
    OriginEnum.T_ALLY_O_ALLY: lambda x,y: True,
    OriginEnum.T_SELF: lambda x,y: x.target is y,
    OriginEnum.T_ALLY: True
}