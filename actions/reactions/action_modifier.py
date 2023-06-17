
from enum import Enum
from typing import Any
from attr import define
from actions.reactions.continuous_action import ContinuousAction

from enums.operator import Ops_


@define
class ActionModifier(ContinuousAction):
    parameter: str
    operator: Ops_
    value: Any

    def modify_event(self, event):
        parameter = self.parameter
        original_param_value = getattr(event, parameter)
        new_param_value = self.operator.compute(original_param_value, self.value)
        setattr(event, parameter, new_param_value)
        # print(f'tamper {self.triggering_event.event} {parameter} {original_param_value} > {new_param_value}')
        return event