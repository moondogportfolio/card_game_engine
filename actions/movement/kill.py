
from enum import Enum
from attr import define, field

from actions.movement.movement_action import BaseMovementAction
from classes.gamestate import GameState
from enums.entity_events import EntityEvents
from enums.location import LocEnum


@define
class KillAction(BaseMovementAction):
    destination: LocEnum = field(init=False, default=LocEnum.GRAVEYARD)
    event: Enum = field(init=False, default=EntityEvents.KILL)



@define
class DestroyLandmarkEffect(BaseMovementAction):
    destination: LocEnum = field(init=False, default=LocEnum.GRAVEYARD)
    event_enum: Enum = field(init=False, default=EntityEvents.DESTROY_LANDMARK)
