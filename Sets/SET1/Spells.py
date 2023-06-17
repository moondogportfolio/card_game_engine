from attr import define
from Sets.SET1.CustomSpells import (
    RummageEffect,
    ShatterEffect,
    StandUnitedEffect,
    TrueshotBarrageEffect,
)
import Sets.SET1.Units as Set1Units
from actions.activations.negate_spell import NegateSpell
from actions.action_modifiers.silence import SilenceEffect
from actions.attribute.buff import BuffCostEffect, BuffEffect
from actions.attribute.buff_everywhere import (
    BuffEverywhereEffect,
    TargetedBuffEverywhereEffect,
)
from actions.attribute.damage import DamageEffect, SpellOverwhelmEffect
from actions.attribute.drain import DrainEffect
from actions.attribute.frostbite import FrostbiteEffect
from actions.attribute.gain_mana_gem import GainManaGemEffect
from actions.attribute.heal import HealEffect
from actions.attribute.rally import RallyEffect
from actions.attribute.refill_mana import RefillSpellMana
from actions.attribute.reveal import RevealEffect
from actions.attribute.set_attribute import SetAttribute
from actions.attribute.spend_mana import SpendManaEffect
from actions.branching.branching_action import BranchingAction
from actions.champ.level_up import LevelupEffect
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
from actions.keywords.remove_keyword import PurgeKeywordsEffect, RemoveKeywordEffect
from actions.keywords.stun_effect import StunEffect
from actions.meta.create_ta import CreateTriggeredAction
from actions.movement.capture import CaptureEffect
from actions.movement.discard import DiscardEffect
from actions.movement.draw import (
    DrawEffect,
    DrawSpecificReturnRestEffect,
    TargetedDrawAction,
)
from actions.movement.initsplace import InItsPlaceEffect
from actions.movement.kill import DestroyLandmarkEffect, KillAction
from actions.movement.move import MoveEffect
from actions.movement.nba import NabEffect
from actions.movement.obliterate import ObliterateEffect
from actions.movement.predict import PredictEffect
from actions.movement.recall import RecallEffect
from actions.movement.revive import ReviveEffect
from actions.movement.steal import StealEffect
from actions.movement.summon import SummonEffect
from actions.movement.swap import SwapPositionsEffect
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
from actions.reactions.state_triggered_action import StateTriggeredAction
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
    PlantMysteriousPortalEffect,
    PlantPuffcaps,
    SetTrapEffect,
    TrapMultiplier,
)
from card_classes.spell import Spell
from card_classes.unit import Unit
from conditions.base_condition import Condition, OwnerCondition, OwnerStatisticCondition
from entity_selectors.base_card_filter import BaseCardFilter, InvokeBaseCardFilter
from entity_selectors.card_filter import (
    CardFilter,
    DrawCardFilter,
    EntityFilter,
    StackSpellFilter,
)
from entity_selectors.input import ChoiceAction, ChoiceBaseCard, Input
from entity_selectors.target_game_card import TargetEntity
from enums.attribute import AttrEnum
from enums.card_rarity import CardRarity
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
from enums.region import RegionEnum
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
from value.entity_attribute import EntityAttribute
from value.player_statistic import PlayerStatistic
from value.player_statistic_list import PlayerStatisticList


# Kill ALL units.
def TheRuination():
    effect = KillAction(target=AutoEntitySelector.ALL_BOARD_UNITS)
    return Spell(activation_effect=effect)


# Drain 3 from any unit.
def GraspoftheUndying():
    effect = DrainEffect(target=TargetShorthand.ANY_BOARD_UNIT, value=3)
    return Spell(activation_effect=effect)


# Get an empty mana gem and heal your Nexus 3.
def CatalystofAeons():
    effect = HealEffect(target=TargetPlayer.ORIGIN_OWNER, value=3)
    effect1 = GainManaGemEffect()
    return Spell(activation_effect=(effect, effect1))


# Deal 2 to ALL units.
def Avalanche():
    effect = DamageEffect(target=AutoEntitySelector.ALL_BOARD_UNITS, value=2)
    return Spell(activation_effect=effect)


# Pick a follower. Create an Ephemeral copy of it in hand.
def FadingMemories():
    target_obj = TargetEntity(choices=CardFilter(owner=None))
    effect = CreateCardEffect(target=target_obj, is_ephemeral=True)
    return Spell(activation_effect=effect)


