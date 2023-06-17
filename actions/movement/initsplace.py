from enum import Enum
from typing import Any, Tuple, Type
from attr import define, field
from actions.base_action import BaseAction, BaseTargetAction
from actions.create.create_card import CreateCardEffect

from enums.entity_events import EntityEvents
from enums.location import LocEnum
from events.base_event import BaseEvent
from events.movement.swap_event import SwapPositionsEvent

events = {LocEnum.HAND: EntityEvents.RECALL}


@define
class InItsPlaceEffect(BaseTargetAction):
    replacement: BaseAction | Type
    destination: LocEnum

    def resolve(self, target, gamestate, origin, *args, **kwargs) -> BaseEvent | Tuple[BaseEvent]:
        event1 = CreateCardEffect(
            target=self.replacement,
            location=LocEnum.SHADOWREALM,
            owner=origin.owner,
        ).resolve(gamestate, origin, *args, **kwargs)
        event2 = SwapPositionsEvent(
            target=target,
            destination=event1.created_card[0],
        )
        return (event1, event2)
