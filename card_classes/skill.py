from typing import List
from attr import define, field
from actions.base_action import BaseAction

from card_classes.cardarchetype import CardArchetype
from enums.spell_speed import SpellSpeedEnum


@define
class Skill(CardArchetype):
    activation_effect: List[BaseAction] | BaseAction = field(kw_only=True)
    