# Costs 1 less for each ally that died this round. Summon a random 5 cost follower from Demacia.
def Remembrance():
    target_obj = BaseCardFilter(
        cost=5, regions=RegionEnum.DEMACIA, flags=CardFlags.IS_FOLLOWER
    )
    effect = CreateCardEffect(target=target_obj, location=LocEnum.HOMEBASE)
    buff_cost = BuffCostEffect(target=AutoEntitySelector.SELF, value=1, round_only=True)
    ta = TriggeredAction(
        event_filter=EntityEvents.DIE, action=buff_cost, ally_enum=OriginEnum.T_ALLY
    )
    # effect = DynamicCostModifier(value=PlayerStatistic.ALLY_DIED_THIS_ROUND)
    return Spell(activation_effect=effect, effects=ta)


# Fully heal an ally, then double its Power and Health.
def RedoubledValor():
    heal_effect = HealEffect(target=TargetEntity(), value=Ops_.MAX)
    attr_buff = BuffEffect(
        target=heal_effect.target, attack=2, health=2, operator=Ops_.MULTIPLY
    )
    return Spell(activation_effect=(heal_effect, attr_buff))


# Grant a damaged ally +3|+3.
def TakeHeart():
    effect = BuffEffect(
        target=TargetEntity(choices=CardFilter(flags=CardFlags.IS_DAMAGED)),
        attack=3,
        health=3,
    )
    return Spell(activation_effect=effect)


# Transform a follower into an exact copy of another follower.
def HextechTransmogulator():
    target_obj = TargetEntity(
        choices=CardFilter(owner=None, flags=CardFlags.IS_FOLLOWER)
    )
    source = TargetEntity(
        choices=CardFilter(owner=None, flags=CardFlags.IS_FOLLOWER),
        exclusion=target_obj,
    )
    trans_effect = TransformEffect(target=target_obj, new_form=source, exact_copy=True)
    return Spell(activation_effect=trans_effect)


# Frostbite 2 enemies.
def HarshWinds():
    target_obj = TargetEntity(
        choices=CardFilter(owner=TargetPlayer.OPPONENT), quantity=2
    )
    effect = FrostbiteEffect(target=target_obj)
    return Spell(activation_effect=effect)


# If you have a 5+ Power ally, kill ALL units with 4 or less Power.
def Reckoning():
    condition = Condition(
        target=TargetPlayer.ORIGIN_OWNER,
        condition=PlayerFlags.HAS_X_CARD_IN_PLAY,
        parameter=CardFilter(attack=(5, 0)),
    )
    effect = KillAction(
        target=CardFilter(owner=None, attack=(0, 4)),
        condition=condition,
    )
    return Spell(activation_effect=effect)


# To play, spend all your mana. Deal that much to a unit.
def ThermogenicBeam():
    effect = DamageEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT,
        value=PostEventParam.VALUE,
    )
    play_effect = SpendManaEffect(
        value=Ops_.MAX,
        include_spell_mana=True,
        coevent=effect,
    )
    return Spell(activation_effect=effect, play_effect=play_effect)


# Draw 3, then reduce those cards' costs by 1.
def ProgressDay():
    draw_effect = DrawEffect(quantity=3, cost_reduction=1)
    return Spell(activation_effect=draw_effect)


# Heal an ally or your Nexus 7. Draw 1.
def RitualofRenewal():
    heal_effect1 = HealEffect(target=TargetShorthand.ALLY_NEXUS_OR_BOARD_UNITS, value=7)
    draw_effect = DrawEffect()
    return Spell(activation_effect=(heal_effect1, draw_effect))


# Kill an ally to deal damage equal to its Power to anything.
def Atrocity():
    effect = KillAction(target=TargetShorthand.ALLIED_BOARD_UNIT)
    damage_effect = DamageEffect(
        target=TargetShorthand.ANYTHING, fizz_if_fail=effect, value=...
    )
    # TODO postevent parameter
    return Spell(activation_effect=(effect, damage_effect))


# Give all allies +2|+2 and Overwhelm this round.
def PackMentality():
    effect = BuffEffect(
        target=CardFilter(),
        attack=2,
        health=2,
        keyword=KeywordEnum.OVERWHELM,
        round_only=True,
    )
    return Spell(activation_effect=effect)


# Give an ally +4|+0 and Quick Attack this round.
def RisingSpellForce():
    effect = BuffEffect(
        target=TargetEntity(),
        attack=4,
        health=0,
        keyword=KeywordEnum.QUICKSTRIKE,
        round_only=True,
    )
    return Spell(activation_effect=effect)


# Recall an ally to summon a Living Shadow in its place.
def Shadowshift():
    effect = InItsPlaceEffect(
        destination=LocEnum.HAND,
        replacement=Set1Units.LivingShadow,
        target=TargetShorthand.ALLIED_BOARD_UNIT,
    )
    return Spell(activation_effect=effect)


