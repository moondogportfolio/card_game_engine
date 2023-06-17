from enum import Enum
from attr import define, field
from actions.attachments.equip import EquipEvent
from actions.base_action import BaseTargetAction
from card_classes.equipment import Equipment
from classes.gamestate import GameState
from enums.entity_events import EntityEvents


@define
class AutoEquipEffect(BaseTargetAction):
    equipment: Equipment

    def resolve(self, gamestate: GameState):
        return EquipEvent(equipment=...)