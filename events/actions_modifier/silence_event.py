
from attr import define
from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState

from events.base_event import BaseTargetEvent


@define
class SilenceEvent(BaseTargetEvent):

    def resolve(self, gamestate: GameState, origin: CardArchetype, target):
        return super().resolve(gamestate, origin, target)
        #TODO