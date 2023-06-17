
from attr import define
from actions.base_action import BaseAction

from actions.reactions.continuous_action import ContinuousAction


@define
class ActionReplacement(ContinuousAction):
    replacement_action: BaseAction