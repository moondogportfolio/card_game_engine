from attr import define
from actions.base_action import BaseAction
from classes.gamestate import GameState
from entity_classes.player import Player
from enums.location import LocEnum


@define
class CreateDeckEffect(BaseAction):
    owner: Player
    deckcode: str

    def resolve(self, gamestate: GameState):
        gamestate.entity_man.create_card('01NX007', LocEnum.HOMEBASE, self.owner, 40)