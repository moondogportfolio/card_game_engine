

from enum import Enum
from typing import Any
from attr import define, field

from actions.base_action import BaseTargetAction
from classes.gamestate import GameState
from enums.attribute import AttrEnum


@define
class SwapAttributesEffect(BaseTargetAction):
    second_entity: Any
    target_attr: AttrEnum
    second_entity_attr: AttrEnum
