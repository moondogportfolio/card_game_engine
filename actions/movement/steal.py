
from enum import Enum
from typing import Any
from attr import define, field
from actions.base_action import BaseTargetAction

from actions.movement.movement_action import BaseMovementAction
from classes.gamestate import GameState
from enums.entity_events import EntityEvents
from enums.location import LocEnum


@define
class StealEffect(BaseTargetAction):
    round_only: bool = field(default=False)
    event_enum: Enum = field(init=False, default=EntityEvents.SUMMON)

    def resolve(self, gamestate: GameState, origin: Any):
        return super().resolve(gamestate, origin)
