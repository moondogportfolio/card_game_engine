from __future__ import annotations
from enum import Enum
from random import choice
from typing import TYPE_CHECKING, Any, List
from attr import define, field

from custom_types.resolvables import ResolvableEntity

if TYPE_CHECKING:
    from actions.base_action import BaseAction
    from entity_selectors.base_card_filter import BaseCardFilter


@define
class Input(ResolvableEntity):
    choices: ResolvableEntity
    quantity: int = field(default=1, kw_only=True)
    minimum: int = field(default=1, kw_only=True)
    selection: Any | None = field(init=False, default=None)
    message: str = field(default="Select choice", kw_only=True)
    
    randomize: bool = field(default=False, kw_only=True)


@define
class ChoiceBaseCard(Input):
    choices: BaseCardFilter


@define
class ChoiceValue(Input):
    choices: Enum | int


@define
class ChoiceAction(Input):
    choices: List[BaseAction]
    randomized: bool = field(default=False, kw_only=True)
