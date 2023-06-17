from random import choice

from actions.movement.steal import StealEffect
import Sets.SET1.Units as Set1Units
import Sets.SET1.Spells as Set1Spells
import Sets.SET2.Spells as Set2Spells
import Sets.SET2.Units as Set2Units
import Sets.SET3.Units as Set3Units
import Sets.SET3.Spells as Set3Spells
import Sets.SET4.Skills as Set4Skills

import Sets.SET4.Spells as Set4Spells
import Sets.SET4.Units as Set4Units
import Sets.SET5.Units as Set5Units
import Sets.SET4.Landmarks as Set4Landmarks
import Sets.SET5.Landmarks as Set5Landmarks
import Sets.SET5.Champions as Set5Champions
import Sets.SET5.Spells as Set5Spells

import Sets.SET6.Units as Set6Units
import Sets.SET6.Champions as Set6Champions

import Sets.SET6.Equipments as Set6Equipments
from actions.action_modifiers.silence import SilenceEffect
from actions.activations.copy_spell import CopySpellWithSameTargets
from actions.activations.multiple_activations import MultipleActivationsEffect
from actions.activations.negate_spell import NegateSpell
from actions.activations.play_skill import PlaySkill
from actions.activations.recast_spell import RecastEventOfAction
from actions.attachments.destroy import DestroyAttachmentsEffect, DestroyEquipEffect
from actions.attachments.equip import EquipEffect
from actions.attachments.forge import ForgeEffect
from actions.attachments.improvise import ImproviseEffect
from actions.attachments.transfer_equip import TransferEquipmentEffect
from actions.attachments.unequip import UnequipEffect
from actions.attack.challenge import ChallengeEffect
from actions.attack.free_attack import FreeAttackEffect
from actions.attack.overwhelm_effect import OverwhelmEffect
from actions.attribute.buff import BuffCostEffect, BuffEffect
from actions.attribute.buff_everywhere import BuffEverywhereEffect
from actions.attribute.countdown import AdvanceCountdownEffect
from actions.attribute.damage import DamageEffect
from actions.attribute.destroy_mana_gem import DestroyManaGem
from actions.attribute.drain import DrainEffect
from actions.attribute.frostbite import FrostbiteEffect
from actions.attribute.gain_mana_gem import GainManaGemEffect
from actions.attribute.heal import HealEffect
from actions.attribute.phase import PhaseMoonWeaponEffect
from actions.attribute.rally import RallyEffect
from actions.attribute.refill_mana import RefillManaEffect, RefillSpellMana
from actions.attribute.reveal import RevealEffect
from actions.attribute.set_attribute import SetAttribute
from actions.branching.branching_action import BranchingAction
from actions.champ.level_up import LevelupEffect
from actions.combination_action import CombinationAction
from actions.common.strike import MutualStrikeEffect, StrikeEffect
from actions.create.bladedance import BladedanceEffect

