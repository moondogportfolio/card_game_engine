
from enum import Enum
from attr import define, field
from actions.base_action import BaseAction

@define
class CoeventAction:
    coevent: BaseAction
    action: BaseAction