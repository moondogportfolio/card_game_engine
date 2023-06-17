# Rampaging Baccai and an enemy strike each other.
from actions.attribute.buff import BuffEffect
from actions.attribute.buff_everywhere import BuffEverywhereEffect
from actions.attribute.damage import DamageEffect
from actions.attribute.rally import RallyEffect
from actions.champ.level_up import LevelupEffect
from actions.common.strike import MutualStrikeEffect, StrikeEffect
from actions.create.create_card import CreateCardEffect
from actions.create.create_copy import CreateExactCopyEffect
from actions.keywords.add_keyword import AddKeywordEffect
from actions.keywords.stun_effect import StunEffect
from actions.movement.draw import DrawEffect
from actions.movement.kill import DestroyLandmarkEffect, KillAction
from actions.movement.obliterate import ObliterateEffect
from actions.movement.revive import ReviveEffect
from actions.movement.swap import SwapPositionsEffect
from actions.reactions.dynamic_attr_modifier import DynamicCostModifier
from card_classes.spell import Spell
from entity_selectors.base_card_filter import BaseCardFilter
from entity_selectors.card_filter import CardFilter
from entity_selectors.input import ChoiceBaseCard
from entity_selectors.target_game_card import TargetEntity
from enums.keywords import KeywordEnum
from enums.location import LocEnum
from enums.post_event_param import PostEventParam
from enums.types import Types_
from resolvable_enums.active_cards_selector import TargetShorthand
from resolvable_enums.auto_card_selector import AutoEntitySelector
import Sets.SET4.Units as Set4Units
import Sets.SET4.Champions as Set4Champions
from resolvable_enums.card_conditions import CardFlags
from resolvable_enums.target_player import TargetPlayer


def BaccaiRampage():
    effect = MutualStrikeEffect(
        first_striker=PostEventParam.SKILL_ORIGIN,
        second_striker=TargetShorthand.OPPONENT_BOARD_UNIT,
    )
    return Spell(activation_effect=effect)

def ShakenGround():
    ...

# Deal 1 to enemies and the enemy Nexus.
def CircuitBreaker():
    effect = DamageEffect(
        value=1, target=AutoEntitySelector.OPPONENT_NEXUS_AND_BOARD_UNITS
    )
    return Spell(activation_effect=effect)


# If you've slain 13+ units this game, kill all enemy followers, then summon a copy of me.
def ConservatorsJudgment():
    effect = KillAction(target=AutoEntitySelector.ALL_OPPONENT_FOLLOWERS)
    effect1 = CreateCardEffect(Set4Units.SanctumConservator, LocEnum.HOMEBASE)
    return Spell(activation_effect=(effect, effect1))


# Each Lurker ally strikes a random enemy.
def FrenziedFeast():
    effect = ...
    # TODO looper


# Kill an ally to kill an enemy.
def TheSecondDeath():
    effect = KillAction(target=TargetShorthand.ALLIED_BOARD_UNIT)
    effect1 = KillAction(
        target=TargetShorthand.OPPONENT_BOARD_UNIT, fizz_if_fail=effect
    )
    return Spell(activation_effect=(effect, effect1))


# Kill an ally to deal 3 to the enemy Nexus.
def SymmetryInStars():
    effect = KillAction(target=TargetShorthand.ALLIED_BOARD_UNIT)
    effect1 = DamageEffect(target=TargetPlayer.OPPONENT, value=3, fizz_if_fail=effect)
    return Spell(activation_effect=(effect, effect1))




# Summon an exact copy of an ally. It's Ephemeral.Draw 1.
def ShimmeringMirage():
    effect = CreateExactCopyEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT, is_ephemeral=True
    )
    effect1 = DrawEffect()
    return Spell(activation_effect=(effect, effect1))


# Obliterate 3 enemy units or landmarks.
def Sandstorm():
    effect = ObliterateEffect(
        target=TargetEntity(
            quantity=3,
            filter=CardFilter(
                owner=TargetPlayer.OPPONENT, type=(Types_.UNIT, Types_.LANDMARK)
            ),
        )
    )
    return Spell(activation_effect=effect)


# Obliterate an enemy follower.Draw 1.
def CrumblingSands():
    effect = ObliterateEffect(target=TargetShorthand.OPPONENT_BOARD_FOLLOWER)
    effect1 = DrawEffect()
    return Spell(activation_effect=(effect, effect1))


# Draw 2.
def EmperorsProsperity():
    effect = DrawEffect(quantity=2)
    return Spell(activation_effect=effect)


# Rally. Summon Renekton and Nasus. Immediately level them up to level 3.
def AscendedsCall():
    effect = RallyEffect()
    effect1 = CreateCardEffect(Set4Champions.Nasus, LocEnum.HOMEBASE)
    effect2 = CreateCardEffect(Set4Champions.Renekton, LocEnum.HOMEBASE)
    effect3 = LevelupEffect(target=..., new_form=Set4Champions.Nasus3)
    effect4 = LevelupEffect(target=..., new_form=Set4Champions.Renekton3)
    return Spell(activation_effect=(effect, effect1, effect2, effect3, effect4))


# Swap Irelia with an ally.
def Bladesurge():
    target_obj1 = TargetEntity(filter=CardFilter(card_class=Set4Champions.Irelia))
    target_obj2 = TargetEntity(exclusion=target_obj1)
    effect = SwapPositionsEffect(target=target_obj1, destination=target_obj2)
    return Spell(activation_effect=effect)


# Stun all enemies.
def UnstoppableForce():
    effect = StunEffect(target=AutoEntitySelector.ALL_OPPONENT_UNITS)
    return Spell(activation_effect=effect)


# Revive all allies that died this round, then Rally.
def Chronobreak():
    value = EventQueryParamGetter(
        query=EventQuery(event=EntityEvents.DIE, this_round=True),
        parameter=EventParameter.TARGET,
    )
    effect = ReviveEffect(target=value)
    effect1 = RallyEffect()
    return Spell(activation_effect=(effect, effect1))


# Summon Pyke striking an enemy.
def DeathFromBelow():
    effect = CreateCardEffect(Set4Champions.Pyke, LocEnum.HOMEBASE)
    effect1 = StrikeEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT,
        striker=PostEffectParamGetter(effect=effect, parameter=EventParameter.TARGET),
    )
    return Spell(activation_effect=(effect, effect1))


# Deal 2 to enemies and the enemy Nexus.
def DominusDestruction():
    effect = DamageEffect(
        value=2, target=AutoEntitySelector.OPPONENT_NEXUS_AND_BOARD_UNITS
    )
    return Spell(activation_effect=effect)


def RockSlide():
    effect = StunEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT)
    return Spell(activation_effect=effect)


# Stun the Strongest enemy.
def BlindingCrest():
    effect = StunEffect(target=AutoEntitySelector.STRONGEST_OPPONENT_BOARD_UNIT)
    return Spell(activation_effect=effect)


# Destroy a landmark. If it's allied, summon a Grumpy Rockbear.
def TeenSpirit():
    effect = DestroyLandmarkEffect(target=TargetShorthand.ANY_LANDMARK)
    effect1 = CreateCardEffect(
        target=Set4Units.GrumpyRockbear,
        location=LocEnum.HOMEBASE,
        condition=...,
    )
    return Spell(activation_effect=(effect, effect1))


# Deal 2 to Taliyah's blocker. If it's dead or gone, deal 2 to the enemy Nexus instead.
def ThreadedVolley():
    effect = DamageEffect(value=2, target=...)
    # TODO
