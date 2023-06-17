
from enum import Enum, auto


class AutoEntitySelector(Enum):
    #EQUIPMENT/ATTACHMENT
    THIS_ATTACHMENT_BEARER = auto()
    THIS_EQUIPMENT_BEARER = auto()
    EQUIPMENT = auto()
    ATTACHMENT = auto()

    ALL_BOARD_UNITS = auto()
    ALL_ALLIED_UNITS = auto()
    ALL_OPPONENT_UNITS = auto()
    ALL_OPPONENT_FOLLOWERS = auto()
    ALL_STUNNED_OPPONENT_UNITS = auto()
    ANYTHING = auto()
    EVERYTHING = auto()
    OPPONENT_NEXUS_AND_BOARD_UNITS = auto()
    OWNER_NEXUS_AND_BOARD_UNITS = auto()
    ANY_BOARD_UNIT_OR_LANDMARK = auto()
    EQUIPPED_ALLIED_BOARD_UNIT = auto()
    SELF = auto()
    ORIGIN_AND_NEXUS = auto()
    ALLIED_STRONGEST_TENTACLE = auto()
    ORIGIN = auto()
    EFFECT_ORIGIN = auto()
    ALL_HAND_SPELLS = auto()
    STRONGEST_OPPONENT_BOARD_UNIT = auto()
    STRONGEST_BOARD_UNIT = auto()
    WEAKEST_OPPONENT_UNIT = auto()
    WEAKEST_ALLY = auto()
    TOP_ALLY_IN_DECK = auto()
    SKILL_ORIGIN_UNIT = auto()
    NAGAKABOUROS_MINIONS = auto()

    STRONGEST_DEAD_ALLY = auto()
    RANDOM_DEAD_ALLY = auto()

    def resolve(self, gamestate, origin):
        return tp_dict[self](gamestate, origin)

tp_dict = {
    AutoEntitySelector.SELF: lambda x, y: y
}