from actions.create.create_card import CreateCardEffect
from actions.create.create_copy import CreateExactCopyEffect
from actions.create.create_hand_cards import ReforgeEffect
from actions.create.fill_location import FillHandWithCards
from actions.create.invoke import InvokeEffect
from actions.create.manifest import ManifestEffect
from actions.create.post_events import CreatePostActParams
from actions.create.replace_deck import ReplaceDeck
from actions.create.summon_specific_cards import SpawnEffect, SummonHuskEffect
from actions.keywords.add_keyword import AddKeywordEffect, AddRandomKeywordEffect
from actions.create.tellstones import TellstonesEffect
from actions.keywords.copy_keywords import CopyKeywords
from actions.keywords.remove_keyword import (
    PurgeKeywordsEffect,
    RemoveKeywordEffect,
)
from actions.keywords.stun_effect import StunEffect
from actions.meta.create_ta import CreateTriggeredAction
from actions.movement.capture import CaptureEffect
from actions.movement.discard import DiscardEffect
from actions.movement.draw import (
    DrawEffect,
    DrawSpecificReturnRestEffect,
    TargetedDrawAction,
)
from actions.movement.kill import DestroyLandmarkEffect, KillAction
from actions.movement.move import MoveEffect
from actions.movement.nba import NabEffect
from actions.movement.obliterate import ObliterateEffect
from actions.movement.predict import PredictEffect
from actions.movement.recall import RecallEffect
from actions.movement.revive import ReviveEffect
from actions.movement.summon import SummonEffect
from actions.movement.toss import TossEffect
from actions.postevent import PostEventParamGetter
from actions.reactions.action_modifier import ActionModifier
from actions.reactions.action_negator import ActionNegator
from actions.reactions.action_replacement import ActionReplacement
from actions.reactions.dynamic_attr_modifier import (
    DynamicAtkHPModifier,
    DynamicAttackModifier,
    DynamicCostModifier,
    DynamicKeywordModifier,
)
from actions.reactions.event_filter import EventFilter
from actions.reactions.triggered_action import AllyOrigin_TA, TriggeredAction
from actions.reactions.value_triggered_action import (
    EventCounterEnum,
    ValueTriggeredAction,
)
from actions.requisite.action_requisite import ActionRequisite
from actions.transform.transform import TransformEffect
from actions.traps.set_trap import (
    ActivateBoons,
    PlantChimes,
    PlantFlashBombTrap,
    PlantMysteriousPortalEffect,
    PlantPuffcaps,
    SetTrapEffect,
    TrapMultiplier,
)
from card_classes.champion import Champion
from card_classes.spell import Spell
from card_classes.unit import Unit
from conditions.base_condition import Condition
from entity_selectors.base_card_filter import (
    BaseCardFilter,
    InvokeBaseCardFilter,
    ManifestBaseCardFilter,
)
from entity_selectors.card_filter import (
    BeholdingFilter,
    CardFilter,
    DrawCardFilter,
    EntityFilter,
    StackSpellFilter,
)
from entity_selectors.input import ChoiceAction, ChoiceBaseCard, Input
from entity_selectors.target_game_card import TargetEntity
from entity_selectors.target_player import TargetPlayerInput
from enums.attribute import AttrEnum
from enums.card_sorters import CardSorter
from enums.counters import TrapEnums
from enums.deck_archetypes import DeckArchetypes
from enums.entity_events import EntityEvents
from enums.entity_pools import EntityPool
from enums.keywords import KeywordEnum
from enums.gamestate import GameStateEnums
from enums.location import LocEnum
from enums.operator import Ops_
from enums.origin_enum import OriginEnum
from enums.post_event_param import PostEventParam
from enums.spell_speed import SpellSpeedEnum
from enums.subtypes import SubTypes_
from enums.types import Types_
from events.event_query import EventQuery
from events.event_query_enum import EventQueryParamGetter, EventQueryTimeframe
from resolvable_enums.active_cards_selector import TargetShorthand
from resolvable_enums.auto_card_selector import AutoEntitySelector
from resolvable_enums.card_conditions import CardFlags
from resolvable_enums.player_conditions import PlayerFlags
from resolvable_enums.target_player import TargetPlayer
from value.branching_value import BranchingValue
from value.card_counter import CardCounter
from value.entity_attribute import EntityAttribute


# When I'm summoned or Round Start: If you have the attack token, create an Unstoppable Force in hand.
def Malphite():
    effect = PlaySkill(target=Set4Skills.RockSlide)
    create = CreateCardEffect(target=Set4Spells.UnstoppableForce)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.LEVEL_UP,
        action=create,
        activate_once=True,
        ally_enum=OriginEnum.T_SELF,
        condition=PlayerFlags.HAS_ATTACK_TOKEN,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Malphite2)
    levelwatcher = ValueTriggeredAction(
        event_filter=EntityEvents.SUMMON_LANDMARK,
        threshold=10,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        instance_bound=False,
        event_counter=...,
    )
    return Champion(
        play_effect=effect,
        effects=[ta1, levelwatcher],
        cardcode="04MT008",
        champion_spell=Set3Spells.PaleCascade,
    )


def Malphite2():
    effect = PlaySkill(target=Set4Skills.RockSlide)
    create = CreateCardEffect(target=Set4Spells.UnstoppableForce)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=create,
        ally_enum=OriginEnum.T_SELF,
        condition=PlayerFlags.HAS_ATTACK_TOKEN,
    )
    ta2 = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START,
        action=create,
        condition=PlayerFlags.HAS_ATTACK_TOKEN,
    )
    return Champion(
        play_effect=effect,
        effects=[ta1, ta2],
        cardcode="04MT008T1",
        champion_spell=Set4Spells.GroundSlam,
    )


