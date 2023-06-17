
from enum import Enum
from typing import Literal
from attr import define, field
from events.movement.MovementEvent import MovementEvent


from actions.movement.movement_action import BaseMovementAction
from classes.gamestate import GameState
from enums.entity_events import EntityEvents
from enums.location import LocEnum


@define
class DiscardEffect(BaseMovementAction):
    quantity: int = field(default=1)
    destination: LocEnum = field(init=False, default=LocEnum.SHADOWREALM)
    event_enum: Enum = field(init=False, default=EntityEvents.DISCARD)

    def resolve(self, gamestate: GameState, origin):
        # return self.relocate(gamestate)
        
        return MovementEvent(
            event=EntityEvents.DISCARD,
            destination=LocEnum.SHADOWREALM
        )



