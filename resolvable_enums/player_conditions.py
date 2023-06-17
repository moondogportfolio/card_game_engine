from __future__ import annotations
from enum import Enum, auto
from typing import TYPE_CHECKING, Callable, Dict
from classes.gamestate import GameState

from custom_types.resolvables import ResolvableCondition
from enums.location import LocEnum

if TYPE_CHECKING:
    from entity_selectors.card_filter import CardFilter


class PlayerFlags(Enum):
    LOCATION_HAS_SPACE = auto()
    HAS_PLAYED_A_6_COST_SPELL = auto()       
    IS_BEHOLDING_CELESTIAL = auto()
    LURK = auto()
    SCOUT = auto()
    DAYBREAK = auto()
    NIGHTFALL = auto()
    PLUNDER = auto()
    PHASED = auto()
    ENLIGHTENED = auto()
    DEEP = auto()
    EVOLVED = auto()
    REPUTATION = auto()
    FLOW = auto()
    HAS_X_CARDS_ON_Y_LOC = auto()
    HAS_ATTACK_TOKEN = auto()
    HAS_LEVELED_CHAMP_THIS_GAME = auto()
    HAS_LEVELED_CHAMP_X_THIS_GAME = auto()
    HAS_SUMMONED_LANDMARK_THIS_GAME = auto()
    HAS_SPENT_X_MANA_THIS_ROUND = auto()
    HAS_SUPPORTED_THIS_GAME = auto()
    HAS_NO_X_HAND_CARD = auto()
    HAS_EQUIPPED_ALLY_THIS_GAME = auto()
    ALLY_DIED_THIS_ROUND = auto()
    ADDED_CARDS_TO_HAND = auto() #TODO
    HAS_X_BOARD_ALLIES = auto()
    HAS_CREATED_X_CARDS = auto()
    HAS_PLAYED_X_DIFF_NAMED_CARDS = auto()
    HAS_SLAIN_UNIT_THIS_ROUND = auto()
    HAS_PLAYED_6_PLUS_NEW_CARDS =auto()
    IS_OWNER = auto()
    HAS_X_CARD_IN_PLAY = auto()
    HAS_PLAYED_CARDS_FROM_DIFF_REGIONS = auto()
    HAS_SUMMONED_UNITS_FROM_X_REGIONS = auto()
    DEALT_DAMAGE_TO_NEXUS_X_TIMES = auto()
    HAS_ADDED_CARDS_TO_HAND_THIS_ROUND = auto()
    HAS_DESTROYED_X_LANDMARKS = auto()
    HAS_CARD_X_ON_BOARD = auto()
    IS_BEHOLDING_8_COST_CARD = auto()
    IS_BEHOLDING_CELESTIAL_CARD = auto()
    HAS_UNIT_ON_BOARD = auto()
    IS_BEHOLDING_X_CARD = auto()
    IS_BEHOLDING_DRAGON = auto()
    ACTIVATED_TRAP_OR_BOON_THIS_ROUND = auto()

    def resolve(self):
        return tpdict[self]
    

def has_x_board_allies(gamestate: GameState, origin, player, count: int, strict = False):
    return True

def location_has_space(gamestate: GameState, origin, location: LocEnum):
    return gamestate.loc_man.get_location_obj(location, player=origin.owner).is_full()


def has_card_x_on_board(gamestate: GameState, origin, player, card_filter: CardFilter):
    for card in gamestate.loc_man.get_cards(LocEnum.BOARD, player):
        if card_filter.card_satisfies_filter(card):
            return True
    return False

def ally_died_this_round(gamestate: GameState, origin, player, quantity: int):
    return True


tpdict: Dict[PlayerFlags, ResolvableCondition] = {
    PlayerFlags.HAS_X_BOARD_ALLIES: has_x_board_allies,
    PlayerFlags.LOCATION_HAS_SPACE: location_has_space,
    PlayerFlags.HAS_CARD_X_ON_BOARD: has_card_x_on_board,
    PlayerFlags.ALLY_DIED_THIS_ROUND: ally_died_this_round
    }