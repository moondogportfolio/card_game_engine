
from enum import Enum
from attr import define, field
from events.movement.MovementEvent import MovementEvent


from actions.movement.movement_action import BaseMovementAction
from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from enums.entity_events import EntityEvents
from enums.location import LocEnum


@define
class SummonEffect(BaseMovementAction):
    destination: LocEnum = field(default=LocEnum.HOMEBASE)
    event_enum: Enum = field(init=False, default=EntityEvents.SUMMON)

    def resolve(self, gamestate: GameState):
        self.relocate(gamestate)


@define
class SummonEvent(MovementEvent):
    event: Enum = field(init=False, default=EntityEvents.SUMMON)

    def resolve(self, gamestate: GameState, origin: CardArchetype, target):
        return super().resolve(gamestate, origin, target)