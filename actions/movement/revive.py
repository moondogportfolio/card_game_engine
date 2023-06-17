
from enum import Enum
from attr import define, field

from actions.movement.movement_action import BaseMovementAction
from classes.gamestate import GameState
from enums.entity_events import EntityEvents
from enums.location import LocEnum


@define
class ReviveEffect(BaseMovementAction):
    destination: LocEnum = field(kw_only=True, default=LocEnum.HOMEBASE)
    event_enum: Enum = field(init=False, default=EntityEvents.REVIVE)

    def resolve(self, gamestate: GameState):
        self.relocate(gamestate)
