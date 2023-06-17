from typing import Any
from attr import define, field
from actions.base_action import BaseAction
from classes.gamestate import GameState
from entity_selectors.card_filter import EntityFilter

from entity_selectors.target_game_card import TargetEntity
from resolvable_enums.target_player import TargetPlayer


# Support: Grant my supported ally +2|+2.
# If it has Support, grant its supported ally +2|+2 and
# continue for each supported ally in succession.
@define
class MountainSojournersEffect(BaseAction):

    def resolve(self, gamestate: GameState, origin: Any):
        return super().resolve(gamestate, origin)

# Attack: Grant me all keywords on allies.
@define
class MechanizedMimicEffect(BaseAction):

    def resolve(self, gamestate: GameState, origin: Any):
        return super().resolve(gamestate, origin)