# Summon a Dauntless Vanguard.
def Succession():
    effect = CreateCardEffect(
        target=Set1Units.DauntlessVanguard, location=LocEnum.HOMEBASE
    )
    return Spell(activation_effect=effect)


# If you have a Yeti, summon an Enraged Yeti. Otherwise, create it on top of your deck.
def TallTales():
    effect = CreateCardEffect(target=Set1Units.EnragedYeti, location=LocEnum.HOMEBASE)
    effect1 = CreateCardEffect(
        target=Set1Units.EnragedYeti, location=LocEnum.HOMEBASE, index=0
    )
    condition = OwnerCondition(
        condition=PlayerFlags.HAS_CARD_X_ON_BOARD,
        parameter=CardFilter(subtype=SubTypes_.YETI),
    )
    effect2 = BranchingAction(condition=condition, if_true=effect, if_false=effect1)
    return Spell(activation_effect=effect2)


# Summon an exact copy of an ally. It's Ephemeral and 1|1.
def SplinterSoul():
    effect = CreateExactCopyEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=1,
        health=1,
        is_ephemeral=True,
    )
    return Spell(activation_effect=effect)


# Summon 2 Dauntless Vanguards, then grant Elite allies +1|+1.
def Reinforcements():
    effect = CreateCardEffect(
        target=Set1Units.DauntlessVanguard,
        location=LocEnum.HOMEBASE,
        quantity=2,
    )
    effect1 = BuffEffect(target=CardFilter(subtype=SubTypes_.ELITE), attack=1, health=1)
    return Spell(activation_effect=(effect, effect1))


# Kill all enemies with 0 Power, then Frostbite all enemies.
def WintersBreath():
    effect = KillAction(target=CardFilter(attack=0, owner=TargetPlayer.OPPONENT))
    effect1 = FrostbiteEffect(target=CardFilter(owner=TargetPlayer.OPPONENT))
    return Spell(activation_effect=(effect, effect1))


# Drain 4 from an ally.
def AbsorbSoul():
    effect = DrainEffect(target=TargetShorthand.ALLIED_BOARD_UNIT, value=4)
    return Spell(activation_effect=effect)


# Deal 1 to anything.
def BladesEdge():
    effect = DamageEffect(target=TargetShorthand.ANYTHING, value=1)
    return Spell(activation_effect=effect)


# Kill a unit.
def Vengeance():
    effect = KillAction(target=TargetShorthand.ANY_BOARD_UNIT)
    return Spell(activation_effect=effect)


# Deal 3 to an enemy or the enemy Nexus, 2 to another, and 1 to another.
def TrueshotBarrage():
    effect1 = TrueshotBarrageEffect()
    return Spell(activation_effect=effect1)


# Grant an ally Tough.
def ChainVest():
    effect = AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT, keyword=KeywordEnum.TOUGH
    )
    return Spell(activation_effect=effect)


# Give an ally Elusive this round.
def Ghost():
    effect = AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        keyword=KeywordEnum.ELUSIVE,
        round_only=True,
    )
    return Spell(activation_effect=effect)


# Stun an enemy.
def Guile():
    effect = StunEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT)
    return Spell(activation_effect=effect)


# Pick a card in hand. Create 4 exact copies of it in your deck.
def CounterfeitCopies():
    effect = CreateExactCopyEffect(
        target=TargetShorthand.ALLIED_HAND_CARD,
        location=LocEnum.DECK,
        quantity=4,
    )
    return Spell(activation_effect=effect)


# If an ally died this round, summon 2 Spiderlings.
def CrawlingSensation():
    effect = CreateCardEffect(
        target=Set1Units.Spiderling,
        location=LocEnum.HOMEBASE,
        quantity=2,
        condition=PlayerFlags.ALLY_DIED_THIS_ROUND,
    )
    return Spell(activation_effect=effect)


# Summon an Illegal Contraption.
def UnlicensedInnovation():
    effect = CreateCardEffect(
        target=Set1Units.IllegalContraption, location=LocEnum.HOMEBASE
    )
    return Spell(activation_effect=effect)


# Swap 2 allies. Give them Barrier this round.
def StandUnited():
    effect = StandUnitedEffect(
        target=TargetEntity(
            choices=CardFilter(),
            quantity=2,
            minimum=2,
        )
    )
    return Spell(activation_effect=effect)


# Grant ALL battling followers Ephemeral.
def ShadowFlare():
    effect = AddKeywordEffect(
        target=CardFilter(
            location=LocEnum.BATTLEFIELD,
            owner=None,
            flags=CardFlags.IS_FOLLOWER,
        ),
        keyword=KeywordEnum.EPHEMERAL,
    )
    return Spell(activation_effect=effect)