def Nasus():
    # TODO i have for every
    dynamic = DynamicAtkHPModifier(value_attack=1, value_health=1)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Nasus2)
    watcher = TriggeredAction(
        event_filter=EntityEvents.STRIKE,
        ally_enum=OriginEnum.S_STRIKER,
        action=levelup,
        condition=...,
    )
    return Champion(
        effects=[watcher, dynamic],
        cardcode="04SH047",
        champion_spell=Set4Spells.SiphoningStrike,
    )


# I have +1|+1 for each unit you've slain this game. Enemies have -3|-0.
def Nasus2():
    dynamic = DynamicAtkHPModifier(value_attack=1, value_health=1)
    dynamic_debuff = DynamicAttackModifier(
        value=-1, target=AutoEntitySelector.ALL_OPPONENT_UNITS
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Nasus3)
    watcher = TriggeredAction(
        event_filter=EntityEvents.SUNDISC_RESTORED,
        ally_enum=OriginEnum.T_ALLY,
        action=levelup,
    )
    return Champion(
        effects=[watcher, dynamic, dynamic_debuff],
        cardcode="04SH047T3",
        champion_spell=Set4Spells.SiphoningStrike,
    )


def Nasus3():
    dynamic = DynamicAtkHPModifier(value_attack=1, value_health=1)
    dynamic_debuff = DynamicAttackModifier(
        value=-3, target=AutoEntitySelector.ALL_OPPONENT_UNITS
    )
    return Champion(
        effects=[dynamic, dynamic_debuff],
        cardcode="04SH047T2",
        champion_spell=Set4Spells.SiphoningStrike,
    )


def JarvanIV():
    effect1 = ...  # PAYCOST
    effect2 = SummonEffect(target=AutoEntitySelector.SELF)
    effect3 = ChallengeEffect(target=AutoEntitySelector.STRONGEST_OPPONENT_BOARD_UNIT)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.PLAYER_ATTACK_COMMIT,
        action=[effect1, effect2, effect3],
        ally_enum=OriginEnum.T_ALLY,
        condition=...,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=JarvanIV2)
    levelwatcher = ValueTriggeredAction(
        event_filter=EntityEvents.DAMAGE_SURVIVE,
        threshold=3,
        action_on_value=levelup,
        ally_enum=OriginEnum.O_ALLY,
        instance_bound=False,
        condition=...,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(
        effects=[ta1, levelwatcher],
        cardcode="04DE008",
        champion_spell=Set4Spells.Cataclysm,
    )


# When you attack, pay my cost to summon me Challenging the strongest enemy.
# Round Start: Create a Fleeting Cataclysm in hand.
# When I Challenge an enemy, give me Barrier this round.
def JarvanIV2():
    create = CreateCardEffect(target=Set4Spells.Cataclysm, is_fleeting=True)
    add_keyword = AddKeywordEffect(
        target=AutoEntitySelector.SELF, keyword=KeywordEnum.BARRIER
    )
    ta1 = TriggeredAction(
        event_filter=EntityEvents.CHALLENGE,
        action=add_keyword,
        ally_enum=OriginEnum.T_SELF,
        condition=...,
    )
    effect1 = ...  # PAYCOST
    effect2 = SummonEffect(target=AutoEntitySelector.SELF)
    effect3 = ChallengeEffect(target=AutoEntitySelector.STRONGEST_OPPONENT_BOARD_UNIT)
    ta2 = TriggeredAction(
        event_filter=EntityEvents.PLAYER_ATTACK_COMMIT,
        action=[effect1, effect2, effect3],
        ally_enum=OriginEnum.T_ALLY,
        condition=...,
    )
    return Champion(
        round_start_effects=create,
        effects=[ta1, ta2],
        cardcode="04DE008T2",
        champion_spell=Set4Spells.Cataclysm,
    )


def Viego():
    create = CreateCardEffect(Set4Units.EncroachingMist, location=LocEnum.HOMEBASE)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.DIE,
        action=create,
        ally_enum=OriginEnum.T_ALLY,
        activations_per_round=1,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Viego2)
    levelwatcher = ValueTriggeredAction(
        event_filter=EntityEvents.DIE,
        threshold=20,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        event_counter=...,
    )
    return Champion(
        effects=[ta1, levelwatcher],
        cardcode="04SI055",
        champion_spell=Set4Spells.Despair,
    )


