
from attr import define

from actions.base_action import BaseAction


@define
class CopySpellWithSameTargets(BaseAction):
    effect: BaseAction