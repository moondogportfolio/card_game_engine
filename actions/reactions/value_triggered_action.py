from enum import Enum, auto
from typing import Any, Callable, Dict
from attr import define, field

from actions.base_action import BaseAction
from actions.reactions.continuous_action import ContinuousAction
from actions.reactions.event_filter import EventFilter
from events.base_event import BaseEvent



class EventCounterEnum(Enum):
    COUNT_INSTANCES = auto()
    COUNT_VALUE = auto()
    BOOLEAN = auto()
    DISCRETE_ROUNDS = auto()
    UNIQUE_TARGETS = auto()

    def resolve(self):
        return event_counter_dict[self]
    
event_counter_dict: Dict[EventCounterEnum, Callable[[BaseEvent, int], int]] = {
    EventCounterEnum.COUNT_INSTANCES: lambda x, y: y+1 
}

def convert(event: EventCounterEnum):
    if callable(event):
        return event
    else:
        return event.resolve()
    
@define
class ValueTriggeredAction(ContinuousAction):
    threshold: int
    action_on_value: BaseAction
    event_counter: EventCounterEnum |  Callable[[BaseEvent, int], int] = field(converter=convert)
    player_bound: bool = field(default=False)
    round_end_reset: bool = field(default=False)
    on_activate_reset: bool = field(default=False)
    init_value: int = field(default=0, kw_only=True)
    value: Any = field(default=0, init=False)

    def resolve(self, event):
        return self.action_on_value
        self.increment(event)
        if self.value >= self.threshold:
            return self.action_on_value

    def increment(self, event):
        self.value = self.event_counter(event, self.value)

