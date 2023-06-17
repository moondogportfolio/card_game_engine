from enum import Enum, auto


class PlayerStatistic(Enum):
    UNIQUE_NAMES_PLAYED = auto()
    ALLIED_LANDMARKS_DESTROYED = auto()
    EPHEMERALS_SUMMONED = auto()
    SPELL_CAST_THIS_GAME = auto()
    ALLY_DIED_THIS_GAME = auto()
    ALLY_DIED_THIS_ROUND = auto()
    ALLY_ATTACKED_THIS_GAME = auto()
    CARD_DREW_LAST_ROUND = auto()
    CARD_DREW_THIS_GAME = auto()
    ACTIVATED_NIGHTFALL = auto()
    PLAYED_CELESTIAL_CARDS = auto()
    FROSTBITTEN_ENEMIES = auto()
    UNIQUE_SUBTYPES_SUMMONED = auto()
    DISTINCT_ROUNDS_DAMAGE_OPPO_NEXUS = auto()
    BARKEEP_SUMMONED = auto()
    STUNNED_OR_RECALLED = auto()
    # EventQuery(
    #         event=EntityEvents.DAMAGE,
    #         param_getter=EventQueryParamGetter.DISTINCT_ROUNDS,
    #     )

    def resolve(self, *args, **kwargs):
        return 1