from typing import List

from attr import define
from actions.reactions.triggered_action import TriggeredAction
from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from events.base_event import BaseTargetEvent

@define
class GrantReactionActions(BaseTargetEvent):
    triggered_action: TriggeredAction | List[TriggeredAction]
    
    def resolve(self, gamestate: GameState, origin: CardArchetype, *args, **kwargs):
        try:
            for sub_ta in self.triggered_action:
                gamestate.event_man.add_action(sub_ta, self.target)
        except TypeError:
            gamestate.event_man.add_action(self.triggered_action, self.target)