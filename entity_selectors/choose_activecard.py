
from attr import define, field
from classes.gamestate import GameState
from entity_selectors.card_filter import CardFilter


@define
class ChooseActiveCard:
    choices: CardFilter

    def resolve(self, gamestate: GameState):
        ...