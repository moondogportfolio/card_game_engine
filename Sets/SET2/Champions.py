from random import choice
from actions.activations.multiple_activations import MultipleActivationsEffect
from actions.activations.negate_spell import NegateSpell
from actions.activations.play_skill import PlaySkill
from actions.activations.recast_spell import RecastEventOfAction
from actions.attachments.autoequip import AutoEquipEffect
from actions.attachments.equip import EquipEffect
from actions.attachments.forge import ForgeEffect
from actions.attribute.buff import BuffCostEffect, BuffEffect
from actions.attribute.buff_everywhere import BuffEverywhereEffect
from actions.attribute.damage import DamageEffect
from actions.attribute.frostbite import FrostbiteEffect
from actions.attribute.heal import HealEffect
from actions.attribute.rally import RallyEffect
from actions.branching.branching_action import BranchingAction
from actions.champ.level_up import LevelupEffect
from actions.common.strike import StrikeEffect
from actions.create.create_card import CreateCardEffect
from actions.create.summon_specific_cards import SpawnEffect, SummonHuskEffect
from actions.keywords.add_keyword import AddKeywordEffect, AddRandomKeywordEffect
from actions.keywords.copy_keywords import CopyKeywords
from actions.keywords.stun_effect import StunEffect
from actions.meta.create_dynamic_value import CreateDynamicValue
from actions.movement.draw import DrawEffect
from actions.movement.move import MoveEffect
from actions.movement.obliterate import ObliterateEffect
from actions.movement.recall import RecallEffect
from actions.movement.revive import ReviveEffect
from actions.movement.summon import SummonEffect
from actions.movement.swap import SwapPositionsEffect
from actions.movement.toss import TossEffect
from actions.reactions.action_modifier import ActionModifier
from actions.reactions.action_negator import ActionNegator
from actions.reactions.action_replacement import ActionReplacement
from actions.reactions.dynamic_attr_modifier import (
    DynamicAttackModifier,
    DynamicCostModifier,
    DynamicKeywordModifier,
)
from actions.reactions.state_triggered_action import StateTriggeredAction
from actions.reactions.triggered_action import TriggeredAction
from actions.reactions.value_triggered_action import (
    EventCounterEnum,
    ValueTriggeredAction,
)
from actions.transform.transform import TransformEffect
from actions.traps.set_trap import (
    PlantChimes,
    PlantFlashBombTrap,
    PlantMysteriousPortalEffect,
    PlantPuffcaps,
    TrapMultiplier,
)
from actions.win.win_con import DeclareGameResult
from card_classes.champion import Champion
from card_classes.unit import Unit
from conditions.base_condition import Condition
from entity_selectors.base_card_filter import BaseCardFilter
from entity_selectors.card_filter import CardFilter
from entity_selectors.input import ChoiceBaseCard, ChoiceValue
from enums.attribute import AttrEnum
from enums.card_sorters import CardSorter
from enums.entity_events import EntityEvents
from enums.gamestate import GameStateEnums
from enums.keywords import KeywordEnum
from enums.location import LocEnum
from enums.operator import Ops_
from enums.origin_enum import OriginEnum
from enums.post_event_param import PostEventParam
from enums.subtypes import SubTypes_
from enums.types import Types_
from resolvable_enums.active_cards_selector import TargetShorthand
from resolvable_enums.auto_card_selector import AutoEntitySelector
import Sets.SET2.Spells as Set2Spells
import Sets.SET1.Units as Set1Units
import Sets.SET2.Units as Set2Units
import Sets.SET1.Skills as Set1Skills
import Sets.SET2.Skills as Set2Skills

from resolvable_enums.card_conditions import CardFlags
from resolvable_enums.player_conditions import PlayerFlags
from resolvable_enums.target_player import TargetPlayer
from value.entity_attribute import EntityAttribute


def Nautilus():
    # TODO
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Nautilus2)
    effect = CreateCardEffect(..., location=LocEnum.DECK)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.LEVEL_UP,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
        activate_once=True,
    )
    ta2 = TriggeredAction(
        event_filter=EntityEvents.DEEP, ally_enum=OriginEnum.T_ALLY, action=levelup
    )
    return Champion(effects=[ta1, ta2])


# Sea Monster allies cost 4 less.
def Nautilus2():
    effect = DynamicCostModifier(
        value=4, target=CardFilter(subtype=SubTypes_.SEA_MONSTER)
    )
    return Champion(
        effects=effect, cardcode="02BW053T1", champion_spell=Set2Spells.Riptide
    )


def Sejuani():
    effect = AddKeywordEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT,
        keyword=(KeywordEnum.FROSTBITE, KeywordEnum.VULNERABLE),
        round_only=True,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Sejuani2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.DAMAGE,
        threshold=5,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_OPPONEXUS,
        event_counter=EventCounterEnum.DISCRETE_ROUNDS,
    )
    return Champion(effects=watcher, play_effect=effect)


