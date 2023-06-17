from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable
from attr import define, field

if TYPE_CHECKING:
    from actions.base_action import BaseAction
    from conditions.base_condition import Condition

@define
class BranchingAction:
    if_true: BaseAction 
    if_false: BaseAction
    condition: Condition | None

    def resolve(self, gamestate, origin: Any, *args, **kwargs):
        if self.condition.resolve(gamestate, origin):
            return self.if_true
        else:
            return self.if_false