from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState


from attr import define

from events.base_event import BaseTargetEvent


@define
class NegateQueuedSpellEvent(BaseTargetEvent):

    def resolve(self, gamestate: GameState, origin: CardArchetype, *args, **kwargs):
        gamestate.spell_stack_man.remove_from_q(target=self.target)