from typing import Any
from attr import define
from actions.base_action import BaseTargetAction

from card_classes.skill import Skill
from classes.gamestate import GameState

@define
class PlaySkill(BaseTargetAction):
    target: Skill

    def resolve(self, gamestate: GameState, origin: Any):
        return super().resolve(gamestate, origin)