# Play: Give an enemy Frostbite and Vulnerable this round.Each round, the first time you damage the enemy Nexus, Frostbite all enemies.
def Sejuani2():
    effect = AddKeywordEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT,
        keyword=(KeywordEnum.FROSTBITE, KeywordEnum.VULNERABLE),
        round_only=True,
    )
    effect1 = FrostbiteEffect(target=AutoEntitySelector.ALL_OPPONENT_UNITS)
    ta = TriggeredAction(
        event_filter=EntityEvents.DAMAGE,
        ally_enum=OriginEnum.T_OPPONEXUS,
        activations_per_round=1,
        action=effect1,
    )
    return Champion(
        effects=ta,
        play_effect=effect,
        cardcode="02FR002T3",
        champion_spell=Set2Spells.FuryoftheNorth,
    )


def Vi():
    effect = BuffEffect(target=AutoEntitySelector.SELF, attack=1, max_attack=8)
    ta = TriggeredAction(
        event_filter=EntityEvents.PLAY,
        ally_enum=OriginEnum.T_ALLY,
        action=effect,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Vi2)
    watcher = TriggeredAction(
        event_filter=EntityEvents.STRIKE,
        ally_enum=OriginEnum.S_STRIKER,
        action=levelup,
        condition=...,
    )
    return Champion(effects=[ta, watcher])


# When I strike a unit while attacking, deal 5 to the enemy Nexus.
def Vi2():
    effect = DamageEffect(target=TargetPlayer.OPPONENT, value=5)
    watcher = TriggeredAction(
        event_filter=EntityEvents.BATTLE_STRIKE,
        ally_enum=OriginEnum.S_STRIKER,
        action=effect,
    )
    return Champion(
        effects=watcher,
        cardcode="02PZ008T2",
        champion_spell=Set2Spells.VaultBreaker,
    )


def Quinn():
    effect = CreateCardEffect(Set2Units.Valor)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Quinn2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.PLAYER_ATTACK_COMMIT,
        threshold=4,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(effects=watcher, attack_commit_effect=effect)


# Attack: Summon Valor Challenging the strongest enemy.
def Quinn2():
    effect = CreateCardEffect(Set2Units.Valor)
    return Champion(
        attack_commit_effect=effect,
        cardcode="02DE006T1",
        champion_spell=Set2Spells.BlindingAssault,
    )


def LeeSin():
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=LeeSin2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL,
        threshold=10,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        instance_bound=False,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    effect1 = AddKeywordEffect(
        target=AutoEntitySelector.SELF, keyword=KeywordEnum.CHALLENGER, round_only=True
    )
    effect1 = AddKeywordEffect(
        target=AutoEntitySelector.SELF, keyword=KeywordEnum.BARRIER, round_only=True
    )
    ta = TriggeredAction(
        # TODO internal?
    )
    return Champion(effects=watcher)


# When you cast a spell, give me Challenger this round.
# If you cast another, give me Barrier this round.
# I Dragon's Rage enemies that I Challenge.
def LeeSin2():
    effect = PlaySkill()
    return Champion(
        attack_commit_effect=effect,
        cardcode="02IO006T1",
        champion_spell=Set2Spells.SonicWave,
    )


def Gangplank():
    create = CreateCardEffect(Set2Units.PowderKeg, LocEnum.HOMEBASE)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Gangplank2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.DAMAGE,
        threshold=5,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_OPPONEXUS,
        event_counter=EventCounterEnum.DISCRETE_ROUNDS,
    )
    return Champion(effects=watcher, summon_effect=create)


# When I'm summoned or Round Start: Summon a Powder Keg.
# Attack: Deal 1 to all enemies and the enemy Nexus.


def Gangplank2():
    create = CreateCardEffect(Set2Units.PowderKeg, LocEnum.HOMEBASE)
    effect = PlaySkill(target=Set2Skills.PowderfulExplosion)
    return Champion(
        attack_commit_effect=effect,
        summon_effect=create,
        round_start_effects=create,
        cardcode="02BW032T3",
        champion_spell=Set2Spells.Parrrley,
    )


# Each round, the first 3 times you play a card, I play a Destiny Card.
def TwistedFate():
    # TODO randmoized
    dc = ChoiceBaseCard(
        choices=(Set2Skills.RedCard, Set2Skills.BlueCard, Set2Skills.GoldCard)
    )
    effect = PlaySkill(target=dc)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Gangplank2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.DRAW,
        threshold=9,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(
        effects=watcher,
        play_effect=effect,
        cardcode="02BW026",
        champion_spell=Set2Spells.PickaCard,
    )


def TwistedFate2():
    # TODO
    effect = PlaySkill(target=...)
    watcher = TriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL,
        ally_enum=OriginEnum.T_ALLY,
        action=effect,
    )
    return Champion(
        effects=watcher,
        cardcode="02BW026T3",
        champion_spell=Set2Spells.PickaCard,
    )


