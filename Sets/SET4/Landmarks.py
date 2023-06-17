from random import choice
import Sets.SET1.Units as Set1Units
import Sets.SET1.Spells as Set1Spells
import Sets.SET2.Spells as Set2Spells
import Sets.SET2.Units as Set2Units
import Sets.SET3.Units as Set3Units
import Sets.SET3.Spells as Set3Spells
import Sets.SET3.Skills as Set3Skills

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
from actions.activations.countdown import CountdownEffect
from actions.activations.multiple_activations import MultipleActivationsEffect
from actions.activations.negate_spell import NegateSpell
from actions.activations.play_skill import PlaySkill
from actions.activations.recast_spell import  RecastEventOfAction
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
from actions.beacons.restore_sun import RestoreSundisc
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
from actions.win.win_con import DeclareGameResult
from card_classes.champion import Champion
from card_classes.landmark import Landmark
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


# Play: Predict.Countdown 2: Summon a Clockling.
def AncientPreparations():
    effect1 = PredictEffect()
    effect2 = CreateCardEffect()
    effect3 = CountdownEffect(effect=effect2, countdown=2)
    return Landmark(play_effect=effect1, countdown_effect=effect3)


# Countdown 2: Summon exact copies of the units and landmarks stored inside.
def FrozenTomb():
    #TODO internal
    effect = CreateCardEffect()
    effect1 = CountdownEffect(effect=effect, countdown=2)
    return Landmark(countdown_effect=effect1)


# Countdown 1: Summon exact copies of the units and landmarks stored inside.
def StasisStatue():
    effect = CreateCardEffect()
    effect1 = CountdownEffect(effect=effect, countdown=1)
    return Landmark(countdown_effect=effect1)


# When an enemy is summoned, destroy me to grant it Vulnerable.
def RoilingSands():
    effect = DestroyLandmarkEffect(target=AutoEntitySelector.SELF)
    effect1 = AddKeywordEffect(
        PostEventParam.TARGET, KeywordEnum.VULNERABLE, fizz_if_fail=effect
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_OPPO,
        action=(effect, effect1),
    )
    return Landmark(effects=ta)


# Countdown 1: Get an extra mana gem this round.
def CrestofInsight():
    effect = GainManaGemEffect(round_only=True)
    effect1 = CountdownEffect(effect=effect, countdown=1)
    return Landmark(countdown_effect=effect1)



# Start of Game: Summon 1 of me from your deck if it's all Shuriman.
# Countdown 25: Restore the Sun Disc.
# When an Ascended ally levels up, advance me 10 rounds.
def BuriedSunDisc():
    effect = MoveEffect(target=AutoEntitySelector.SELF, destination=LocEnum.HOMEBASE)
    ta = TriggeredAction(
        event_filter=GameStateEnums.GAME_START,
        action=effect,
        condition=...
        #NO SUNDISC IN PLAY, ORIGIN IN DECK
    )
    effect1 = AdvanceCountdownEffect(target=AutoEntitySelector.SELF, value=10)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.LEVEL_UP,
        ally_enum=OriginEnum.T_ALLY,
        action=effect1,
        condition=...
    )
    effect2 = RestoreSundisc()
    effect3 = CountdownEffect(effect=effect2, countdown=25)
    return Landmark(countdown_effect=effect3, effects=(ta, ta1))

# Countdown 8: Summon a Frostguard Thrall.
def FrozenThrall():
    effect = CreateCardEffect(Set4Units.FrostguardThrall, LocEnum.HOMEBASE)
    return Landmark(countdown_effect=effect)


# When allies attack, before Lurk tries to activate, obliterate the top card of your deck
# if it doesn't have Lurk.
def RippersBay():
    effect = ObliterateEffect(target=CardFilter())
    effect1 = TriggeredAction(
        event_filter=EntityEvents.LURK,
        ally_enum=OriginEnum.T_ALLY,
        action=effect,
        condition=...
    )
    #TODO forefront
    return Landmark(effects=effect1)


