from typing import Any
from attr import define, field
from actions.reactions.event_filter import EventFilter

from actions.reactions.triggered_action import TriggeredAction
from enums.entity_events import EntityEvents

te = EventFilter(event=EntityEvents.SUMMON)


@define
class UponSummonAlly(TriggeredAction):
    triggering_event: EventFilter = field(init=False, default=te)