def ViegoStealEffect():
    if ...:
        return KillAction(target=AutoEntitySelector.STRONGEST_OPPONENT_BOARD_UNIT)
    else:
        return StealEffect(target=...)


# Each round, the first time a unit dies, summon an Encroaching Mist.
# Round Start: Steal the strongest enemy this round. If it's a champion, kill it instead.
def Viego2():
    create = CreateCardEffect(Set4Units.EncroachingMist, location=LocEnum.HOMEBASE)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.DIE,
        action=create,
        ally_enum=OriginEnum.T_ALLY,
        activations_per_round=1,
    )
    # TODO distribute
    return Champion(
        round_start_effects=ViegoStealEffect,
        effects=ta1,
        cardcode="04SI055T2",
        champion_spell=Set4Spells.Despair,
    )


# When allies attack, summon an attacking Sand Soldier.When you summon an ally, give us both +1|+0 this round.
def Azir():
    create = CreateCardEffect(Set4Units.SandSoldier, LocEnum.BATTLEFIELD)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.PLAYER_ATTACK_COMMIT,
        ally_enum=OriginEnum.T_ALLY,
        action=create,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Azir2)
    # TODO multi
    levelwatcher = ValueTriggeredAction(
        event_filter=EntityEvents.SUMMON,
        threshold=13,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        condition=...,
        instance_bound=False,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(
        nexus_strike_effect=create,
        effects=[ta1, levelwatcher],
        cardcode="",
        champion_spell=Set4Spells.Arise,
    )


def Azir2():
    create = CreateCardEffect(Set4Units.SandSoldier, LocEnum.BATTLEFIELD)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.PLAYER_ATTACK_COMMIT,
        ally_enum=OriginEnum.T_ALLY,
        action=create,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Azir2)
    buff1 = BuffEffect(target=AutoEntitySelector.SELF, attack=1, round_only=True)
    buff2 = BuffEffect(target=PostEventParam.TARGET, attack=1, round_only=True)
    ta2 = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        action=[buff1, buff2],
    )
    watcher = TriggeredAction(
        event_filter=EntityEvents.SUNDISC_RESTORED,
        ally_enum=OriginEnum.T_ALLY,
        action=levelup,
    )
    return Champion(
        effects=[ta1, ta2, watcher],
        cardcode="",
        champion_spell=Set4Spells.Arise,
    )


def Azir3():
    # TODO replace deck
    # cards = {
    #         Set4Spells.CrumblingSands: 1,
    #         Set4Spells.ShimmeringMirage: 1,
    #         Set4Spells.EmperorsProsperity: 2,
    #         Set4Spells.Sandstorm: 1,
    #         Set4Units.EmperorsGuard: 4,
    #         Set4Units.GoldenHerald: 2,
    #         Set4Units.EternalGladiator: 2,
    #         Set4Landmarks.GeneralsPalace: 1,
    #     }
    create = CreateCardEffect(Set4Units.SandstoneCharger, LocEnum.BATTLEFIELD)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.PLAYER_ATTACK_COMMIT,
        ally_enum=OriginEnum.T_ALLY,
        action=create,
    )
    effect = DrawEffect()
    effect1 = ...
    ta2 = TriggeredAction(
        event_filter=EntityEvents.LEVEL_UP,
        action=[effect, effect1],
        activate_once=True,
        ally_enum=OriginEnum.T_SELF,
    )
    return Champion(
        effects=[ta1, ta2],
        cardcode="",
        champion_spell=Set4Spells.Arise,
    )


# Attack: Give me +3|+3 this round.
def Renekton():
    buff = BuffEffect(
        target=AutoEntitySelector.SELF, attack=2, health=1, round_only=True
    )
    ta1 = TriggeredAction(
        event_filter=EntityEvents.CHALLENGE,
        action=buff,
        ally_enum=OriginEnum.T_SELF,
        condition=...,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Renekton2)
    levelwatcher = ValueTriggeredAction(
        event_filter=EntityEvents.DAMAGE,
        threshold=10,
        action_on_value=levelup,
        ally_enum=OriginEnum.O_SELF,
        event_counter=EventCounterEnum.COUNT_VALUE,
    )
    return Champion(
        effects=[ta1, levelwatcher],
        cardcode="04SH067T1",
        champion_spell=Set4Spells.RuthlessPredator,
    )