# Give an ally +0|+2 this round.
def ElixirofIron():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=0,
        health=2,
        round_only=True,
    )
    return Spell(activation_effect=effect)


# Heal an ally or your Nexus 3.
def HealthPotion():
    effect = HealEffect(value=3, target=TargetShorthand.ALLY_NEXUS_OR_BOARD_UNITS)
    return Spell(activation_effect=effect)


# Give an ally +3|+0 this round.
def ElixirofWrath():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=3,
        health=0,
        round_only=True,
    )
    return Spell(activation_effect=effect)


# A battling ally strikes all battling enemies.
def Judgment():
    effect = StrikeEffect(
        target=CardFilter(location=LocEnum.BATTLEFIELD, owner=TargetPlayer.OPPONENT),
        striker=TargetEntity(choices=CardFilter(location=LocEnum.BATTLEFIELD)),
    )
    return Spell(activation_effect=effect)


# Summon the top ally from your deck now and EACH Round Start.
def WarmothersCall():
    effect = SummonEffect(target=CardFilter(location=LocEnum.DECK, quantity=1))
    effect1 = TriggeredAction(event_filter=GameStateEnums.ROUND_START, action=effect)
    effect2 = CreateTriggeredAction(
        triggered_action=effect1, target=TargetPlayer.ORIGIN_OWNER
    )
    return Spell(activation_effect=(effect, effect2))


"""
______________________
"""


# To play, discard 1.Give an ally +1|+0 this round.
def SpinningAxe():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=1,
        health=0,
        round_only=True,
    )
    effect1 = DiscardEffect(quantity=1)
    return Spell(activation_effect=effect, play_requisite=effect1)


# Grant Barrier to an ally in hand. Draw 1.
def KiGuardian():
    effect = AddKeywordEffect(
        target=TargetShorthand.ALLIED_HAND_UNIT, keyword=KeywordEnum.BARRIER
    )
    effect1 = DrawEffect()
    return Spell(activation_effect=(effect, effect1))


# Drain 1 from a unit to summon a Spiderling.
def VileFeast():
    effect = DrainEffect(value=1, target=TargetShorthand.ANY_BOARD_UNIT)
    effect1 = CreateCardEffect(
        target=Set1Units.Spiderling, location=LocEnum.HOMEBASE, fizz_if_fail=effect
    )
    return Spell(activation_effect=(effect, effect1))


# Kill a damaged unit to create a Fleeting Noxian Guillotine in hand.
def NoxianGuillotine():
    effect = KillAction(
        target=TargetEntity(choices=CardFilter(owner=None, flags=CardFlags.IS_DAMAGED))
    )
    effect1 = CreateCardEffect(
        target=NoxianGuillotine, is_fleeting=True, fizz_if_fail=effect
    )
    return Spell(activation_effect=(effect, effect1))


# Grant an ally Elusive.
def SumpworksMap():
    effect = AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT, keyword=KeywordEnum.ELUSIVE
    )
    return Spell(activation_effect=effect)


# Give an ally Barrier and Lifesteal this round.
def SpiritsRefuge():
    effect = AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        keyword=(KeywordEnum.LIFESTEAL, KeywordEnum.BARRIER),
        round_only=True,
    )
    return Spell(activation_effect=effect)


# Stun an attacking enemy.
def SteelTempest():
    effect = StunEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT)
    return Spell(activation_effect=effect)


# Deal 1 to all enemies. Heal your Nexus 3.
def WitheringWail():
    effect = DamageEffect(value=1, target=CardFilter(owner=TargetPlayer.OPPONENT))
    effect1 = HealEffect(value=3, target=TargetPlayer.ORIGIN_OWNER)
    return Spell(activation_effect=(effect, effect1))


# Frostbite an enemy.
def FlashFreeze():
    effect = FrostbiteEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT)
    return Spell(activation_effect=effect)


# Give an ally +1|+1 this round.
def RadiantStrike():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=1,
        health=1,
        round_only=True,
    )
    return Spell(activation_effect=effect)


# Give all allies +3|+3 this round.
def ForDemacia():
    effect = BuffEffect(target=CardFilter(), attack=3, health=3, round_only=True)
    return Spell(activation_effect=effect)


# Create in hand a random 6+ cost spell from your regions.
# Refill your spell mana.
def FlashofBrilliance():
    effect = CreateCardEffect(
        target=BaseCardFilter(
            cost=(6, 0), type=Types_.SPELL, quantity=1, owner_same_regions=True
        )
    )
    effect1 = RefillSpellMana(value=Ops_.MAX)
    return Spell(activation_effect=(effect, effect1))


