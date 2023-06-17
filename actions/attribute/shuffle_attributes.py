from typing import Any
from attr import define, field
from events.attribute.SetAttributeEvent import SetAttributeEvent

from actions.base_action import BaseTargetAction
from classes.gamestate import GameState
from enums.attribute import AttrEnum
from enums.entity_events import EntityEvents


@define
class StatShuffleEfect(BaseTargetAction):
    def resolve(self, gamestate: GameState, origin: Any):
        health = ...
        attack = ...
        event1 = SetAttributeEvent(
            event=EntityEvents.SET_ATTRIBUTE,
            target=...,
            attribute=AttrEnum.HEALTH,
            value=...,
        )
        event2 = SetAttributeEvent(
            event=EntityEvents.SET_ATTRIBUTE,
            target=...,
            attribute=AttrEnum.ATTACK,
            value=...,
        )