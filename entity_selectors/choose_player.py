
from typing import Any
from attr import define, field
from classes.gamestate import GameState

from entity_selectors.base_card_filter import BaseCardFilter


@define
class ChoosePlayer:
    choices: Any = field(init=False)

    def resolve(self, gamestate: GameState):
        ...