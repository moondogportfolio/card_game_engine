

from attr import define
from actions.reactions.value_triggered_action import ValueTriggeredAction

@define
class ResetEventCounter:
    target: ValueTriggeredAction