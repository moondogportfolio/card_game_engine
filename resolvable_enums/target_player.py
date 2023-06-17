
from enum import Enum, auto
from typing import Any, Callable, Dict
from classes.gamestate import GameState

from entity_classes.player import Player



class TargetPlayer(Enum):
    ORIGIN_OWNER = auto()
    OPPONENT = auto()
    ALL_PLAYERS = auto()
    OUT_OF_TURN_PLAYER = auto()
    PLAYER_WITH_TURN = auto()

    def resolve(self, gamestate, origin, *args, **kwargs):
        return tpdict[self](gamestate, origin)


tpdict: Dict[TargetPlayer, Callable[[GameState, Any], Any]] = {
    TargetPlayer.ORIGIN_OWNER: lambda x, y: y.owner,
    TargetPlayer.OPPONENT: lambda x, y: x.entity_man.get_opponent(y.owner),
    TargetPlayer.ALL_PLAYERS: lambda x, y: x.entity_man.players,
    TargetPlayer.OUT_OF_TURN_PLAYER: lambda x, y: x.player_out_of_turn,
    TargetPlayer.PLAYER_WITH_TURN: lambda x, y: x.player_turn,
}