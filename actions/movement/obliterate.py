
from enum import Enum
from attr import define, field
from events.movement.MovementEvent import MovementEvent


from actions.movement.movement_action import BaseMovementAction
from classes.gamestate import GameState
from enums.entity_events import EntityEvents
from enums.location import LocEnum


@define
class ObliterateEffect(BaseMovementAction):
    destination: LocEnum = field(init=False, default=LocEnum.SHADOWREALM)
    event_enum: Enum = field(init=False, default=EntityEvents.OBLITERATE)

    def resolve(self, target):
        return MovementEvent(
            event=EntityEvents.OBLITERATE,
            destination=LocEnum.SHADOWREALM
        )