def Renekton2():
    buff = BuffEffect(
        target=AutoEntitySelector.SELF, attack=3, health=3, round_only=True
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Renekton3)
    watcher = TriggeredAction(
        event_filter=EntityEvents.SUNDISC_RESTORED,
        ally_enum=OriginEnum.T_ALLY,
        action=levelup,
    )

    return Champion(
        attack_commit_effect=buff,
        effects=watcher,
        cardcode="04SH067T1",
        champion_spell=Set4Spells.RuthlessPredator,
    )


def Renekton3():
    effect = PlaySkill(target=Set4Spells.DominusDestruction)
    watcher = TriggeredAction(
        event_filter=EntityEvents.BLOCK,
        ally_enum=OriginEnum.O_SELF,
        action=effect,
    )
    return Champion(
        attack_commit_effect=effect,
        effects=watcher,
        cardcode="04SH067T2",
        champion_spell=Set4Spells.RuthlessPredator,
    )


# When I'm summoned or Round Start: If you have the attack token, create a Flawless Duet in hand.
# When allies attack, create a Bladesurge in hand.
def Irelia():
    effect = CreateCardEffect(Set4Spells.FlawlessDuet)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
        condition=PlayerFlags.HAS_ATTACK_TOKEN,
    )
    ta2 = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START,
        action=effect,
        condition=PlayerFlags.HAS_ATTACK_TOKEN,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Irelia2)
    levelwatcher = ValueTriggeredAction(
        event_filter=EntityEvents.ATTACK_COMMIT,
        threshold=14,
        action_on_value=levelup,
        ally_enum=OriginEnum.O_ALLY,
        instance_bound=False,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(
        effects=[ta1, ta2, levelwatcher],
        cardcode="04IO005T2",
        champion_spell=Set4Spells.VanguardsEdge,
    )


def Irelia2():
    effect = CreateCardEffect(Set4Spells.FlawlessDuet)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
        condition=PlayerFlags.HAS_ATTACK_TOKEN,
    )
    ta2 = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START,
        action=effect,
        condition=PlayerFlags.HAS_ATTACK_TOKEN,
    )
    effect1 = CreateCardEffect(Set4Spells.FlawlessDuet)
    ta3 = TriggeredAction(
        event_filter=EntityEvents.PLAYER_ATTACK_COMMIT,
        ally_enum=OriginEnum.T_ALLY,
        action=effect1,
    )
    return Champion(
        effects=[ta1, ta2, ta3],
        cardcode="04IO005T2",
        champion_spell=Set4Spells.VanguardsEdge,
    )


# When I Lurk, transform me into Death From Below.
# When I kill an enemy, I strike the weakest enemy.
def Pyke():
    effect = TransformEffect(AutoEntitySelector.SELF, Set4Spells.DeathFromBelow)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.LURK,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Pyke2)
    levelwatcher = ValueTriggeredAction(
        event_filter=EntityEvents.DAMAGE,
        threshold=15,
        action_on_value=levelup,
        ally_enum=OriginEnum.O_ALLY,
        instance_bound=False,
        condition=...,
        event_counter=EventCounterEnum.COUNT_VALUE,
    )
    return Champion(
        effects=[ta1, levelwatcher],
        cardcode="04BW005",
        champion_spell=Set4Spells.BoneSkewer,
    )


def Pyke2():
    effect = TransformEffect(AutoEntitySelector.SELF, Set4Spells.DeathFromBelow)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.LURK,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
    )
    effect1 = StrikeEffect(
        striker=AutoEntitySelector.SELF, target=AutoEntitySelector.WEAKEST_OPPONENT_UNIT
    )
    ta2 = TriggeredAction(
        event_filter=EntityEvents.KILL,
        action=effect1,
        ally_enum=OriginEnum.T_OPPO_O_SELF,
    )
    return Champion(
        effects=[ta1, ta2],
        cardcode="04BW005T2",
        champion_spell=Set4Spells.BoneSkewer,
    )


