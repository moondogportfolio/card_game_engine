from enum import Enum
from typing import Literal
from attr import define, field
from events.attribute.SetAttributeEvent import SetAttributeEvent
from actions.base_action import BaseTargetAction
from classes.gamestate import GameState
from enums.attribute import AttrEnum
from enums.entity_events import EntityEvents
from enums.operator import Ops_


@define
class HealEffect(BaseTargetAction):
    value: int | Literal[Ops_.MAX]
    event_enum: Enum = field(init=False, default=EntityEvents.DAMAGE)

    def resolve(self, target, *args, **kwargs):
        return SetAttributeEvent(
            target=target,
            value=self.value,
            attribute=AttrEnum.HEALTH,
            operator=Ops_.INCREMENT,
            event=EntityEvents.HEAL
        )