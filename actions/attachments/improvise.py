from enum import Enum
from attr import define, field
from actions.base_action import BaseTargetAction
from card_classes.equipment import Equipment
from classes.gamestate import GameState
from enums.entity_events import EntityEvents


@define
class ImproviseEffect(BaseTargetAction):
    event_enum: Enum = field(init=False, default=EntityEvents.IMPROVISE)

    def resolve(self, gamestate: GameState):
        return super().resolve(gamestate)