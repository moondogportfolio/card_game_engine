from enum import Enum, auto
from typing import Any, Callable, Dict

from classes.gamestate import GameState
from custom_types.resolvables import ResolvableCondition


class CardFlags(Enum):
    IS_NON_CHAMPION = auto()
    IS_NEW_CARD = auto()
    IS_SPEEDTYPE = auto()
    HEALTH_REACHES_AMOUNT = auto()
    ATTACK_REACHES_AMOUNT = auto()
    ATTACKED_THIS_ROUND = auto()
    ALLEGIANCE = auto()
    IS_CARD_CLASS = auto()
    IS_STUNNED = auto()
    IS_ALLY = auto()
    IS_LURKER = auto()
    IS_ON_THE_BOARD = auto()
    IS_5_PLUS_POWER = auto()
    IS_ON_HAND = auto()
    IS_EQUIPMENT = auto()
    IS_EQUIPPED = auto()
    IS_FOLLOWER = auto()
    IS_IN_HAND = auto()
    IS_IN_HAND_OR_PLAY = auto()
    IS_DEAD = auto()  # means on the graveyard
    IS_DAMAGED = auto()
    IS_CHAMPION = auto()
    IS_MULTIREGION = auto()
    IS_CREATED = auto()
    IS_SUBTYPE_X = auto()
    HAS_KEYWORD = auto()
    HAS_COUNTDOWN = auto()
    HAS_ATTACHMENT = auto()
    HAS_FURY = auto()
    HAS_LASTBREATH = auto()
    HAS_MARK_OF_THE_STORM = auto()
    HAS_NIGHTFALL = auto()
    HAS_DAYBREAK = auto()
    FROM_YOUR_REGIONS = auto()

    def resolve(self):
        return tpdict[self]


def is_subtype(gamestate: GameState, origin, target, parameter):
	print(target, parameter)


def allegiance(gamestate: GameState, origin):
	...

def is_card_class(gamestate: GameState, origin):
	...

def is_stunned(gamestate: GameState, origin):
	...

def is_ally(gamestate: GameState, origin):
	...

def is_lurker(gamestate: GameState, origin):
	...

def is_on_the_board(gamestate: GameState, origin):
	...

def is_5_plus_power(gamestate: GameState, origin):
	...

def is_on_hand(gamestate: GameState, origin):
	...

def is_equipment(gamestate: GameState, origin):
	...

def is_equipped(gamestate: GameState, origin):
	...

def is_follower(gamestate: GameState, origin):
	...

def is_in_hand_or_play(gamestate: GameState, origin):
	...

def is_damaged(gamestate: GameState, origin):
	...

def is_champion(gamestate: GameState, origin):
	...

def is_multiregion(gamestate: GameState, origin):
	...

def is_created(gamestate: GameState, origin):
	...

def has_countdown(gamestate: GameState, origin):
	...

def has_attachment(gamestate: GameState, origin):
	...

def has_fury(gamestate: GameState, origin):
	...

def has_lastbreath(gamestate: GameState, origin):
	...

def has_mark_of_the_storm(gamestate: GameState, origin):
	...

def has_nightfall(gamestate: GameState, origin):
	...

def has_daybreak(gamestate: GameState, origin):
	...

def is_dead(gamestate: GameState, origin):
	...
def is_created(gamestate: GameState, target):
	...


tpdict: Dict[CardFlags, ResolvableCondition] = {
    CardFlags.ALLEGIANCE: allegiance,
    CardFlags.IS_CARD_CLASS: is_card_class,
    CardFlags.IS_STUNNED: is_stunned,
    CardFlags.IS_ALLY: is_ally,
    CardFlags.IS_LURKER: is_lurker,
    CardFlags.IS_ON_THE_BOARD: is_on_the_board,
    CardFlags.IS_5_PLUS_POWER: is_5_plus_power,
    CardFlags.IS_ON_HAND: is_on_hand,
    CardFlags.IS_EQUIPMENT: is_equipment,
    CardFlags.IS_EQUIPPED: is_equipped,
    CardFlags.IS_FOLLOWER: is_follower,
    CardFlags.IS_IN_HAND_OR_PLAY: is_in_hand_or_play,
    CardFlags.IS_DAMAGED: is_damaged,
    CardFlags.IS_CHAMPION: is_champion,
    CardFlags.IS_MULTIREGION: is_multiregion,
    CardFlags.IS_CREATED: is_created,
    CardFlags.HAS_COUNTDOWN: has_countdown,
    CardFlags.HAS_ATTACHMENT: has_attachment,
    CardFlags.HAS_FURY: has_fury,
    CardFlags.HAS_LASTBREATH: has_lastbreath,
    CardFlags.HAS_MARK_OF_THE_STORM: has_mark_of_the_storm,
    CardFlags.HAS_NIGHTFALL: has_nightfall,
    CardFlags.HAS_DAYBREAK: has_daybreak,
    CardFlags.IS_DEAD: is_dead,
    CardFlags.IS_SUBTYPE_X: is_subtype
}