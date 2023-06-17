
from attr import define, field
from actions.create.base_create import BaseCreateCardEffect
from classes.gamestate import GameState
from enums.location import LocEnum


@define
class FillLocationWithCards(BaseCreateCardEffect):
    quantity: None = field(default=None, init=False)

    def resolve(self, gamestate: GameState):
        return super().resolve(gamestate)

@define
class FillHandWithCards(FillLocationWithCards):
    location: LocEnum = field(default=LocEnum.HAND, init=False)