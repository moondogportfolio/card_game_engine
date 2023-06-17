from actions.attribute.damage import DamageEffect
from actions.attribute.drain import DrainEffect
from actions.branching.branching_action import BranchingAction
from actions.common.strike import StrikeEffect
from actions.keywords.stun_effect import StunEffect
from actions.movement.kill import DestroyLandmarkEffect
from actions.movement.recall import RecallEffect
from actions.traps.set_trap import PlantFlashBombTrap
from card_classes.spell import Spell
from conditions.base_condition import Condition
from entity_selectors.card_filter import CardFilter
from entity_selectors.target_game_card import TargetEntity
from enums.post_event_param import PostEventParam
from resolvable_enums.active_cards_selector import TargetShorthand
from resolvable_enums.auto_card_selector import AutoEntitySelector
from resolvable_enums.player_conditions import PlayerFlags
from resolvable_enums.target_player import TargetPlayer


# Deal 4 to all Stunned enemies and the enemy Nexus.
def CurtainCall():
    effect = DamageEffect(
        target=AutoEntitySelector.ALL_STUNNED_OPPONENT_UNITS,
        target_player=TargetPlayer.OPPONENT,
        value=4,
    )
    return Spell(activation_effect=effect)


# Deal 2 to all Stunned enemies.
def DeadlyFlourish():
    effect = DamageEffect(target=AutoEntitySelector.ALL_STUNNED_OPPONENT_UNITS, value=2)
    return Spell(activation_effect=effect)


# Deal 1 to all enemies. If you've played 6+ new spells this game, deal 3 instead.
def FatalEncore():
    value = BranchingValue(
        condition=PlayerFlags.HAS_PLAYED_6_PLUS_NEW_CARDS, if_true=3, if_false=1
    )
    effect = DamageEffect(
        target=CardFilter(owner=TargetPlayer.OPPONENT),
        value=value,
    )
    return Spell(activation_effect=effect)


# Camouflaged Horror strikes an enemy.
def FeedtheVoid():
    effect = StrikeEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT,
        striker=PostEventParam.SKILL_ORIGIN,
    )
    return Spell(activation_effect=effect)


# Deal 2 to an enemy.
def KashuriGauntlet():
    effect = DamageEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT, value=2)
    return Spell(activation_effect=effect)


# Deal 1 to the enemy Nexus. If Jhin is in play, Stun the weakest enemy.
def LotusTrap():
    effect = DamageEffect(target=TargetPlayer.OPPONENT, value=1)
    effect1 = StunEffect(
        target=AutoEntitySelector.WEAKEST_OPPONENT_UNIT,
        condition=Condition(
            target=TargetPlayer.ORIGIN_OWNER,
            condition=PlayerFlags.HAS_X_CARD_IN_PLAY,
            parameter=Set6Champions.Jhin,
        ),
    )
    return Spell(activation_effect=effect)


# Deal 1 to the enemy Nexus.
def MagicEmbers():
    effect = DamageEffect(target=TargetPlayer.OPPONENT, value=1)
    return Spell(activation_effect=effect)


# Deal 3 and Stun Annie's blocker. If it's dead or gone, deal 3 to the enemy Nexus instead.
def MoltenShield():
    effect = DamageEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT, value=2)
    self.add_effect(effect)


# Deal 3 and Stun Annie's blocker. If it's dead or gone, deal 3 to the enemy Nexus instead.
def MoltenShield():
    effect1 = BranchingValue(condition=..., if_true=..., if_false=...)
    effect = DamageEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT, value=3)
    self.add_effect(effect)
    # blocker


# Deal 3 to Captive Greyback's blocker. If it's dead or gone, deal 3 to the enemy Nexus instead.
def ObeyedOrder():
    effect = StunEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT)
    self.add_effect(effect)


# Recall a unit with less Power than me.
def PeerlessArtistry():
    value = EntityAttribute(
        target=TargetShorthand.SKILL_ORIGIN_UNIT, attribute=Attr_.ATTACK
    )
    effect = RecallEffect(
        target=TargetEntity(
            choices=CardFilter(owner=TargetPlayer.OPPONENT, attack=(0, value - 1))
        )
    )
    return Spell(activation_effect=effect)


# Deal 1 to the enemy nexus.
def PiercingBolt():
    effect = DamageEffect(target=TargetPlayer.OPPONENT, value=1)
    return Spell(activation_effect=effect)


# Stun an enemy, then deal 2 to all Stunned or damaged enemies.
def PyroclasticArrival():
    effect2 = AcquireTargetEffect(choices=TargetShorthand.OPPONENT_BOARD_UNIT)
    effect = StunEffect(target=effect2)
    effect = DamageEffect(
        target=CardFilter(
            owner=TargetPlayer.OPPONENT,
            flags=(CardFlags.IS_STUNNED, CardFlags.IS_DAMAGED),
        ),
        value=2,
    )
    return Spell(activation_effect=effect)


# Stun an enemy.
def ScintillatingArtifact():
    effect = StunEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT)
    return Spell(activation_effect=effect)


# Drain 1 from the enemy Nexus one time for every 2 power Gwen has. (max 50 times)
def SnipSnipSnip():
    value = EntityAttribute(
        target=TargetShorthand.SKILL_ORIGIN_UNIT, attribute=Attr_.ATTACK
    )
    effect = DrainEffect(target=TargetPlayer.OPPONENT, value=value)
    self.add_effect(effect)


# Drain 2 from the enemy Nexus.
def SnipSnip():
    effect = DrainEffect(target=TargetPlayer.OPPONENT, value=2)
    return Spell(activation_effect=effect)


# Stun an enemy or if it's already Stunned deal 2 to it instead.
def StiffenedSinews():
    effect2 = AcquireTargetEffect(choices=TargetShorthand.OPPONENT_BOARD_UNIT)
    effect = StunEffect(target=effect2)
    effect1 = DamageEffect(target=effect2, value=2)
    effect3 = BranchingAction(
        branching_condition=Condition(target=effect2, condition=CardFlags.IS_STUNNED),
        if_true=effect,
        if_false=effect1,
    )
    return Spell(activation_effect=effect3)


# Stun an enemy.
def StunningPerformance():
    effect = StunEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT)
    return Spell(activation_effect=effect)