# Deal 4 to the enemy Nexus.
def Decimate():
    effect = DamageEffect(target=TargetPlayer.OPPONENT, value=4)
    return Spell(activation_effect=effect)


# Give 2 allies +3|+3 this round.
def BacktoBack():
    effect = BuffEffect(
        target=TargetEntity(quantity=2, choices=CardFilter()),
        attack=3,
        health=3,
        round_only=True,
    )
    return Spell(activation_effect=effect)


# Grant 2 allies +0|+3.
def BloodswornPledge():
    effect = BuffEffect(
        target=TargetEntity(quantity=2, choices=CardFilter()), attack=0, health=3
    )
    return Spell(activation_effect=effect)


# To play, discard 1.Deal 3 to anything.
def GetExcited():
    effect = DamageEffect(target=TargetShorthand.ANYTHING, value=3)
    effect1 = DiscardEffect(quantity=1)
    return Spell(activation_effect=effect, play_requisite=effect1)


# Stop a Fast spell, Slow spell, or Skill.
def Deny():
    # TODO add skills to choices
    target = TargetEntity(
        choices=StackSpellFilter(
            owner=None,
            spell_speed=(SpellSpeedEnum.FAST, SpellSpeedEnum.SLOW),
        )
    )
    effect = NegateSpell(target=target)
    return Spell(activation_effect=effect)


# Give all allies Challenger this round.
def EnGarde():
    effect = AddKeywordEffect(
        target=CardFilter(), keyword=KeywordEnum.CHALLENGER, round_only=True
    )
    return Spell(activation_effect=effect)


# Deal 1 to an allied follower. If it survives, create a copy of it in hand.
def BloodforBlood():
    effect = DamageEffect(target=TargetEntity(), value=1)
    effect1 = CreateCardEffect(
        target=PostEventParam.TARGET,
        condition=Condition(target=PostEventParam.TARGET, condition=...),
    )
    # TODO if it survives
    return Spell(activation_effect=(effect, effect1))


# Summon 3 Spiderlings, then grant Spider allies +1|+0.
def BroodAwakening():
    effect = CreateCardEffect(
        target=Set1Units.Spiderling, location=LocEnum.HOMEBASE, quantity=3
    )
    effect1 = BuffEffect(
        target=CardFilter(subtype=SubTypes_.SPIDER), attack=1, health=0
    )
    return Spell(activation_effect=(effect, effect1))


# Give an ally Barrier this round.
def PrismaticBarrier():
    effect = AddKeywordEffect(target=TargetEntity(), keyword=KeywordEnum.BARRIER)
    return Spell(activation_effect=effect)


# An ally and an enemy strike each other.
def SingleCombat():
    target_obj2 = TargetEntity()
    target_obj1 = TargetEntity(choices=CardFilter(owner=TargetPlayer.OPPONENT))
    effect = StrikeEffect(target=target_obj1, striker=target_obj2)
    return Spell(activation_effect=effect)


# Revive a random ally that died this round.
def MistsCall():
    effect = ReviveEffect(
        target=TargetEntity(
            choices=None,
            entity_pool=PlayerStatisticList.ALLIES_DEAD_THIS_ROUND,
        )
    )
    return Spell(activation_effect=effect)


# Recall a unit.
def WillofIonia():
    effect = RecallEffect(target=TargetEntity(choices=CardFilter(owner=None)))
    return Spell(activation_effect=effect)


# If you've played 20 cards with different names this game, summon Catastrophe.
def PurrsuitofPerfection():
    condition = OwnerStatisticCondition(
        condition=PlayerStatistic.UNIQUE_NAMES_PLAYED, parameter=20
    )
    effect = CreateCardEffect(
        target=Set1Units.Catastrophe, location=LocEnum.HOMEBASE, condition=condition
    )
    return Spell(activation_effect=effect)


# Deal 1 to ALL battling units.
def DeathLotus():
    effect = DamageEffect(
        target=TargetEntity(
            choices=CardFilter(owner=None, location=LocEnum.BATTLEFIELD)
        ),
        value=1,
    )
    return Spell(activation_effect=effect)


# Steal an enemy follower this round. (Can't play if you have 6 allies or landmarks already.)
def Possession():
    effect = StealEffect(
        target=TargetShorthand.OPPONENT_BOARD_FOLLOWER, condition=..., round_only=True
    )
    return Spell(activation_effect=effect)


# Grant an ally +2|+2 and Ephemeral.
def MarkoftheIsles():
    effect = BuffEffect(
        target=TargetEntity(),
        attack=2,
        health=2,
        keyword=KeywordEnum.EPHEMERAL,
        round_only=True,
    )
    return Spell(activation_effect=effect)


