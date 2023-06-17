from enum import Enum
from typing import Any, Tuple
from attr import define, field
from actions.base_action import BaseTargetAction

from classes.gamestate import GameState
from custom_types.resolvables import ResolvableEntity
from enums.entity_events import EntityEvents
from events.base_event import BaseEvent
from events.movement.swap_event import SwapPositionsEvent


@define
class SwapPositionsEffect(BaseTargetAction):
    destination: ResolvableEntity

    def get_target_objects(self) -> Tuple:
        return (self.target, self.destination)

    def resolve(self, target, destination, *args, **kwargs) -> BaseEvent:
        return SwapPositionsEvent(
            event=None, target=target.cardslot, destination=destination.cardslot
        )
