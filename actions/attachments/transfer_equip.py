from enum import Enum
from typing import Any
from attr import define, field
from actions.base_action import BaseAction
from card_classes.equipment import Equipment
from classes.gamestate import GameState
from custom_types.resolvables import ResolvableEntity
from enums.entity_events import EntityEvents


@define
class TransferEquipmentEffect(BaseAction):
    source: ResolvableEntity
    destination: ResolvableEntity
    event_enum: Enum = field(init=False, default=EntityEvents.FORGE)

    def resolve(self, gamestate: GameState):
        return super().resolve(gamestate)