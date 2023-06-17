from typing import List
from attr import define, field

from actions.base_action import BaseTargetAction
from classes.gamestate import GameState
from entity_selectors.card_filter import CardFilter
from entity_selectors.input import Input
from enums.location import LocEnum


class PredictEvent:
    choices: List
    chosen_card: any


target = Input(choices=CardFilter(location=LocEnum.DECK))


@define
class PredictEffect(BaseTargetAction):
    target: Input = field(init=False, default=target)

    def resolve(self, gamestate: GameState):
        gamestate.loc_man.move_card(
            target=self.target,
            new_location=LocEnum.DECK,
            player=self.action_origin.owner,
            index=0,
        )
