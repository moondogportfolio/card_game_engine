
from attr import define
from classes.gamestate import GameState

from entity_selectors.base_card_filter import BaseCardFilter


@define
class ChooseBaseCard:
    choices: BaseCardFilter

    def resolve(self, gamestate: GameState):
        ...