from actions.movement.recall import RecallEffect
from card_classes.skill import Skill
from resolvable_enums.auto_card_selector import AutoEntitySelector


def MoreThanYouCanChew():
    
    effect = RecallEffect(target=AutoEntitySelector.STRONGEST_OPPONENT_BOARD_UNIT)
    effect1 = RecallEffect(target=AutoEntitySelector.ALL_OPPONENT_UNITS)
    condition = OwnerCondition(
        condition=PlayerFlags.HAS_SPENT_X_MANA_THIS_ROUND, parameter=16
    )
    branch = BranchingAction(condition=condition, if_true=effect1, if_false=effect)
    return Skill(activation_effect=)