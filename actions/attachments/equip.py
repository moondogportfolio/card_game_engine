from enum import Enum
from attr import define, field
from actions.base_action import BaseTargetAction
from card_classes.cardarchetype import CardArchetype
from card_classes.equipment import Equipment
from classes.gamestate import GameState
from enums.entity_events import EntityEvents
from events.base_event import BaseTargetEvent


@define
class EquipEffect(BaseTargetAction):
    equipment: Equipment

    def resolve(self, target, equipment, *args, **kwargs):
        return EquipEvent(event=EntityEvents.IS_EQUIPPED_WITH, equipment=self.equipment)

@define
class EquipEvent(BaseTargetEvent):
    equipment: Equipment

    def resolve(self, gamestate: GameState, origin: CardArchetype, target):
        gamestate.attach_man.set_entity_attachment(target, self.equipment)
