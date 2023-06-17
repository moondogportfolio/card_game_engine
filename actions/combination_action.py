from typing import List
from attr import define

from actions.base_action import BaseAction


@define
class CombinationAction:
    actions: List[BaseAction]