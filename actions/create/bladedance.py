from attr import define

from actions.base_action import BaseAction
from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from enums.entity_events import EntityEvents
from enums.location import LocEnum
from events.base_event import BaseEvent


@define
class BladedanceEffect(BaseAction):
    quantity: int

    def resolve(self, gamestate: GameState):
        return BladedanceEvent(event=EntityEvents.BLADE_DANCE)
        gamestate.entity_man.create_card(
            ..., LocEnum.BATTLEFIELD, self.action_origin, gamestate, self.quantity
        )

@define
class BladedanceEvent(BaseEvent):

    def resolve(self, gamestate: GameState, origin: CardArchetype):
        return super().resolve(gamestate, origin)
