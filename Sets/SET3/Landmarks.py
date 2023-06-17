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


# Round End: Heal damaged allies 1.
# Then, once I've seen you heal 22+ damage from allies, win the game.


def StarSpring():
    effect = HealEffect(target=CardFilter(flags=CardFlags.IS_DAMAGED))
    win = DeclareGameResult(winner=TargetPlayer.ORIGIN_OWNER)
    watcher1 = ValueTriggeredAction(
        event_filter=EntityEvents.HEAL,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        threshold=22,
        action_on_value=win,
        event_counter=EventCounterEnum.COUNT_VALUE,
    )
    return Unit(round_start_effects=effect, effects=watcher1)


# Round Start: ALL players draw 1.
def HexcoreFoundry():
    effect = DrawEffect(player=TargetPlayer.ALL_PLAYERS)
    return Unit(round_start_effects=effect)


# Round Start: Create a Sanctuary in hand.
def MonasteryofHirana():
    effect = CreateCardEffect(Set3Spells.Sanctuary)
    return Unit(round_start_effects=effect)


# When an ally is summoned, give it +1|+0 and Challenger this round.
def TheGrandPlaza():
    effect = BuffEffect(
        target=PostEventParam.TARGET,
        keyword=KeywordEnum.CHALLENGER,
        attack=1,
        round_only=True,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON, ally_enum=OriginEnum.T_ALLY, action=effect
    )
    return Unit(effects=ta)


# When an ally survives damage, grant it +1|+0 and Tough.
def TheScargrounds():
    effect = BuffEffect(
        target=PostEventParam.TARGET,
        keyword=KeywordEnum.TOUGH,
        attack=1,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.DAMAGE_SURVIVE,
        ally_enum=OriginEnum.T_ALLY,
        action=effect,
    )
    return Unit(effects=ta)


# Round Start: Toss 1. If you are Deep, destroy me to summon a random Sea Monster.
def TheSlaughterDocks():
    effect = TossEffect(quantity=1)
    effect1 = DestroyLandmarkEffect(target=AutoEntitySelector.SELF)
    effect2 = CreateCardEffect(
        BaseCardFilter(subtype=SubTypes_.SEA_MONSTER),
        LocEnum.HOMEBASE,
        fizz_if_fail=effect1,
    )
    ta = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START,
        ally_enum=OriginEnum.T_ALLY,
        action=(effect1, effect2),
        condition=PlayerFlags.DEEP,
    )
    return Unit(round_start_effects=effect)


# Round End: Your strongest ally and the weakest enemy strike each other.
def NoxkrayaArena():
    effect = MutualStrikeEffect(
        first_striker=AutoEntitySelector.STRONGEST_BOARD_UNIT,
        second_striker=AutoEntitySelector.WEAKEST_OPPONENT_UNIT,
    )
    return Unit(round_end_effects=effect)


def TargonPeak():
    effect = BuffCostEffect(
        target=CardFilter(location=LocEnum.HAND, type=None),
        value=0,
        operator=Ops_.SET,
        round_only=True,
    )
    effect1 = BuffCostEffect(
        target=CardFilter(
            location=LocEnum.HAND, type=None, owner=TargetPlayer.OPPONENT
        ),
        value=0,
        operator=Ops_.SET,
        round_only=True,
    )
    return Unit(round_start_effects=(effect, effect1))


# Round Start: Discard your hand. Create 3 random cards in hand and grant them Fleeting.
def TheUniversityofPiltover():
    effect = DiscardEffect(quantity=Ops_.MAX)
    effect1 = CreateCardEffect(
        target=BaseCardFilter(quantity=3, type=None), is_fleeting=True
    )
    return Unit(round_start_effects=(effect, effect1))




# Each round, the first time you play 2 other cards, 
# refill 2 mana and grant your strongest ally +1|+0.
def TheVeiledTemple():
    effect = RefillManaEffect(value=2)
    effect1 = BuffEffect(target=AutoEntitySelector.SELF, attack=1)
    va = ValueTriggeredAction(
        event_filter=EntityEvents.PLAY,
        ally_enum=OriginEnum.T_ALLY,
        action_on_value=(effect, effect1),
        threshold=2,
        activations_per_round=1,
        round_end_reset=True,
        event_counter=EventCounterEnum.COUNT_INSTANCES
    )
    return Unit(effects=va)



# Round Start: If you can, kill your most expensive ally to summon an ally from your deck
# that costs 1 more.
def VaultsofHelia():
    hc = max(self.owner.homebase(), key=lambda x: x.cost)
    val = hc.cost + 1
    target = self.owner.first_instance_in_deck(lambda x: x.cost == val)
    if target:
        kill(hc)
        summon(target)


# Round Start: Create in hand a random level 2 champion that's not in your hand, deck, or play.
def TheHowlingAbyss():
    cards = self.owner.cards_in_play(lambda x: is_champion(True))
    unique_owned = set([card.cardCode for card in cards])
    chosen = self.json_manager.invoke(
        lambda x: x["cardCode"] not in unique_owned and x["supertype"] == "Champion",
        1,
    )[0]
    self.create_card(self, chosen)