# Summon 3 Unleashed Spirits.
def HauntedRelic():
    effect = CreateCardEffect(
        target=Set1Units.UnleashedSpirit,
        location=LocEnum.HOMEBASE,
        quantity=3,
    )
    return Spell(activation_effect=effect)


# Give an ally +3|+0 and Overwhelm this round.
def Might():
    effect = BuffEffect(
        target=TargetEntity(),
        attack=3,
        health=0,
        keyword=KeywordEnum.OVERWHELM,
        round_only=True,
    )
    return Spell(activation_effect=effect)


# Create in hand another random spell from your regions.
# Enlightened: Create 2 instead.
def InsightofAges():
    effect = CreateCardEffect(
        target=BaseCardFilter(type=Types_.SPELL, owner_same_regions=True, quantity=1)
    )
    effect1 = CreateCardEffect(
        target=BaseCardFilter(type=Types_.SPELL, owner_same_regions=True, quantity=2)
    )
    effect2 = BranchingAction(
        condition=PlayerFlags.ENLIGHTENED, if_true=effect1, if_false=effect
    )
    return Spell(activation_effect=effect2)


# Grant an ally +8|+4.
def BattleFury():
    effect = BuffEffect(target=TargetEntity(), attack=8, health=4)
    return Spell(activation_effect=effect)


# Grant Poro allies everywhere +1|+1.
def PoroSnax():
    effect = BuffEverywhereEffect(
        attack=1,
        health=1,
        filter_obj=CardFilter(subtype=SubTypes_.PORO),
    )
    return Spell(activation_effect=effect)


# If 3+ allies have died this round, summon Vilemaw.
def FreshOfferings():
    effect = CreateCardEffect(
        target=Set1Units.Vilemaw,
        location=LocEnum.HOMEBASE,
        condition=OwnerCondition(
            condition=PlayerFlags.ALLY_DIED_THIS_ROUND, parameter=3
        ),
    )
    return Spell(activation_effect=effect)


# Give an ally +3|+0 and Barrier this round.
def Riposte():
    effect = BuffEffect(
        target=TargetEntity(),
        attack=3,
        health=0,
        keyword=KeywordEnum.BARRIER,
        round_only=True,
    )
    return Spell(activation_effect=effect)


# Give an ally +3|+0 or +0|+3 this round.
def TwinDisciplines():
    effect = BuffEffect(target=TargetEntity(), attack=2, health=0, round_only=True)
    effect1 = BuffEffect(target=TargetEntity(), attack=0, health=3, round_only=True)
    effect2 = ChoiceAction(choices=[effect, effect1])
    return Spell(activation_effect=effect2)


# If you've played 15 cards with different names this game, summon Catastrophe.
def AcceleratedPurrsuit():
    condition = OwnerStatisticCondition(
        condition=PlayerStatistic.UNIQUE_NAMES_PLAYED, parameter=15
    )
    effect = CreateCardEffect(
        target=Set1Units.Catastrophe, location=LocEnum.HOMEBASE, condition=condition
    )
    return Spell(activation_effect=effect)


# When cast or discarded, grant all allies +1|+0.
def Vision():
    effect = BuffEffect(target=CardFilter(), attack=1, health=0)
    effect1 = TriggeredAction(
        event_filter=EntityEvents.DISCARD, action=effect, ally_enum=OriginEnum.T_SELF
    )
    return Spell(activation_effect=effect, effects=effect1)


# Deal 4 to an enemy. If there are no enemies, deal 4 to the enemy Nexus instead.
def FinalSpark():
    target = TargetEntity(choices=CardFilter(owner=TargetPlayer.OPPONENT), minimum=0)
    effect1 = SpellOverwhelmEffect(value=4, target=target)
    return Spell(activation_effect=effect1)


# Deal 3 to each enemy that was summoned this round.
def TheBox():
    effect = DamageEffect(
        target=TargetEntity(
            choices=None,
            entity_pool=PlayerStatisticList.ALLIES_SUMMONED_THIS_ROUND,
        ),
        value=3,
    )
    return Spell(activation_effect=effect)


# Silence a follower.
def Purify():
    effect = SilenceEffect(target=TargetShorthand.ANY_BOARD_FOLLOWER)
    return Spell(activation_effect=effect)


# Give an ally +1|+0 and Quick Attack this round.
def Rush():
    effect = BuffEffect(
        target=TargetEntity(),
        attack=1,
        health=0,
        keyword=KeywordEnum.QUICKSTRIKE,
        round_only=True,
    )
    return Spell(activation_effect=effect)


