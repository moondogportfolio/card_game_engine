
from enum import Enum
from typing import Callable
from attr import define, field
from actions.base_action import BaseAction
from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from conditions.base_condition import Condition

@define
class StateTriggeredAction:
    action: BaseAction
    condition: Callable[[GameState, CardArchetype], bool] | None = field(default=None)
    round_only: bool = field(default=False, kw_only=True)
    activate_once: bool = field(default=False, kw_only=True)
    activations_per_round: int | None = field(default=None, kw_only=True)
    instance_bound: bool = field(default=True, kw_only=True)