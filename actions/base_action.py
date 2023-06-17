from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, List, Tuple
from attr import Attribute, asdict, define, evolve, field, fields
from custom_types.converters import shortcut_enum_converter
from custom_types.resolvables import ShortcutEnum
from entity_selectors.input import Input

if TYPE_CHECKING:
    from classes.gamestate import GameState
    from events.base_event import BaseEvent
    from custom_types.resolvables import InputEnum, ResolvableEntity
    from enums.base_action_attribute import BaseActionAttrEnum
    from events.base_event import BaseEvent
    from resolvable_enums.target_player import TargetPlayer
    from classes.gamestate import GameState
    from entity_selectors.base_card_filter import BaseCardFilter
    from conditions.base_condition import Condition
    from card_classes.cardarchetype import CardArchetype


@define
class BaseAction(ABC):
    condition: Callable[[GameState], bool] | Condition | None | Enum = field(
        kw_only=True, default=None
    )
    fizz_if_fail: None | BaseAction = field(default=None, kw_only=True)
    coevent: None | BaseAction = field(default=None, kw_only=True)

    def resolve_param(self, param: BaseActionAttrEnum, gamestate: GameState, origin):
        value = getattr(self, param.name.lower(), None)
        # resolvable
        try:
            return value.resolve(gamestate, origin)
        except AttributeError:
            ...
        # callable
        try:
            return value(gamestate, origin)
        except:
            ...
        return value

    # def resolve_params(self, gamestate: GameState):
    #     fds: List[Attribute] = fields(type(self))
    #     selfdict = {field.name: getattr(self, field.name, None) for field in fds}
    #     for k,v in selfdict.items():
    #         if v is None or isinstance(v, int):
    #             continue
    #         setattr(self, k, resolve(k, v, gamestate, self.action_origin))
    #     return self

    @abstractmethod
    def resolve(
        self, gamestate: GameState, origin: Any, *args, **kwargs
    ) -> BaseEvent | Tuple[BaseEvent]:
        ...

    def resolve_condition(self, gamestate: GameState, origin, *args, **kwargs):
        if not self.condition:
            return True
        return self.condition.resolve(gamestate, origin, *args, **kwargs)


@define
class TestBaseAction(BaseAction):
    def resolve(self, *args, **kwargs):
        print("TEST OK")


@define
class SelectBaseCardsAction(BaseAction):
    choices: BaseCardFilter


@define
class BaseTargetAction(BaseAction):
    # target: ResolvableEntity | Input
    target: ShortcutEnum | Input = field(converter=shortcut_enum_converter)
    target_exclusion: ResolvableEntity | None = field(default=None, kw_only=True)
    target_player: TargetPlayer | None = field(default=None, kw_only=True)
    exclude_origin: bool = field(default=False, kw_only=True)

    def resolve(
        self, target: CardArchetype, gamestate: GameState, origin: CardArchetype, *args, **kwargs
    ) -> BaseEvent | Tuple[BaseEvent]:
        ...

    def get_target_objects(self) -> Tuple:
        return (self.target,)

    # def validate_targets(self, gamestate: GameState) -> bool:
    #     return True if self.target.resolve(gamestate) else False

    # def resolve_params(self, gamestate):
    #     if not hasattr(self, 'target') or not self.target:
    #         return
    #     if type(self.target) is TargetPlayer:
    #         target = target_player_resolver(self.target, None, gamestate)
    #     else:
    #         target = self.target.resolve(gamestate)
    #     return target

   

@define
class BaseTargetValueAction(BaseTargetAction):
    value: int | ResolvableEntity

    