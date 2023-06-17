
from attr import define, field

from enums.entity_events import EntityEvents
from events.event_query_enum import EventQueryParamGetter, EventQueryTimeframe


@define
class EventFilter:
    target: ...


@define
class EventQuery:
    '''
    :param target_filter
    EventFilter default is:
    target: opponent
    origin: ally
    '''
    event: EntityEvents | EventFilter
    param_getter: EventQueryParamGetter
    timeframe: EventQueryTimeframe = field(default=EventQueryTimeframe.ENTIRE_GAME)