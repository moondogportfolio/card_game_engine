
from attr import define, field

from actions.base_action import BaseAction


@define
class MultipleActivationsEffect(BaseAction):
    effect: BaseAction
    multiplier: int = field(default=2)