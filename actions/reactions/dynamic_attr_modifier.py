from enum import Enum
from typing import Any

from attr import define, field
from conditions.base_condition import Condition
from enums.attribute import AttrEnum
from enums.location import LocEnum
from enums.operator import Ops_
from resolvable_enums.auto_card_selector import AutoEntitySelector

@define
class DynamicAttributeModifier:
    attribute: AttrEnum
    value: int
    condition: Condition | Enum
    target: Any = field(default=AutoEntitySelector.ORIGIN)
    origin_location: LocEnum | None= field(default=LocEnum.BATTLEFIELD, kw_only=True)
    max_value: int | None = field(default=None, kw_only=True)
    operator: Ops_ = field(default=Ops_.INCREMENT, kw_only=True)

@define
class DynamicCostModifier(DynamicAttributeModifier):
    attribute: AttrEnum = field(init=False, default=AttrEnum.COST)

@define
class DynamicAttackModifier(DynamicAttributeModifier):
    attribute: AttrEnum = field(init=False, default=AttrEnum.ATTACK)


@define
class DynamicAtkHPModifier(DynamicAttributeModifier):
    # value_attack: int
    # value_health: int
    attribute: AttrEnum = field(init=False, default=(AttrEnum.ATTACK, AttrEnum.HEALTH))



@define
class DynamicKeywordModifier(DynamicAttributeModifier):
    attribute: AttrEnum = field(init=False, default=AttrEnum.KEYWORDS)

