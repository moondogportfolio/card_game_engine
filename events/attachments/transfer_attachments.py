from attr import define, field
from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from enums.entity_events import EntityEvents
from events.base_event import BaseTargetEvent


@define
class TransferAttachmentsEvent(BaseTargetEvent):
    event: EntityEvents = field(default=None, init=False)

    destination: CardArchetype

    def resolve(self, gamestate: GameState, origin: CardArchetype):
        #TODO
        ...