# If an ally died this round, deal 4 to a unit.
def BlackSpear():
    effect = DamageEffect(
        target=TargetEntity(choices=CardFilter(owner=None)),
        condition=PlayerFlags.ALLY_DIED_THIS_ROUND,
        value=4,
    )
    return Spell(activation_effect=effect)


# Summon 2 Scrap Scuttlers.
def ScrapdashAssembly():
    effect = CreateCardEffect(
        target=Set1Units.ScrapScuttler, location=LocEnum.HOMEBASE, quantity=2
    )
    return Spell(activation_effect=effect)


# To play, discard up to 2 cards. Draw 1 for each card you discarded.
def Rummage():
    # TODO play requisite
    effect = RummageEffect(target=CardFilter())
    return Spell(activation_effect=effect, play_requisite=effect)


# Frostbite an enemy with 3 or less Health.
def BrittleSteel():
    effect = FrostbiteEffect(
        target=CardFilter(owner=TargetPlayer.OPPONENT, health=(0, 3))
    )
    return Spell(activation_effect=effect)


# Stun all enemies with 4 or less Power.
def IntimidatingRoar():
    effect = StunEffect(target=CardFilter(owner=TargetPlayer.OPPONENT, attack=(0, 4)))
    return Spell(activation_effect=effect)


# Deal 1 to an enemy or the enemy Nexus, and 1 to another.Draw 1.
def StatikkShock():
    effect = DamageEffect(
        target=TargetEntity(
            choices=EntityFilter(
                owner=TargetPlayer.OPPONENT, player=TargetPlayer.OPPONENT
            ),
            minimum=0,
            quantity=2,
        ),
        value=1,
    )
    effect1 = DrawEffect()
    return Spell(activation_effect=(effect, effect1))


# Revive the 6 strongest allies that died this game and grant them Ephemeral.
def TheHarrowing():
    target_obj = TargetEntity(
        choices=None,
        entity_pool=PlayerStatisticList.ALLIES_DEAD_THIS_GAME,
        sorter=CardSorter.STRONGEST,
    )
    effect = ReviveEffect(target=target_obj)
    return Spell(activation_effect=effect)


# Deal 2 to anything.
def MysticShot():
    effect = DamageEffect(target=TargetShorthand.ANYTHING, value=2)
    return Spell(activation_effect=effect)


# A battling ally strikes a battling enemy.
def WhirlingDeath():
    target_obj1 = TargetEntity(choices=CardFilter(location=LocEnum.BATTLEFIELD))
    target_obj2 = TargetEntity(
        choices=CardFilter(location=LocEnum.BATTLEFIELD, owner=TargetPlayer.OPPONENT)
    )
    effect = StrikeEffect(target=target_obj2, striker=target_obj1)
    return Spell(activation_effect=effect)


# Summon 2 exact copies of an ally. They're Ephemeral.
def DawnandDusk():
    effect = CreateExactCopyEffect(
        target=TargetEntity(),
        location=LocEnum.HOMEBASE,
        is_ephemeral=True,
        quantity=2,
    )
    return Spell(activation_effect=effect)


# Plant 5 Poison Puffcaps on random cards in the enemy deck.
def MushroomCloud():
    effect = PlantPuffcaps(quantity=5)
    return Spell(activation_effect=effect)


# Remove Ephemeral from an ally to grant it to an enemy.
def DeathMark():
    target_obj1 = CardFilter(owner=TargetPlayer.OPPONENT)
    target_obj2 = CardFilter(keyword=KeywordEnum.EPHEMERAL)
    effect = AddKeywordEffect(target=target_obj2, keyword=KeywordEnum.EPHEMERAL)
    effect1 = RemoveKeywordEffect(
        target=target_obj1, keyword=KeywordEnum.EPHEMERAL, fizz_if_fail=effect
    )
    return Spell(activation_effect=(effect, effect1))


# Grant all allies in hand +1|+0.
def SownSeeds():
    target_obj = CardFilter(location=LocEnum.HAND)
    effect = BuffEffect(target=target_obj, attack=1, health=0)
    return Spell(activation_effect=effect)


# Draw a champion.
def Entreat():
    effect = DrawEffect(
        filter_obj=DrawCardFilter(
            flags=CardFlags.IS_CHAMPION,
        )
    )
    return Spell(activation_effect=effect)


# Grant 2 allies +2|+0.
def BrothersBond():
    effect = BuffEffect(
        target=TargetEntity(choices=CardFilter(), quantity=2),
        attack=2,
        health=0,
    )
    return Spell(activation_effect=effect)


