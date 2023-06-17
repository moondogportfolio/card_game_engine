from typing import Any
from attr import define

from actions.base_action import BaseTargetAction


@define
class ChallengeEffect(BaseTargetAction):
    challenger: Any