# When allies attack, summon an attacking Sand Soldier.
def EmperorsDais():
    effect = CreateCardEffect(Set4Units.SandSoldier, LocEnum.BATTLEFIELD)
    ta = TriggeredAction(
        event_filter=EntityEvents.PLAYER_ATTACK_COMMIT,
        ally_enum=OriginEnum.T_ALLY,
        action=effect,
    )
    return Landmark(effects=ta)


# Countdown 3: Summon a Grumpy Rockbear.
def HibernatingRockbear():
    effect = CreateCardEffect(Set4Units.GrumpyRockbear, LocEnum.HOMEBASE)
    effect1 = CountdownEffect(effect=effect, countdown=3)
    return Landmark(countdown_effect=effect1)


# When I'm summoned, draw 1.
# Countdown 2: Draw 1.
def Preservarium():
    effect = DrawEffect()
    effect1 = CountdownEffect(effect=effect, countdown=2)
    return Landmark(countdown_effect=effect1, summon_effect=effect)


# Countdown 2: Obliterate the weakest enemy.
def RockfallPath():
    effect = ObliterateEffect(target=AutoEntitySelector.WEAKEST_OPPONENT_UNIT)
    effect1 = CountdownEffect(effect=effect, countdown=2)
    return Landmark(countdown_effect=effect1)


# Countdown 2: Create 2 random Celestial cards that cost 3 or less in hand.
def StartippedPeak():
    effect = CreateCardEffect(
        BaseCardFilter(quantity=2, cost=(0, 3), subtype=SubTypes_.CELESTIAL)
    )
    effect1 = CountdownEffect(effect=effect, countdown=2)

    return Landmark(countdown_effect=effect1)


# Reputation: I cost 0.
# Countdown 1: Create 2 Lucky Finds in hand.
def InnerSanctum():
    effect = CreateCardEffect(Set4Spells.LuckyFind)
    effect1 = CountdownEffect(effect=effect, countdown=1)
    effect2 = DynamicCostModifier(
        value=0, operator=Ops_.SET, condition=PlayerFlags.REPUTATION
    )
    return Landmark(countdown_effect=effect1, effects=effect2)


# Countdown 3: Create a Seed of Strength in hand.
def SpiralStairs():
    effect = CreateCardEffect(Set4Spells.SeedofStrength)
    effect1 = CountdownEffect(effect=effect, countdown=3)
    return Landmark(countdown_effect=effect1)