# Play: Summon an exact copy of an allied landmark. Attack: Deal 2 to my blocker 3 times. If it's dead or gone, deal 2 to the enemy Nexus instead.
def Taliyah():
    effect = CreateExactCopyEffect(target=CardFilter(type=Types_.LANDMARK))
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Taliyah2)
    levelwatcher = ValueTriggeredAction(
        event_filter=EntityEvents.SUMMON_LANDMARK,
        threshold=5,
        action_on_value=levelup,
        ally_enum=OriginEnum.O_ALLY,
        instance_bound=False,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )

    return Champion(
        play_effect=effect,
        effects=levelwatcher,
        cardcode="04SH073",
        champion_spell=Set4Spells.Stoneweaving,
    )


def Taliyah2():
    effect = CreateExactCopyEffect(target=CardFilter(type=Types_.LANDMARK))
    effect1 = PlaySkill(target=Set4Skills.ThreadedVolley)

    return Champion(
        play_effect=effect,
        attack_commit_effect=effect1,
        cardcode="04SH073T2",
        champion_spell=Set4Spells.Stoneweaving,
    )


def Sivir():
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Sivir2)
    levelwatcher = ValueTriggeredAction(
        event_filter=EntityEvents.DAMAGE,
        threshold=30,
        action_on_value=levelup,
        ally_enum=OriginEnum.O_ALLY,
        instance_bound=False,
        event_counter=EventCounterEnum.COUNT_VALUE,
    )
    return Champion(
        effects=levelwatcher,
        cardcode="04SH020",
        champion_spell=Set4Spells.Ricochet,
    )


# While I'm attacking, attacking allies have my keywords.
def Sivir2():
    # TODO
    dynamic = DynamicKeywordModifier(
        value=..., condition=..., target=CardFilter(location=LocEnum.BATTLEFIELD)
    )
    return Champion(
        effects=dynamic,
        cardcode="04SH020T1",
        champion_spell=Set4Spells.Ricochet,
    )


# The first time you slay a unit each round, grant me +2|+2 and I mark the weakest enemy. Round End: Kill units with my mark.
def Kindred():
    # TODO marked
    killaction = KillAction(target=...)
    effect = AddKeywordEffect(
        target=PostEventParam.TARGET, keyword=KeywordEnum.KINDRED_MARK
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SLAY,
        action=effect,
        ally_enum=OriginEnum.T_OPPO_O_ALLY,
        activations_per_round=1,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Kindred2)
    levelwatcher = ValueTriggeredAction(
        event_filter=EntityEvents.SLAY,
        threshold=2,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_OPPO_O_ALLY,
        condition=...,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(
        round_end_effects=killaction,
        effects=(levelwatcher, ta),
        cardcode="04SI005",
        champion_spell=Set4Spells.SpiritJourney,
    )


def Kindred2():
    killaction = KillAction(target=...)
    buff = BuffEffect(target=AutoEntitySelector.SELF, attack=2, health=2)
    effect = AddKeywordEffect(
        target=PostEventParam.TARGET, keyword=KeywordEnum.KINDRED_MARK
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SLAY,
        action=(buff, effect),
        ally_enum=OriginEnum.T_OPPO_O_ALLY,
        activations_per_round=1,
    )
    return Champion(
        round_end_effects=killaction,
        effects=ta,
        cardcode="04SI005T1",
        champion_spell=Set4Spells.SpiritJourney,
    )


# Strike: Create a Fleeting 0 cost Time Trick in hand.
def Ekko():
    create1 = CreateCardEffect(Set4Spells.TimeTrick, is_fleeting=True)
    create = CreateCardEffect(Set4Spells.Chronobreak, LocEnum.DECK, quantity=3)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.LEVEL_UP,
        action=create,
        activate_once=True,
        ally_enum=OriginEnum.T_SELF,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Ekko2)
    levelwatcher = ValueTriggeredAction(
        event_filter=EntityEvents.PREDICT,
        threshold=4,
        action_on_value=levelup,
        ally_enum=OriginEnum.O_ALLY,
        instance_bound=False,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(
        strike_effect=create1,
        effects=(ta1, levelwatcher),
        cardcode="04PZ001",
        champion_spell=Set4Spells.CalledShot,
    )


def Ekko2():
    create1 = CreateCardEffect(Set4Spells.TimeTrick, is_fleeting=True, cost=0)

    return Champion(
        strike_effect=create1,
        cardcode="04PZ001",
        champion_spell=Set4Spells.CalledShot,
    )


# When I level up, create 3 random Lurkers in hand.When I Lurk or Attack: Grant Lurker allies everywhere +1|+0.
def RekSai():
    buff_everywhere = BuffEverywhereEffect(
        attack=1, health=0, filter_obj=BaseCardFilter(flags=CardFlags.IS_LURKER)
    )
    ta1 = TriggeredAction(
        event_filter=EntityEvents.LURK,
        action=buff_everywhere,
        ally_enum=OriginEnum.T_SELF,
    )
    effect1 = MoveEffect(target=AutoEntitySelector.SELF, destination=LocEnum.DECK)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=RekSai2)
    ta2 = TriggeredAction(
        event_filter=EntityEvents.ATTACK_COMMIT,
        action=levelup,
        ally_enum=OriginEnum.T_SELF,
        activate_once=True,
        condition=...,
    )
    return Champion(
        round_end_effects=effect1,
        attack_commit_effect=buff_everywhere,
        effects=(ta1, ta2),
        cardcode="04SH019",
        champion_spell=Set4Spells.CallThePack,
    )


