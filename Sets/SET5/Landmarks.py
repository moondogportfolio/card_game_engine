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


# Countdown 3 or when I'm destroyed: Deal 1 to the enemy Nexus.
def ScrappyBomb():
    effect = DamageEffect(TargetPlayer.OPPONENT, value=1)
    effect1 = CountdownEffect(effect=effect, countdown=3)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.DESTROY_LANDMARK,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
    )
    return Landmark(countdown_effect=effect1, effects=ta1)


# Countdown 3 or when I'm destroyed: Summon a Dami'yin the Unbound.
def RisenAltar():
    # TODO
    effect = CreateCardEffect(Set5Units.Dami)
    effect1 = CountdownEffect(effect=effect, countdown=3)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.DESTROY_LANDMARK,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
    )
    return Landmark(countdown_effect=effect1, effects=ta1)


# Round Start: Create a follower from a new region in hand.
# Win the game if you've summoned units from 10 regions.
def TheBandleTree():
    effect = CreateCardEffect(BaseCardFilter(is_follower=True, regions=...))
    win = DeclareGameResult(winner=TargetPlayer.ORIGIN_OWNER)
    watcher1 = ValueTriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        threshold=10,
        action_on_value=win,
        condition=...,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Unit(round_start_effects=effect, effects=watcher1)


# Countdown 3 or when I'm destroyed: summon a Restored Devout.
def Sarcophagus():
    #TODO
    effect = CreateCardEffect(Set5Units)
    effect1 = CountdownEffect(effect=effect, countdown=3)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.DESTROY_LANDMARK,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
    )
    return Landmark(countdown_effect=effect1, effects=ta1)


# Round Start: Create in hand a Fleeting copy of a non-Fleeting spell you cast last round.
def CatalogueofRegrets():
    #TODO
    effect1 = CreateCardEffect(target=..., is_fleeting=True)
    return Landmark(round_start_effects=effect1)
    
    
# When I am summoned, summon a Forge Worker.
# When you cast a 6+ cost spell, destroy me and refill your spell mana.
def TheForgeOfTomorrow():
    effect = SummonEffect(Set5Units.ForgeWorker, LocEnum.HOMEBASE)
    effect1 = DestroyLandmarkEffect(target=AutoEntitySelector.SELF)
    effect2 = RefillSpellMana(value=Ops_.MAX)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL,
        ally_enum=OriginEnum.T_ALLY,
        action=(effect1, effect2),
        condition=...
    )
    return Landmark(summon_effect=effect, effects=ta1)

# Play: Recall an ally to summon an Ephemeral copy of it.
# Countdown 3: Summon another Ephemeral copy of it.
def GodWillowSeedling():
    #TODO
    effect = RecallEffect(target=TargetShorthand.ALLIED_BOARD_UNIT)
    effect1 = CreateCardEffect(target=..., is_ephemeral=True, fizz_if_fail=effect1)
    return Landmark(countdown_effect=effect, play_effect=(effect, effect1))


# Countdown 3 or when I'm summoned or destroyed: Grant the strongest ally +2|+0.
def ObeliskofPower():
    effect = BuffEffect(target=AutoEntitySelector.STRONGEST_BOARD_UNIT, attack=2)
    effect1 = CountdownEffect(effect=effect, countdown=3)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.DESTROY_LANDMARK,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
    )
    return Landmark(countdown_effect=effect1, effects=ta1)

# When I�m summoned or destroyed, Stun the strongest enemy.
def HexplosiveMinefield():
    effect = StunEffect(AutoEntitySelector.STRONGEST_OPPONENT_BOARD_UNIT)
    effect1 = CountdownEffect(effect=effect, countdown=3)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.DESTROY_LANDMARK,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
    )
    return Landmark(countdown_effect=effect1, effects=ta1)