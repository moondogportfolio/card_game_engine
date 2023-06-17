
from attr import define, field
from actions.base_action import BaseAction
from classes.gamestate import GameState


@define
class ReforgeEffect(BaseAction):

    def resolve(self, gamestate: GameState):
        return super().resolve(gamestate)

@define
class GenerateCoinEffect(BaseAction):
    value: int = field(default=1)

    def resolve(self, gamestate: GameState):
        return super().resolve(gamestate)