# When I Level Up, Obliterate the enemy deck, leaving 4 non-champions.Round Start: Summon a Sapling.
def Maokai():
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Maokai2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.DRAW,
        threshold=25,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    #TODO multiple
    toss = TossEffect(quantity=2)
    create = CreateCardEffect(Set2Units.Sapling, location=LocEnum.HOMEBASE)
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        action=[toss, create],
        activations_per_round=1
    )
    return Champion(
        effects=[watcher, ta],
        cardcode="02SI008",
        champion_spell=Set2Spells.SapMagic,
    )


    k = min(4, len(self.opponent.deckcards))
    remaining = sample(self.opponent.deckcards(lambda x: not is_champion(x)), k=k)
    [obliterate(st) for st in self.opponent.deckcards() if st not in k]


def Maokai2():
    #TODO
    effect = ObliterateEffect(target=...)
    create = CreateCardEffect(Set2Units.Sapling, location=LocEnum.HOMEBASE)

    ta1 = TriggeredAction(
        event_filter=EntityEvents.LEVEL_UP,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
        activate_once=True,
    )
    return Champion(
        effects=ta1,
        round_start_effects=create,
        cardcode="02SI008T2",
        champion_spell=Set2Spells.SapMagic,
    )

def MissFortune():
    effect = PlaySkill(target=Set2Skills.LoveTap)
    watcher = TriggeredAction(
        event_filter=EntityEvents.PLAYER_ATTACK_COMMIT,
        ally_enum=OriginEnum.T_ALLY,
        action=effect,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Gangplank2)
    levelwatcher = ValueTriggeredAction(
        event_filter=EntityEvents.PLAYER_ATTACK_COMMIT,
        threshold=4,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(
        effects=[watcher, levelwatcher],
        cardcode="02BW022",
        champion_spell=Set2Spells.BulletTime,
    )


# When allies attack, deal 1 three times to all battling enemies and the enemy Nexus.
def MissFortune2():
    effect = PlaySkill(target=Set2Skills.BulletTime)
    watcher = TriggeredAction(
        event_filter=EntityEvents.PLAYER_ATTACK_COMMIT,
        ally_enum=OriginEnum.T_ALLY,
        action=effect,
    )
    return Champion(
        effects=watcher,
        cardcode="02BW022T2",
        champion_spell=Set2Spells.BulletTime,
    )


# When you cast a spell, stop all enemy spells and skills targeting me and give me Elusive this round.Nexus Strike: Create a Chum the Waters in hand.
def Fizz():
    # TODO
    effect = NegateSpell(target=...)
    effect1 = AddKeywordEffect(
        target=AutoEntitySelector.SELF, keyword=KeywordEnum.ELUSIVE
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL,
        ally_enum=OriginEnum.T_ALLY,
        action=[effect, effect1],
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Quinn2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL,
        threshold=6,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        instance_bound=False,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(
        effects=[watcher, ta],
        cardcode="02BW046",
        champion_spell=Set2Spells.PlayfulTrickster,
    )


def Fizz2():
    effect = NegateSpell(target=...)
    effect1 = AddKeywordEffect(
        target=AutoEntitySelector.SELF, keyword=KeywordEnum.ELUSIVE
    )
    effect2 = CreateCardEffect(Set2Spells.ChumtheWaters)
    ta = TriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL,
        ally_enum=OriginEnum.T_ALLY,
        action=[effect, effect1],
    )
    return Champion(
        effects=ta,
        nexus_strike_effect=effect2,
        cardcode="02BW046T3",
        champion_spell=Set2Spells.PlayfulTrickster,
    )


def Swain():
    damage = DamageEffect(target=TargetPlayer.OPPONENT, value=3)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Swain2)
    levelwatcher = ValueTriggeredAction(
        event_filter=EntityEvents.DAMAGE,
        threshold=12,
        action_on_value=levelup,
        ally_enum=OriginEnum.O_ALLY,
        condition=...,
        instance_bound=False,
        event_counter=EventCounterEnum.COUNT_VALUE,
    )
    return Champion(
        effects=levelwatcher,
        nexus_strike_effect=damage,
        cardcode="02NX007",
        champion_spell=Set2Spells.RavenousFlock,
    )


# When you deal non-combat damage to the enemy Nexus, Stun the strongest backrow enemy.
# Nexus Strike: Deal 3 to all enemies and the enemy Nexus.
def Swain2():
    stun = StunEffect(
        target=CardFilter(
            owner=TargetPlayer.OPPONENT,
            location=LocEnum.HOMEBASE,
            sorter=CardSorter.STRONGEST,
        )
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.DAMAGE,
        ally_enum=OriginEnum.T_OPPONEXUS_O_ALLY,
        condition=...,
        action=stun,
    )
    damage = DamageEffect(
        target=AutoEntitySelector.OPPONENT_NEXUS_AND_BOARD_UNITS, value=3
    )
    return Champion(
        effects=ta,
        nexus_strike_effect=damage,
        cardcode="02NX007T2",
        champion_spell=Set2Spells.RavenousFlock,
    )
