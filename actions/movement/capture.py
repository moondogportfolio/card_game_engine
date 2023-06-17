from enum import Enum
from typing import Any, Tuple
from attr import define, field
from actions.base_action import BaseAction, BaseTargetAction
from classes.gamestate import GameState
from custom_types.converters import shortcut_enum_converter
from enums.attribute import AttrEnum

from enums.entity_events import EntityEvents
from enums.location import LocEnum
from events.base_event import BaseEvent
from events.create.CreateCardEvent import SimpleCreateCardEvent
from events.movement.capture_event import CaptureEvent


@define
class CaptureEffect(BaseTargetAction):
    storage: Any = field(converter=shortcut_enum_converter)
    destination: LocEnum = field(init=False, default=LocEnum.SHADOWREALM)
    event_enum: Enum = field(init=False, default=EntityEvents.REVIVE)
    gain_captured_stats: bool = field(default=False, kw_only=True)

    def get_target_objects(self) -> Tuple:
        return (self.target, self.storage)

    def resolve(self, target, storage, *args, **kwargs) -> BaseEvent | Tuple[BaseEvent]:
        return CaptureEvent(target=target, storage=storage)


@define
class RecreateCaptureEffect(BaseAction):
    def resolve(
        self, gamestate: GameState, origin: Any, postevent, *args, **kwargs
    ) -> BaseEvent | Tuple[BaseEvent]:
        moved_card = postevent.target
        captured = gamestate.attach_man.get_entity_attachment(
            moved_card, AttrEnum.CAPTURED_UNITS, True
        )
        if not captured:
            return
        events = []
        for card in captured:
            events.append(
                SimpleCreateCardEvent(
                    card_type=card,
                    location=LocEnum.HOMEBASE,
                    owner=moved_card.owner,
                )
            )
        return events
