

from typing import Any
from attr import define

from actions.base_action import BaseAction


@define
class PostEventParamGetter:
    effect: BaseAction
    parameter: Any