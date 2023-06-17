from enum import Enum
from typing import Any, Tuple

from attr import define, field

from actions.base_action import BaseAction, BaseTargetAction
from classes.gamestate import GameState
from custom_types.converters import shortcut_enum_converter
from enums.entity_events import EntityEvents
from events.base_event import BaseEvent
from events.battle.strike import StrikeEvent


@define
class StrikeEffect(BaseTargetAction):
    striker: Any = field(converter=shortcut_enum_converter)
    event_enum: Enum = field(init=False, default=EntityEvents.STRIKE)

    def get_target_objects(self) -> Tuple:
        return (self.target, self.striker)
    
    def resolve(self, target, striker, *args, **kwargs) -> BaseEvent | Tuple[BaseEvent]:
        return StrikeEvent(striker=striker, target=target)

@define
class MutualStrikeEffect(BaseAction):
    first_striker: Any
    second_striker: Any
