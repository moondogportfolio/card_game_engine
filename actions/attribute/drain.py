from enum import Enum
from attr import define, field
from actions.base_action import BaseTargetAction
from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from enums.attribute import AttrEnum
from enums.entity_events import EntityEvents
from enums.operator import Ops_
from events.base_event import BaseTargetEvent


@define
class DrainEffect(BaseTargetAction):
    value: int

    def resolve(self, target, *args, **kwargs):
        return DrainEvent(
            event=EntityEvents.DRAIN,
            value=self.value,
            target=target,
        )


@define
class DrainEvent(BaseTargetEvent):
    value: int

    def resolve(self, gamestate: GameState, origin: CardArchetype):
        gamestate.entity_man.set_attribute(
            target=self.target,
            attribute=AttrEnum.HEALTH,
            value=self.value,
            operator=Ops_.DECREMENT,
        )
        gamestate.entity_man.set_attribute(
            target=self.target.owner,
            attribute=AttrEnum.HEALTH,
            operator=Ops_.INCREMENT,
            value=self.value,
        )
