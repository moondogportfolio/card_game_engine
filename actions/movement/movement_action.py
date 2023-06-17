from typing import Any
from attr import define, field

from actions.base_action import BaseTargetAction
from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from enums.entity_events import EntityEvents
from enums.location import LocEnum
from events.base_event import BaseEvent
from events.movement.MovementEvent import MovementEvent


@define
class BaseMovementAction(BaseTargetAction):
    destination: LocEnum = field(init=False)
    event: EntityEvents = field(init=False)

    def resolve(self, target, gamestate: GameState, origin: Any, *args, **kwargs) -> BaseEvent:
        return MovementEvent(target=target, destination=self.destination, event=self.event)


