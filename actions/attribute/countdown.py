from enum import Enum
from attr import define, field
from events.attribute.SetAttributeEvent import SetAttributeEvent
from actions.base_action import BaseTargetAction
from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from enums.attribute import AttrEnum
from enums.entity_events import EntityEvents
from enums.operator import Ops_
from events.base_event import BaseTargetEvent


@define
class AdvanceCountdownEffect(BaseTargetAction):
    value: int = field(default=1)
    event_enum: Enum = field(init=False, default=EntityEvents.DAMAGE)

    def resolve(self, gamestate: GameState):
        return AdvanceCountdownEvent(
            event=EntityEvents.ADVANCE,
            attribute=AttrEnum.COUNTDOWN,
            value=1,
            operator=Ops_.DECREMENT,
        )

@define
class AdvanceCountdownEvent(SetAttributeEvent):
    ...

@define
class CountdownEvent(BaseTargetEvent):
    event: Enum = field(init=False, default=EntityEvents.COUNTDOWN)

    def resolve(self, gamestate: GameState, origin: CardArchetype, target):
        ...