from card_classes.cardarchetype import CardArchetype
from card_classes.cardslot import CardSlot
from classes.gamestate import GameState
from enums.entity_events import EntityEvents
from events.base_event import BaseTargetEvent


from attr import define, field


@define
class SwapPositionsEvent(BaseTargetEvent):
    event: EntityEvents = field(init=False, default=None)
    target: CardSlot
    destination: CardSlot

    def resolve(self, gamestate: GameState, origin: CardArchetype):
        gamestate.loc_man.swap_cards(self.target, self.destination)