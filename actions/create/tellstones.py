
from typing import Annotated, List
from attr import define
from actions.base_action import SelectBaseCardsAction
from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from entity_selectors.base_card_filter import InvokeBaseCardFilter


@define
class TellstonesEffect(SelectBaseCardsAction):
    choices: List[CardArchetype]

    def resolve(self, gamestate: GameState):
        return super().resolve(gamestate)
