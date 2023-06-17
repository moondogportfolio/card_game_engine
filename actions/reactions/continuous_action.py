from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, List
from attr import define, field
from custom_types.converters import shortcut_enum_converter
from enums.entity_events import EntityEvents
from enums.location import LocEnum
from enums.origin_enum import OriginEnum

if TYPE_CHECKING:
    from card_classes.cardarchetype import CardArchetype
    from events.base_event import BaseEvent
    from conditions.base_condition import Condition


@define
class ContinuousAction:
    event_filter: EntityEvents
    ally_enum: OriginEnum | Callable[[BaseEvent, CardArchetype], bool] = field(
        default=OriginEnum.ALLY, converter=shortcut_enum_converter, kw_only=True
    )
    round_only: bool = field(default=False, kw_only=True)
    activate_once: bool = field(default=False, kw_only=True)
    activations_per_round: int | None = field(default=None, kw_only=True)
    location: LocEnum = field(default=LocEnum.HOMEBASE, kw_only=True)
    instance_bound: bool = field(default=True, kw_only=True)
    condition: Condition | None = field(kw_only=True, default=None)

    def is_triggered(self, gamestate, origin, postevent: BaseEvent, *args, **kwargs):
        if self.event_filter != postevent.event:
            return False
        if self.condition:
            if not self.condition.resolve(
                gamestate, origin, postevent, *args, **kwargs
            ):
                return False
        if self.ally_enum:
            if not self.ally_enum(postevent, origin):
                return False
        return True
