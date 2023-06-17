
from typing import Callable, Dict
from classes.gamestate import GameState
from resolvable_enums.target_player import TargetPlayer


tpdict: Dict[TargetPlayer, Callable[[None, GameState], None]] = {
    TargetPlayer.ORIGIN_OWNER: lambda x, y: x.owner,
    TargetPlayer.OPPONENT: lambda x, y: y.entity_man.get_opponent(x.owner),
    TargetPlayer.ALL_PLAYERS: lambda x, y: y.entity_man.players,
    'ORIGIN_OWNER': lambda x, y: x.owner,
    TargetPlayer.OUT_OF_TURN_PLAYER: lambda x, y: y.player_out_of_turn,
    TargetPlayer.PLAYER_WITH_TURN: lambda x, y: y.player_turn,
}

def target_player_resolver(target_player, origin, gamestate):
    return tpdict.get(target_player)(origin, gamestate)