def RekSai2():
    effect = CreateCardEffect(
        target=BaseCardFilter(quantity=3, flags=CardFlags.IS_LURKER)
    )
    ta1 = TriggeredAction(
        event_filter=EntityEvents.LEVEL_UP,
        action=effect,
        activate_once=True,
        ally_enum=OriginEnum.T_SELF,
    )
    buff_everywhere = BuffEverywhereEffect(
        attack=1, health=0, filter_obj=BaseCardFilter(flags=CardFlags.IS_LURKER)
    )
    ta1 = TriggeredAction(
        event_filter=EntityEvents.LURK,
        action=buff_everywhere,
        ally_enum=OriginEnum.T_SELF,
    )
    return Champion(
        attack_commit_effect=buff_everywhere,
        effects=ta1,
        cardcode="04SH019T1",
        champion_spell=Set4Spells.CallThePack,
    )


# Your Nexus is Tough.
# When I'm summoned, summon a Frozen Thrall.
# Round Start: Create a Fleeting 0 cost Ice Shard in hand.
def Lissandra():
    create = CreateCardEffect(Set4Landmarks.FrozenThrall, LocEnum.HOMEBASE)
    advance = AdvanceCountdownEffect(target=..., value=2)
    create2 = CreateCardEffect(Set4Units.Watcher)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.LEVEL_UP,
        action=create2,
        activate_once=True,
        ally_enum=OriginEnum.T_SELF,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Lissandra2)
    levelwatcher = ValueTriggeredAction(
        event_filter=EntityEvents.SUMMON,
        threshold=2,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        instance_bound=False,
        condition=...,  # TODO 8+COST
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(
        summon_effect=(create, advance),
        effects=(ta1, levelwatcher),
        cardcode="04FR005",
        champion_spell=Set4Spells.Entomb,
    )


def Lissandra2():
    create = CreateCardEffect(Set4Landmarks.FrozenThrall, LocEnum.HOMEBASE)
    advance = AdvanceCountdownEffect(target=..., value=2)
    dynamic = DynamicKeywordModifier(
        value=KeywordEnum.TOUGH, target=TargetPlayer.ORIGIN_OWNER
    )
    create2 = CreateCardEffect(Set4Spells.IceShard, cost=0)
    return Champion(
        summon_effect=(create, advance),
        effects=dynamic,
        round_start_effects=create2,
        cardcode="04FR005T1",
        champion_spell=Set4Spells.Entomb,
    )


# Each time I see you deal 15+ damage, create a Mirror Image in hand.
# If you already have one, reduce its cost by 1 instead.
def LeBlanc():
    create2 = CreateCardEffect(Set4Spells.MirrorImage)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.LEVEL_UP,
        action=create2,
        activate_once=True,
        ally_enum=OriginEnum.T_SELF,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=LeBlanc2)
    levelwatcher = ValueTriggeredAction(
        event_filter=EntityEvents.DAMAGE,
        threshold=15,
        action_on_value=levelup,
        ally_enum=OriginEnum.O_SELF,
        event_counter=EventCounterEnum.COUNT_VALUE,
    )
    return Champion(
        effects=(ta1, levelwatcher),
        cardcode="",
        champion_spell=Set4Spells.SigilofMalice,
    )


