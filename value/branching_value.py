from typing import Any
from attr import define
from actions.base_action import BaseAction

@define
class BranchingValue:
    condition: Any
    if_true: Any
    if_false: Any