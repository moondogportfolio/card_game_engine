from enum import Enum
from typing import Literal
from attr import define, field
from actions.base_action import BaseTargetAction
from classes.gamestate import GameState
from enums.attribute import AttrEnum
from enums.entity_events import EntityEvents
from enums.operator import Ops_


@define
class PhaseMoonWeaponEffect(BaseTargetAction):
    event_enum: Enum = field(init=False, default=EntityEvents.DAMAGE)

    def resolve(self, gamestate: GameState):
        gamestate.entity_man.set_attribute(
            target=self.target,
            attribute=AttrEnum.HEALTH,
            value=self.value,
            operator=Ops_.INCREMENT,
        )