# Once I've seen 3 Fearsome allies attack, destroy me to summon Vilemaw.
def TheTwistedTreeline():
    effect = DestroyLandmarkEffect(target=AutoEntitySelector.SELF)
    effect1 = CreateCardEffect(Set1Units.Vilemaw, LocEnum.HOMEBASE, fizz_if_fail=effect)
    ta = ValueTriggeredAction(
        event_filter=EntityEvents.ATTACK_COMMIT,
        ally_enum=OriginEnum.T_ALLY,
        action_on_value=(effect, effect1),
        condition=...,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Landmark(effects=ta)


# When I'm summoned, heal your Nexus 4.
# Countdown 1: Deal 2 to EVERYTHING.
def BlightedRavine():
    effect = DamageEffect(AutoEntitySelector.EVERYTHING, value=2)
    effect1 = CountdownEffect(effect=effect, countdown=3)
    effect2 = HealEffect(TargetPlayer.ORIGIN_OWNER, value=4)
    return Landmark(countdown_effect=effect1, summon_effect=effect2)


# Countdown 2: Summon a Grumpy Rockbear.
# Then, if you've summoned 4+ landmarks this game, grant the strongest ally +2|+2.
def SaltSpire():
    effect = CreateCardEffect(Set4Units.GrumpyRockbear)
    effect1 = BuffEffect(
        AutoEntitySelector.STRONGEST_BOARD_UNIT, attack=2, health=2, condition=...
    )
    effect2 = CountdownEffect(effect=(effect, effect1), countdown=2)
    return Landmark(countdown_effect=effect2)


# Countdown 1: Stun the 2 weakest enemies.Daybreak: Summon a copy of me with Countdown 2.
def EyeoftheRaHorak():
    effect = StunEffect(
        target=CardFilter(
            quantity=2, sorter=CardSorter.WEAKEST, owner=TargetPlayer.OPPONENT
        )
    )
    effect1 = CountdownEffect(effect=effect, countdown=1)
    effect2 = CreateCardEffect(EyeoftheRaHorak, LocEnum.HOMEBASE)
    effect3 = ...
    return Landmark(countdown_effect=effect, play_daybreak=(effect2, effect3))


# When I count down, summon a random 1 cost follower.
# Countdown 2: Grant 1 cost allies +2|+1 and Fearsome.
def ReaversRow():
    effect = CreateCardEffect(
        BaseCardFilter(cost=1, is_follower=True), LocEnum.HOMEBASE
    )
    effect1 = CountdownEffect(effect=effect, countdown=2)
    effect2 = BuffEffect(
        target=CardFilter(cost=1, attack=2, health=1, keyword=KeywordEnum.FEARSOME)
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.COUNTDOWN,
        ally_enum=OriginEnum.T_SELF,
        action=effect2,
    )
    return Landmark(countdown_effect=effect1, effects=ta)


# When allies attack, summon an attacking Sandstone Charger.
def SandsweptTomb():
    effect = CreateCardEffect(Set4Units.SandstoneCharger, LocEnum.BATTLEFIELD)
    ta = TriggeredAction(
        event_filter=EntityEvents.PLAYER_ATTACK_COMMIT,
        ally_enum=OriginEnum.T_ALLY,
        action=effect,
    )
    return Landmark(effects=ta)


# Countdown 8: Create a Relic of Power in hand.When you target allies advance me 1.
def WarlordsPalace():
    effect = CreateCardEffect(Set4Spells.RelicofPower)
    effect1 = CountdownEffect(effect=effect, countdown=8)
    effect2 = AdvanceCountdownEffect(target=AutoEntitySelector.SELF, value=1)
    ta = TriggeredAction(
        event_filter=EntityEvents.TARGETED,
        ally_enum=OriginEnum.T_ALLY,
        action=effect2,
    )
    return Landmark(countdown_effect=effect1, effects=ta)


# Countdown 8: Create a Sentinel's Hoard in hand.When you target allies advance me 1.
def WarlordsHoard():
    effect = CreateCardEffect(Set4Spells.SentinelsHoard)
    effect1 = CountdownEffect(effect=effect, countdown=8)
    effect2 = AdvanceCountdownEffect(target=AutoEntitySelector.SELF, value=1)
    ta = TriggeredAction(
        event_filter=EntityEvents.TARGETED,
        ally_enum=OriginEnum.T_ALLY,
        action=effect2,
    )
    return Landmark(countdown_effect=effect1, effects=ta)


# When I'm summoned, draw 1 and advance other allied Time Bombs 1 round.
# Countdown 1: Deal 1 to enemies and the enemy Nexus.
def TimeBomb():
    effect = DamageEffect(AutoEntitySelector.OPPONENT_NEXUS_AND_BOARD_UNITS, value=1)
    effect1 = CountdownEffect(effect=effect, countdown=1)
    effect2 = DrawEffect()
    effect3 = AdvanceCountdownEffect(target=CardFilter(card_type=TimeBomb), value=1)
    return Landmark(countdown_effect=effect1, summon_effect=(effect2, effect3))


# Enemies are Vulnerable.
# Round Start: Rally.
def GeneralsPalace():
    effect = DynamicKeywordModifier(
        value=KeywordEnum.VULNERABLE, target=AutoEntitySelector.ALL_OPPONENT_UNITS
    )
    return Landmark(
        round_end_effects=RallyEffect(), effects=effect
    )
