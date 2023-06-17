
from attr import define, field
from actions.base_action import BaseAction
from actions.create.create_card import CreateCardEffect
from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from enums.entity_events import EntityEvents
from enums.location import LocEnum
from events.base_event import BaseEvent


@define
class SpawnEffect(BaseAction):
    quantity: int

    def resolve(self, gamestate: GameState):
        return SpawnEvent(event=EntityEvents.SPAWN, quantity=self.quantity)

@define
class SpawnEvent(BaseEvent):
    quantity: int

    def resolve(self, gamestate: GameState, origin: CardArchetype):
        return super().resolve(gamestate, origin)


@define
class SummonHuskEffect(CreateCardEffect):
    target: None = field(init=False)
    location: LocEnum = field(init=False, default=LocEnum.HOMEBASE)

    def resolve(self, gamestate: GameState):
        return super().resolve(gamestate)
