

from attr import define, field
from actions.reactions.continuous_action import ContinuousAction

from actions.reactions.event_filter import EventFilter
from enums.location import LocEnum


@define
class ActionNegator(ContinuousAction):
    ...