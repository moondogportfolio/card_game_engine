
from enum import Enum, auto
from operator import eq
from typing import Any, List
from attr import define, field
from classes.gamestate import GameState

from custom_types.resolvables import ResolvableCondition, ResolvableEntity
from enums.attribute import AttrEnum
from enums.post_event_param import PostEventParam
from resolvable_enums.auto_card_selector import AutoEntitySelector
from resolvable_enums.card_conditions import CardFlags
from resolvable_enums.player_conditions import PlayerFlags
from resolvable_enums.target_player import TargetPlayer
from value.player_statistic import PlayerStatistic


class ConditionOperator(Enum):
    GREATER_THAN = auto()
    EQUAL_TO = auto()
    AT_LEAST = auto()

@define
class Condition:
    target: ResolvableEntity | PostEventParam
    condition: ResolvableCondition | CardFlags | PlayerFlags | None = field(default=None)
    parameter: Any | List | None = None
    invert_result: bool = field(default=False, kw_only=True)

    def resolve(self, gamestate: GameState, origin, *args, **kwargs):
        if type(self.target) is PostEventParam:
            postevent = kwargs['postevent']
            target = self.target.resolve(postevent)
        else:
            target = self.target.resolve(gamestate, origin)
        if type(self.condition) in (CardFlags, PlayerFlags):
            condition = self.condition.resolve()
        elif self.condition is None:
            return target == self.parameter
        else:
            condition = self.condition
        try:
            return condition(gamestate, origin, target, *self.parameter)
        except TypeError:
            return condition(gamestate, origin, target, self.parameter)
    

@define
class OwnerCondition(Condition):
    target: ResolvableEntity = field(init=False, default=TargetPlayer.ORIGIN_OWNER)

@define
class OwnerStatisticCondition(Condition):
    target: ResolvableEntity = field(init=False, default=TargetPlayer.ORIGIN_OWNER)
    condition: PlayerStatistic
    parameter: int

@define
class SelfCondition(Condition):
    target: ResolvableEntity = field(init=False, default=AutoEntitySelector.SELF)


@define
class AttributeCondition(Condition):
    attribute: AttrEnum = field(default=AttrEnum.ATTACK)
    condition: ResolvableCondition = field(init=False, default=None)
    operator: ConditionOperator = field(default=ConditionOperator.EQUAL_TO)

@define
class PostEventAttributeCondition:
    attribute: AttrEnum
    parameter: Any

@define
class PostEventTargetCondition(Condition):
    target: ResolvableEntity = field(init=False, default=None)
