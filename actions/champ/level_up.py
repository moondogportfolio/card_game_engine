from typing import Any
from attr import define

from actions.base_action import BaseTargetAction
from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from enums.entity_events import EntityEvents
from events.base_event import BaseTargetEvent


@define
class LevelupEffect(BaseTargetAction):
    new_form: CardArchetype

    def resolve(self, origin, *args, **kwargs):
        return LevelupEvent(event=EntityEvents.LEVEL_UP, target=origin)

@define
class LevelupEvent(BaseTargetEvent):
    
    def resolve(self, gamestate: GameState, origin: CardArchetype):
        print('OK LEVELUP')
    

