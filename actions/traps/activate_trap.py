
from attr import define
from actions.base_action import BaseAction
from classes.gamestate import GameState


@define
class ActivateTrapEffect(BaseAction):

    def resolve(self, gamestate: GameState):
        return super().resolve(gamestate)
    