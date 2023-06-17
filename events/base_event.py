from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, List
from attr import Attribute, asdict, define, evolve, field, fields
from conditions.base_condition import Condition
from entity_selectors.base_card_filter import BaseCardFilter
from classes.gamestate import GameState
from custom_types.resolvables import ResolvableEntity
from enums.entity_events import EntityEvents
from resolvable_enums.target_player import TargetPlayer

if TYPE_CHECKING:
    from card_classes.cardarchetype import CardArchetype


@define()
class BaseEvent:
    event: EntityEvents
    success: bool = field(init=False)
    negated: bool = field(init=False)
    modified: bool = field(init=False)

    def resolve(self, gamestate: GameState, origin: CardArchetype):
        ...

    def append_extra_signals(self, signals_list: List) -> EntityEvents:
        ...



@define
class BaseTargetEvent(BaseEvent):
    target: CardArchetype = field(kw_only=True, default=None)

    def get_target_len(self):
        try:
            return len(self.target)
        except TypeError:
            return 1

