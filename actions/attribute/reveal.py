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
class RevealEffect(BaseTargetAction):
    
    def resolve(self, gamestate: GameState):
        return HandRevealEvent(
            event=EntityEvents.REVEALED,
            attribute=AttrEnum.REVEALED,
            value=True,
        )

@define
class HandRevealEvent(SetAttributeEvent):
    ...