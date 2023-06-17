from enum import Enum
from attr import define

from actions.base_action import BaseAction


@define
class ActionRequisite:
    action: Enum
    requisite: BaseAction