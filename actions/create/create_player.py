from typing import Tuple
from attr import define, field
from actions.base_action import BaseAction
from classes.gamestate import GameState
from entity_classes.player import Player

from enums.region import RegionEnum



@define
class CreatePlayerAction(BaseAction):
    health: int
    mana_gem: int
    spell_mana: int
    mana: int
    deckcode: str
    regions: Tuple[RegionEnum, RegionEnum] = field(default=False, init=False)
    rally: bool = field(default=False, init=False)
    target: None = field(init=False)

    def resolve(self, gamestate: GameState):
        player = gamestate.entity_man.create_player(
            health=self.health,
            mana=self.mana,
            mana_gem=self.mana_gem,
            spell_mana=10,
        )
        gamestate.entity_man.create_deck(
            deckcode="asd", player=player, gamestate=gamestate, cc=...
        )
        # gamestate.entity_man.add_player(player)
        return CreatePlayerEvent(created_player=player)