def LeBlanc2():
    effect = BuffCostEffect(target=..., value=1)
    create2 = CreateCardEffect(Set4Spells.MirrorImage)
    condition = Condition(
        target=TargetPlayer.ORIGIN_OWNER,
        condition=PlayerFlags.HAS_NO_X_HAND_CARD,
        parameter=Set4Spells.MirrorImage,
    )
    effect2 = BranchingAction(condition=condition, if_true=create2, if_false=effect)
    ta = ValueTriggeredAction(
        event_filter=EntityEvents.DAMAGE,
        threshold=15,
        action_on_value=effect2,
        ally_enum=OriginEnum.O_SELF,
        event_counter=EventCounterEnum.COUNT_VALUE,
        on_activate_reset=True,
    )
    return Champion(
        effects=ta,
        cardcode="",
        champion_spell=Set4Spells.SigilofMalice,
    )


# Round Start: Create a Fleeting copy of each non-Fleeting card I saw you play last round.
# Play: Create 4 Time Bombs in your deck, then Predict.
def Zilean():
    create = CreateCardEffect(Set4Landmarks.TimeBomb, LocEnum.DECK, quantity=4)
    effect = PredictEffect()
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=LeBlanc2)
    levelwatcher = ValueTriggeredAction(
        event_filter=EntityEvents.DESTROY_LANDMARK,
        threshold=2,
        action_on_value=levelup,
        condition=...,
        ally_enum=OriginEnum.T_OPPO_O_ALLY,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(
        play_effect=(create, effect),
        effects=levelwatcher,
        cardcode="04SH039",
        champion_spell=Set4Spells.CarefulPreparation,
    )


def Zilean2():
    create = CreateCardEffect(Set4Landmarks.TimeBomb, LocEnum.DECK, quantity=4)
    effect = PredictEffect()
    # TODO last value storage?
    create2 = CreateCardEffect(target=..., is_fleeting=True)
    return Champion(
        play_effect=(create, effect),
        round_start_effects=create2,
        cardcode="04SH039T1",
        champion_spell=Set4Spells.CarefulPreparation,
    )


# When I'm summoned, level up, or Strike: Summon a Warlord's Hoard or advance it 1 round.
def Akshan():
    create = CreateCardEffect(Set4Landmarks.WarlordsHoard, LocEnum.HOMEBASE)
    advance = AdvanceCountdownEffect(target=..., value=1)
    condition = Condition(
        target=TargetPlayer.ORIGIN_OWNER,
        condition=PlayerFlags.HAS_X_CARD_IN_PLAY,
        parameter=Set4Landmarks.WarlordsHoard,
    )
    effect2 = BranchingAction(condition=condition, if_true=create, if_false=advance)
    create2 = CreateCardEffect(Set4Landmarks.WarlordsPalace, LocEnum.HOMEBASE)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.LEVEL_UP,
        action=create2,
        activate_once=True,
        ally_enum=OriginEnum.T_SELF,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Akshan2)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.ACTIVATE_COUNTDOWN,
        action=levelup,
        ally_enum=OriginEnum.T_ALLY,
        activate_once=True,
        instance_bound=False,
        condition=...,
    )
    return Champion(
        strike_effect=effect2,
        summon_effect=effect2,
        effects=ta1,
        cardcode="04SH130",
        champion_spell=Set4Spells.GrapplingHook,
    )


def Akshan2():
    create = CreateCardEffect(Set4Landmarks.WarlordsHoard, LocEnum.HOMEBASE)
    advance = AdvanceCountdownEffect(target=..., value=1)
    condition = Condition(
        target=TargetPlayer.ORIGIN_OWNER,
        condition=PlayerFlags.HAS_X_CARD_IN_PLAY,
        parameter=Set4Landmarks.WarlordsHoard,
    )
    effect2 = BranchingAction(condition=condition, if_true=create, if_false=advance)
    return Champion(
        strike_effect=effect2,
        summon_effect=effect2,
        cardcode="04SH130T2",
        champion_spell=Set4Spells.GrapplingHook,
    )
