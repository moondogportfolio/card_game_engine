from enum import Enum
from attr import define, field
from actions.base_action import BaseTargetAction
from card_classes.cardarchetype import CardArchetype
from card_classes.equipment import Equipment
from classes.gamestate import GameState
from enums.entity_events import EntityEvents
from events.base_event import BaseTargetEvent


@define
class UnequipEffect(BaseTargetAction):
    event_enum: Enum = field(init=False, default=EntityEvents.UNEQUIP)

    def resolve(self, *args, **kwargs):
        return UnequipEvent(event=EntityEvents.UNEQUIP)
    
@define
class UnequipEvent(BaseTargetEvent):
    
    def resolve(self, gamestate: GameState, origin: CardArchetype, target):
        gamestate.attach_man.remove_entity_attachment(target)
