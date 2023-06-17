from attr import define
from actions.base_action import BaseTargetAction
from classes.gamestate import GameState
from events.base_event import BaseEvent


@define
class DestroyAttachmentsEffect(BaseTargetAction):

    def resolve(self, gamestate: GameState):
        return super().resolve(gamestate)
    


@define
class DestroyEquipEffect(BaseTargetAction):

    def resolve(self, gamestate: GameState):
        return super().resolve(gamestate)
    
class DestroyEquipEvent(BaseEvent):
    ...
    
