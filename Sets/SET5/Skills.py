"""
UNIT SPELL
"""


from actions.attribute.damage import DamageEffect
from actions.movement.kill import DestroyLandmarkEffect
from actions.movement.recall import RecallEffect
from actions.traps.set_trap import PlantFlashBombTrap
from card_classes.spell import Spell
from resolvable_enums.active_cards_selector import TargetShorthand
from resolvable_enums.target_player import TargetPlayer


# Deal 1 to the enemy Nexus.
def FerrosDividend():
    val = EventQueryInstances(
        query=EventQuery(event=EntityEvents.ACTIVATE_6_PLUS_COST_SPELL)
    )
    effect = DamageEffect(value=val, target=TargetPlayer.OPPONENT)
    return Spell(activation_effect=effect)


# Play: Activate the effects of all traps in the top 5 cards of the enemy deck.
def VolatileBloom():
    ...
    # TODO Activate the effects of all Keyword Trap.svg traps in the top 5 cards of the enemy deck.
    return Spell(activation_effect=effect)


# Play: Plant 5 Flashbomb Traps randomly in the top 5 cards of the enemy deck.
def BeguilingBlossom():
    effect = PlantFlashBombTrap(
        quantity=5,
        top_x_cards=5,
    )
    return Spell(activation_effect=effect)


# Recall a unit.
def Gust():
    effect = RecallEffect(target=TargetShorthand.ANY_BOARD_UNIT)
    return Spell(activation_effect=effect)


# Destroy an allied landmark to deal 3 to anything.
def InspectionPassed():
    effect = DestroyLandmarkEffect(target=TargetShorthand.ALLIED_LANDMARK)
    effect1 = DamageEffect(value=3, target=TargetShorthand.ANYTHING, fizz_if_fail=effect)
    return Spell(activation_effect=effect)


# Grant an enemy Mark of the Storm.
# If they already have it, remove the mark to Stun and deal 2 to them instead.
def MarkoftheStorm():
    target_obj = TargetGameCard(choices=TargetShorthand.OPPONENT_BOARD_UNIT)
    effect1 = AddFlag(target=target_obj, flag=CardFlags.MARK_OF_THE_STORM)
    effect2 = DamageEffect(value=3, target=target_obj)
    effect3 = StunEffect(target=target_obj)
    effect4 = BundledEffect(effects=[effect2, effect3])
    effect = BranchingEffect(
        branching_condition=Condition(
            target=target_obj, condition=CardFlags.HAS_MARK_OF_THE_STORM
        ),
        if_true=effect1,
        if_false=effect4,
    )
    return Spell(activation_effect=effect)


# Give your allies +2|+0 and Quick Attack this round. 
# If they already have it or Double Attack, give them a random keyword instead.
def AccelerationGate():
    value = BranchingValue(
        condition=Condition(
            target=...,
            condition=PlayerFlags.HAS_KEYWORD,
            parameter=[KeywordEnum.QUICKSTRIKE, KeywordEnum.DOUBLESTRIKE],
        ),
        if_true=KeywordEnum.RANDOM_KEYWORD,
        if_false=KeywordEnum.QUICKSTRIKE,
    )
    effect = BuffEffect(target=CardFilter(), round_only=True, attack=2, keyword=value)
    return Spell(activation_effect=effect)


# Deal 2 to Ziggs' blocker and the enemy Nexus.
def ShortFuse():
    effect = DamageEffect(target=TargetPlayer.OPPONENT, value=1)
    effect1 = DamageEffect(
        target=DerivedValue(
            target=TargetShorthand, evaluator=DerivingFunction.GET_BLOCKER
        ),
        value=1,
    )
    return Spell(activation_effect=(effect, effect1))


# class ShortFuse2(Spell):
#     _cardcode = "05BC163T5"

#     def __init__(self, **kwargs) -> None:
#         super().__init__(**kwargs)
#         effect = DamageEffect(target=TargetPlayer.OPPONENT, value=2)
#         effect1 = DamageEffect(
#             target=DerivedValue(
#                 target=TargetShorthand, evaluator=DerivingFunction.GET_BLOCKER
#             ),
#             value=2,
#         )
