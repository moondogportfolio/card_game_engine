from enum import Enum, auto
from typing import Dict

from entity_selectors.card_filter import CardFilter, EntityFilter
from entity_selectors.target_game_card import TargetEntity
from enums.types import Types_
from resolvable_enums.target_player import TargetPlayer


class TargetShorthand(Enum):
    ANY_ALLIED_UNIT = auto()
    ALLIED_BOARD_UNIT = auto()
    ALLIED_BOARD_FOLLOWER = auto()
    ALLIED_HAND_UNIT = auto()
    EQUIPPED_ALLIED_UNIT = auto()
    ALLIED_HAND_CARD = auto()
    ALLIED_LANDMARK = auto()
    ALLIED_COUNTDOWN_LANDMARK = auto()
    ALLY_NEXUS_OR_BOARD_UNITS = auto()
    BATTLE_FIELD_ALLY_ONE = auto()
    HAND_EQUIPMENT = auto()
    ALLIED_STRONGEST_TENTACLE = auto()

    OPPONENT_BOARD_UNIT = auto()
    OPPONENT_BOARD_FOLLOWER = auto()
    OPPONENT_LANDMARK = auto()
    OPPONENT_LANDMARK_OR_BOARD_UNIT = auto()
    OPPONENT_NEXUS_OR_BOARD_UNITS = auto()
    EQUIPPED_OPPONENT_UNIT = auto()
    BATTLE_FIELD_OPPO_ONE = auto()

    ANY_BOARD_UNIT = auto
    ANY_LANDMARK = auto()
    ANY_BOARD_UNIT_OR_LANDMARK = auto()
    ANY_BOARD_FOLLOWER = auto()
    ANYTHING = auto()
    BOARD_ALL = auto()

    def get_longhand(self) -> CardFilter:
        return TargetEntity(choices=tpdict.get(self))


tpdict: Dict[TargetShorthand, CardFilter] = {
    TargetShorthand.ANYTHING: EntityFilter(owner=None, player=TargetPlayer.ALL_PLAYERS),
    TargetShorthand.BOARD_ALL: CardFilter(),
    TargetShorthand.BATTLE_FIELD_ALLY_ONE: CardFilter(),
    TargetShorthand.ANY_ALLIED_UNIT: CardFilter(),
    TargetShorthand.ALLIED_BOARD_UNIT: CardFilter(),
    TargetShorthand.ALLIED_HAND_UNIT: CardFilter(),
    TargetShorthand.OPPONENT_BOARD_UNIT: CardFilter(owner=TargetPlayer.OPPONENT),
    TargetShorthand.BATTLE_FIELD_OPPO_ONE: CardFilter(),
    TargetShorthand.ANY_BOARD_UNIT: CardFilter(owner=None),
    TargetShorthand.ALLIED_HAND_CARD: CardFilter(),
    TargetShorthand.ALLIED_LANDMARK: CardFilter(),
    TargetShorthand.HAND_EQUIPMENT: CardFilter(),
    TargetShorthand.OPPONENT_LANDMARK: CardFilter(
        owner=TargetPlayer.OPPONENT, type=Types_.LANDMARK
    ),
    TargetShorthand.ANY_LANDMARK: CardFilter(owner=None, type=Types_.LANDMARK),
    TargetShorthand.ANY_BOARD_FOLLOWER: CardFilter(owner=None, is_follower=True),
    TargetShorthand.ALLY_NEXUS_OR_BOARD_UNITS: EntityFilter(
        owner=TargetPlayer.ORIGIN_OWNER, player=TargetPlayer.ORIGIN_OWNER
    ),
    TargetShorthand.OPPONENT_LANDMARK_OR_BOARD_UNIT: CardFilter(),
    TargetShorthand.OPPONENT_NEXUS_OR_BOARD_UNITS: CardFilter(
        owner=TargetPlayer.OPPONENT
    ),
}
