from typing import List
from attr import define, field
from actions.base_action import BaseAction
from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from entity_selectors.card_filter import CardFilter

from enums.keywords import KeywordEnum
from enums.subtypes import SubTypes_
from enums.types import Types_
from resolvable_enums.active_cards_selector import TargetShorthand


@define
class Equipment(CardArchetype):
    attack: int = field(default=10)
    health: int = field(default=10)
    bearer_attack_commit_effect: List[BaseAction] | None = field(default=None, kw_only=True)
    subtype_modifier: List[SubTypes_] | None = field(default=None, kw_only=True)
    bearer: CardFilter = field(init=False, default=TargetShorthand.ALLIED_BOARD_UNIT) 

    def is_type_instance(self, type: Types_):
        if type is Types_.EQUIPMENT:
            return True
        return False


    def check_validity(self, gamestate: GameState):
        bearer_val = self.bearer.check_validity(gamestate, self.action_origin)
        return super().check_validity(gamestate) and bearer_val