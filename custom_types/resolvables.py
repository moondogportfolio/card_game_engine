from __future__ import annotations
from typing import List, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from classes.gamestate import GameState
    from entity_selectors.input import Input


class ShortcutEnum(Protocol):

    def get_longhand():
        ...

class InputEnum(Protocol):

    def get_input_object() -> Input:
        ...

class ResolvableEntity(Protocol):
    
    def resolve(self, gamestate: GameState, origin) -> None | List:
        ...


class ResolvableCondition(Protocol):
    
    def resolve(self, gamestate: GameState, origin, *args, **kwargs)  -> bool:
        ...