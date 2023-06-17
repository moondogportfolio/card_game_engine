from dataclasses import field
from attr import define
from actions.base_action import BaseTargetAction


@define
class RecastEventOfAction(BaseTargetAction):
    multiplier: int = field(default=2)