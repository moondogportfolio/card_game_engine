
from enum import Enum
from attr import define, field

from actions.movement.movement_action import BaseMovementAction
from classes.gamestate import GameState
from enums.entity_events import EntityEvents
from enums.location import LocEnum


@define
class MoveEffect(BaseMovementAction):
    destination: LocEnum | None
    index: int | None = field(default=None)
    event_enum: Enum = field(init=False, default=EntityEvents.SUMMON)

    def resolve(self, gamestate: GameState):
        self.relocate(gamestate)