# Reduce the cost of all allies in hand by 1.
def Mobilize():
    effect = BuffCostEffect(target=CardFilter(location=LocEnum.HAND), value=1)
    return Spell(activation_effect=effect)


# Kill a unit with 3 or less Power.
def CullingStrike():
    target_obj = TargetEntity(choices=CardFilter(owner=None, attack=(0, 3)))
    effect = KillAction(target=target_obj)
    return Spell(activation_effect=effect)


# Grant an ally and all allied copies of it everywhere +2|+2.
def IcebornLegacy():
    effect = TargetedBuffEverywhereEffect(
        attack=2,
        health=2,
        target=TargetShorthand.ALLIED_BOARD_UNIT,
    )
    return Spell(activation_effect=effect)


# Kill an ally to draw 2.
def GlimpseBeyond():
    effect = KillAction(target=TargetEntity())
    effect1 = DrawEffect(quantity=2, fizz_if_fail=effect)
    return Spell(activation_effect=(effect, effect1))


# If you have exactly 1 ally, grant it +3|+3.
def StandAlone():
    condition = OwnerCondition(PlayerFlags.HAS_X_BOARD_ALLIES, parameter=[1, True])
    effect = BuffEffect(target=TargetEntity(), attack=3, health=3, condition=condition)
    return Spell(activation_effect=effect)


# Deal 2 to an enemy, then Rally.
def Shunpo():
    effect = DamageEffect(
        target=TargetEntity(choices=CardFilter(owner=TargetPlayer.OPPONENT)),
        value=2,
    )
    effect1 = RallyEffect()
    return Spell(activation_effect=(effect, effect1))


# Stun an enemy. Give all allies +2|+0 this round.
def DecisiveManeuver():
    effect = StunEffect(
        target=TargetEntity(choices=CardFilter(owner=TargetPlayer.OPPONENT))
    )
    effect1 = BuffEffect(target=CardFilter(), attack=2, health=0, round_only=True)
    return Spell(activation_effect=(effect, effect1))


# Deal 4 to the enemy nexus and 1 to all enemies.
def SuperMegaDeathRocket():
    effect = DamageEffect(target=TargetPlayer.OPPONENT, value=4)
    effect1 = DamageEffect(
        target=AutoEntitySelector.OPPONENT_NEXUS_AND_BOARD_UNITS, value=1
    )
    return Spell(activation_effect=(effect, effect1))


# Grant an ally +1|+1.
# Rally.
def RelentlessPursuit():
    effect = BuffEffect(target=TargetEntity(), attack=1, health=1, round_only=True)
    effect1 = RallyEffect()
    return Spell(activation_effect=(effect, effect1))


# Deal 1 to an ally to give another ally +2|+2 this round.
def Transfusion():
    target_obj = TargetEntity()
    target_obj1 = TargetEntity(exclusion=target_obj)
    effect = DamageEffect(target=target_obj, value=1)
    effect1 = BuffEffect(
        target=target_obj1, attack=2, health=2, round_only=True, fizz_if_fail=effect
    )
    return Spell(activation_effect=(effect, effect1))


# Summon 2 Spectral Riders.
def OnslaughtofShadows():
    effect = CreateCardEffect(
        target=Set1Units.SpectralRider, location=LocEnum.HOMEBASE, quantity=2
    )
    return Spell(activation_effect=effect)


# Recall an ally.
def Recall():
    effect = RecallEffect(target=TargetEntity())
    return Spell(activation_effect=effect)


# When cast or discarded, summon a Scrap Scuttler.
def JuryRig():
    effect = CreateCardEffect(target=Set1Units.ScrapScuttler, location=LocEnum.HOMEBASE)
    effect1 = TriggeredAction(
        event_filter=EntityEvents.DISCARD, action=effect, ally_enum=OriginEnum.SELF
    )
    return Spell(activation_effect=effect, effects=effect1)


def CrystalArrow():
    target = TargetEntity(choices=CardFilter(owner=TargetPlayer.OPPONENT))
    effect = FrostbiteEffect(target=target)
    effect1 = FrostbiteEffect(
        target=CardFilter(owner=TargetPlayer.OPPONENT, health=(0, 3)),
        target_exclusion=target,
    )
    effect3 = DrawEffect()
    return Spell(activation_effect=(effect, effect1, effect3))


# An ally Captures a unit.
def Detain():
    effect = CaptureEffect(
        target=TargetShorthand.ANY_BOARD_UNIT, storage=TargetShorthand.ALLIED_BOARD_UNIT
    )
    return Spell(activation_effect=effect)


# Deal 4 to an enemy if it has 0 Power. Otherwise, Frostbite it.
def Shatter():
    effect = ShatterEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT)
    return Spell(activation_effect=effect)
