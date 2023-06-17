
from attr import define
from actions.base_action import SelectBaseCardsAction
from classes.gamestate import GameState
from entity_selectors.base_card_filter import InvokeBaseCardFilter


@define
class InvokeEffect(SelectBaseCardsAction):
    choices: InvokeBaseCardFilter

    def resolve(self, gamestate: GameState):
        return super().resolve(gamestate)
