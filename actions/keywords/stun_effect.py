from typing import Any
from attr import define

from actions.base_action import BaseTargetAction
from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from enums.entity_events import EntityEvents
from events.base_event import BaseTargetEvent


@define
class StunEffect(BaseTargetAction):

    def resolve(self, gamestate: GameState, origin: Any):
        return StunEvent(event=EntityEvents.STUN)
    
@define
class StunEvent(BaseTargetEvent):

    def resolve(self, gamestate: GameState, origin: CardArchetype, target):
        return super().resolve(gamestate, origin, target)