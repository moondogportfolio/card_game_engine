
from attr import define, field

from actions.base_action import BaseAction


@define
class CountdownEffect(BaseAction):
    effect: BaseAction = field()
    countdown: int