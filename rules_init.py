from actions.movement.draw import DrawEffect
from actions.movement.summon import SummonEffect
from classes.rules import Rules
from enums.gamestate import GameStateEnums
from actions.attribute.set_attribute import SetAttribute
from actions.create.create_player import CreatePlayerAction
from enums.attribute import AttrEnum
from enums.gamestate import GameStateEnums
from enums.operator import Ops_
from resolvable_enums.target_player import TargetPlayer


create_player1 = CreatePlayerAction(10, 10, 10, 10, "")
create_player2 = CreatePlayerAction(10, 10, 10, 10, "")
draw_hand = DrawEffect(quantity=5, player=TargetPlayer.ALL_PLAYERS)

gain_mana_gem = SetAttribute(
    target=TargetPlayer.ALL_PLAYERS,
    attribute=AttrEnum.MANA_GEM,
    value=1,
)

rally_on_main_phase = SetAttribute(
    target=TargetPlayer.ALL_PLAYERS,
    attribute=AttrEnum.RALLY,
    value=True,
    operator=Ops_.SET
)
# playcard = PlayCard()


LORRules = Rules()
LORRules.add_phase(
    GameStateEnums.GAME_START,
    GameStateEnums.ROUND_START,
    [create_player1, create_player2, draw_hand],
)
LORRules.add_phase(
    GameStateEnums.ROUND_START,
    GameStateEnums.MAIN_PHASE,
    [gain_mana_gem, rally_on_main_phase],
)

