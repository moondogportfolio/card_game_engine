from typing import Any
from attr import define, field
from events.base_event import BaseEvent
from classes.gamestate import GameState
from actions.base_action import BaseTargetAction
from enums.attribute import AttrEnum
from enums.entity_events import EntityEvents
from enums.operator import Ops_

@define
class SetAttribute(BaseTargetAction):
    attribute: AttrEnum
    value: Any
    operator: Ops_ = field(default=Ops_.INCREMENT)
    event_enum = EntityEvents.SET_ATTRIBUTE

    def resolve(self, gamestate: GameState):
        gamestate.entity_man.set_attribute(
            target=self.target,
            attribute=self.attribute,
            value=self.value,
            operator=self.operator,
        )
        # return SetAttributeEvent(self.target, old_value, new_value)

