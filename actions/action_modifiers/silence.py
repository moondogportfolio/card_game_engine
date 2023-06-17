from typing import Any, Tuple
from attr import define, field

from actions.base_action import BaseTargetAction
from enums.entity_events import EntityEvents
from events.actions_modifier.silence_event import SilenceEvent
from events.base_event import BaseEvent


@define
class SilenceEffect(BaseTargetAction):
    round_only: bool = field(default=False)

    def resolve(self, target, *args, **kwargs) -> BaseEvent | Tuple[BaseEvent]:
        return SilenceEvent(event=EntityEvents.SILENCE)
    
