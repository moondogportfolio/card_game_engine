from random import choice
import Sets.SET1.Units as Set1Units
import Sets.SET1.Spells as Set1Spells
import Sets.SET2.Spells as Set2Spells
import Sets.SET2.Units as Set2Units
import Sets.SET3.Units as Set3Units
import Sets.SET3.Spells as Set3Spells
import Sets.SET4.Units as Set4Units
import Sets.SET5.Units as Set5Units
import Sets.SET4.Landmarks as Set4Landmarks
import Sets.SET5.Landmarks as Set5Landmarks
import Sets.SET5.Champions as Set5Champions

import Sets.SET6.Equipments as Set6Equipments
from actions.action_modifiers.silence import SilenceEffect
from actions.activations.copy_spell import CopySpellWithSameTargets
from actions.activations.multiple_activations import MultipleActivationsEffect
from actions.activations.negate_spell import NegateSpell
from actions.attachments.destroy import DestroyAttachmentsEffect, DestroyEquipEffect
from actions.attachments.equip import EquipEffect
from actions.attachments.forge import ForgeEffect
from actions.attachments.improvise import ImproviseEffect
from actions.attachments.transfer_equip import TransferEquipmentEffect
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
from actions.keywords.remove_keyword import (
    
    RemoveKeywordEffect,
)
from actions.keywords.stun_effect import StunEffect
from actions.meta.create_ta import CreateTriggeredAction
from actions.movement.capture import CaptureEffect
from actions.movement.discard import DiscardEffect
from actions.movement.draw import DrawEffect, TargetedDrawAction
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
from actions.reactions.action_negator import ActionNegator
from actions.reactions.action_replacement import ActionReplacement
from actions.reactions.dynamic_attr_modifier import (
    DynamicAttackModifier,
    DynamicCostModifier,
    DynamicKeywordModifier,
)
from actions.reactions.event_filter import EventFilter
from actions.reactions.triggered_action import AllyOrigin_TA, TriggeredAction
from actions.reactions.value_triggered_action import ValueTriggeredAction
from actions.requisite.action_requisite import ActionRequisite
from actions.transform.transform import TransformEffect
from actions.traps.set_trap import (
    ActivateBoons,
    PlantChimes,
    PlantFlashBombTrap,
    PlantMysteriousPortalEffect,
    SetTrapEffect,
    TrapMultiplier,
)
from card_classes.spell import Spell
from card_classes.unit import Unit
from conditions.base_condition import Condition
from entity_selectors.base_card_filter import (
    BaseCardFilter,
    InvokeBaseCardFilter,
    ManifestBaseCardFilter,
)
from entity_selectors.card_filter import (
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
from value.entity_attribute import EntityAttribute


# To play, discard 1. Kill the weakest enemy.
def RoaroftheSlayer():
    effect = DiscardEffect(target=TargetShorthand.ALLIED_HAND_CARD)
    effect2 = KillAction(target=AutoEntitySelector.WEAKEST_OPPONENT_UNIT)
    return Spell(activation_effect=effect2, play_requisite=effect)


# Destroy one of your mana gems to deal 4 to a unit.
def RiteoftheArcane():
    destroy_lm = DestroyLandmarkEffect(target=TargetShorthand.ALLIED_LANDMARK)
    damage_effect = DamageEffect(value=4, target=TargetShorthand.ANY_BOARD_UNIT)
    destroy_mana = DestroyManaGem(target=TargetPlayer.ORIGIN_OWNER)
    effect = ...
    return Spell(activation_effect=effect)


# Deal 2 to a unit and plant 2 Flashbomb Traps randomly in the top 10 cards of the enemy deck.
def PiltoverPeacemaker():
    effect = DamageEffect(value=2, target=TargetShorthand.ANY_BOARD_UNIT)
    effect1 = PlantFlashBombTrap(quantity=2)
    return Spell(activation_effect=[effect, effect1])


# Pick an ally being targeted by enemy Fast spells, Slow spells, or Skills with only 1 target. Stop them.
def MemorysCloak():
    effect = TargetEntity(choices=...)
    effect2 = StackSpellFilter()
    effect = NegateSpell(
        target=...,
    )
    # TODO
    return Spell(activation_effect=effect)


# Recall an ally to deal 2 to anything.
def LightningRush():
    target_obj = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = RecallEffect(target=target_obj)
    effect1 = DamageEffect(
        target=TargetShorthand.ANYTHING,
        target_exclusion=target_obj,
        fizz_if_fail=effect,
    )
    return Spell(activation_effect=[effect, effect1])


# ALL players draw 2.
def InsiderKnowledge():
    effect = DrawEffect(quantity=2, player=TargetPlayer.ALL_PLAYERS)
    return Spell(activation_effect=effect)


# Give two allies +2|+1 this round.
def HeroicRefrain():
    effect = BuffEffect(
        target=TargetEntity(choices=CardFilter(), quantity=2),
        attack=2,
        health=1,
        round_only=True,
    )
    return Spell(activation_effect=effect)


# Create a Hungry Owlcat in hand, then grant Fae allies in hand +1|+1.
def FaeAid():
    effect1 = CreateCardEffect(target=Set5Units.HungryOwlcat)
    effect = BuffEffect(
        target=CardFilter(location=LocEnum.HAND, subtype=SubTypes_.FAE),
        attack=1,
        health=1,
    )
    return Spell(activation_effect=[effect1, effect])


# Deal 1 to two enemies.
def BouncingBomb():
    effect1 = DamageEffect(value=2, target=TargetShorthand.OPPONENT_BOARD_UNIT)
    effect2 = DamageEffect(
        value=1,
        target=TargetEntity(
            quantity=2, minimum=2, choices=CardFilter(owner=TargetPlayer.OPPONENT)
        ),
    )
    effect = ChoiceAction(choices=[effect1, effect2])
    return Spell(activation_effect=effect)


# If your opponent has more units than you, grant an ally +1|+1 for each extra unit they have.
def AgainsttheOdds():
    # value = DerivedValue(
    #     target=CardFilter(owner=TargetPlayer.OPPONENT),
    #     evaluator=DerivingFunction.COUNT,
    # )
    # value2 = DerivedValue(target=CardFilter(), evaluator=DerivingFunction.COUNT)
    # req = ActionRequisite(
    #     requisite=Condition(
    #         target=value2,
    #         condition=PlayerFlags.IS_GREATER_THAN,
    #         parameter=value,
    #     )
    # )
    # value3 = DerivedValue(
    #     target=value2, evaluator=DerivingFunction.SUBTRACT, parameter=value
    # )
    # effect = BuffEffect(
    #     target=TargetShorthand.ALLIED_BOARD_UNIT, attack=value3, health=value3
    # )
    # self.add_activation_effect(effect=[effect, req])
    effect = ...
    # TODO
    return Spell(activation_effect=effect)


# Your opponent discards their lowest cost card.
def TricksyTentacles():
    target = CardFilter(
        owner=TargetPlayer.OPPONENT,
        location=LocEnum.HAND,
        sorter=CardSorter.CHEAPEST,
        quantity=1,
    )
    effect = DiscardEffect(target=target)
    return Spell(activation_effect=effect)


# Grant an ally +1|+1 and Stun an enemy.
def ShieldVault():
    effect = BuffEffect(target=TargetShorthand.ALLIED_BOARD_UNIT, attack=1, health=1)
    effect1 = StunEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT)
    return Spell(activation_effect=[effect, effect1])


# To play, discard a card.Summon a Reborn Grenadier and give it +2|+0 this round.
def SaltAndStitches():
    effect = DiscardEffect(target=TargetShorthand.ALLIED_HAND_CARD)
    effect2 = CreateCardEffect(
        target=Set5Units.RebornGrenadier, location=LocEnum.HOMEBASE
    )
    effect3 = BuffEffect(
        # target=PostEventParamGetter(
        #     effect=effect2, parameter=PostEventParameter.CREATED_CARD
        # ),
        attack=2,
        health=0,
        round_only=True,
    )
    # TODO postevent
    return Spell(activation_effect=[effect2, effect3], play_requisite=effect)


# Recall a unit with 3 or less Power.
def Quicken():
    effect = RecallEffect(
        target=TargetEntity(choices=CardFilter(owner=None, attack=(0, 3)))
    )
    return Spell(activation_effect=effect)


# Grant an ally +1|+0. Deal 1 to an enemy.
def ProwlingProjectile():
    effect = BuffEffect(target=TargetShorthand.ALLIED_BOARD_UNIT, attack=1)
    effect1 = DamageEffect(value=1, target=TargetShorthand.OPPONENT_BOARD_UNIT)
    return Spell(activation_effect=[effect, effect1])


# Deal 1 to anything. Draw 1.
def PokeyStick():
    effect = DamageEffect(value=1, target=TargetShorthand.ANYTHING)
    effect1 = DrawEffect()
    return Spell(activation_effect=[effect, effect1])


# Grant an ally +2|+0 and Impact.
def Flamespitter():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT, attack=2, keyword=KeywordEnum.IMPACT
    )
    return Spell(activation_effect=effect)


# Pick 1 of 3 units from the enemy deck and plant 3 Poison Puffcaps on all copies of it.
def Entrapment():
    target = TargetEntity(
        quantity=3,
        automatic=True,
        choices=CardFilter(type=[Types_.SPELL, Types_.UNIT], flatten_to_type=True),
    )
    filter_obj = CardFilter(location=LocEnum.DECK, card_class=...)
    effect = SetTrapEffect(target=filter_obj, quantity=3, each=True)
    # TODO
    return Spell(activation_effect=effect)


# To play, discard 1. Deal 2 to a unit and 2 to the enemy Nexus.
def ElectroHarpoon():
    effect = DiscardEffect(target=TargetShorthand.ALLIED_HAND_CARD)
    effect1 = DamageEffect(
        target=TargetShorthand.ANY_BOARD_UNIT,
        value=2,
        target_player=TargetPlayer.OPPONENT,
    )
    return Spell(activation_effect=effect1, play_requisite=effect)


# Deal 2 randomly to an enemy or the enemy Nexus and create a Flow in hand.
def Ebb():
    effect = DamageEffect(
        target=EntityFilter(
            owner=TargetPlayer.OPPONENT, player=TargetPlayer.OPPONENT, quantity=1
        )
    )
    effect1 = CreateCardEffect(target=Flow)
    return Spell(activation_effect=[effect, effect1])


# Heal an ally or your Nexus 2, and create an Ebb and Flow in hand.
def Flow():
    effect = HealEffect(value=2, target=TargetShorthand.ALLY_NEXUS_OR_BOARD_UNITS)
    effect1 = CreateCardEffect(target=EbbandFlow)
    return Spell(activation_effect=[effect, effect1])


# Deal 2 randomly to an enemy or the enemy Nexus and heal an ally or your Nexus 2.
def EbbandFlow():
    # ebb
    effect = DamageEffect(
        target=EntityFilter(
            owner=TargetPlayer.OPPONENT, player=TargetPlayer.OPPONENT, quantity=1
        )
    )
    effect1 = HealEffect(value=2, target=TargetShorthand.ALLY_NEXUS_OR_BOARD_UNITS)
    return Spell(activation_effect=[effect, effect1])


# Recall an ally to give an enemy Vulnerable this round.
def Charm():
    effect = RecallEffect(target=TargetShorthand.ALLIED_BOARD_UNIT)
    effect1 = AddKeywordEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT,
        keyword=KeywordEnum.VULNERABLE,
        round_only=True,
        fizz_if_fail=effect,
    )
    return Spell(activation_effect=[effect, effect1])


# Give an ally +2|+0 this round. If you've added 2+ cards to your hand this round, give it Elusive this round.
def Ambush():
    target_obj = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = BuffEffect(
        target=target_obj,
        attack=2,
        health=0,
        round_only=True,
    )
    effect1 = AddKeywordEffect(
        target=target_obj,
        keyword=KeywordEnum.ELUSIVE,
        round_only=True,
        condition=...
        # condition=PlayerFlags.ALLY_DIED_THIS_ROUND,
    )
    return Spell(activation_effect=[effect, effect1])


# Manifest an Otterpus or one of 2 spells from your regions that cost 3 or less.
def TrinketTrade():
    candidates = BaseCardFilter(
        type=Types_.SPELL, owner_same_regions=True, count=2, cost=(0, 3)
    )
    effect = ManifestEffect(target=[Set5Units.Otterpus, candidates])
    return Spell(activation_effect=effect)


# To play, discard 1.Manifest a Mecha-Yordle.
def Scrapheap():
    effect = DiscardEffect(target=TargetShorthand.ALLIED_HAND_CARD)
    effect2 = ManifestEffect(
        target=ManifestBaseCardFilter(subtype=SubTypes_.MECHA_YORDLE)
    )
    return Spell(activation_effect=effect2, play_requisite=effect)


# Grow an ally to 3|3 this round.
def PurpleberryShake():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=3,
        health=3,
        operator=Ops_.GROW,
        round_only=True,
    )
    return Spell(activation_effect=effect)


# Deal 1 to anything and plant 3 Poison Puffcaps on random cards in the enemy deck.
def PoisonDart():
    effect = DamageEffect(value=1, target=TargetShorthand.ANYTHING)
    effect1 = SetTrapEffect(quantity=3, target=TargetPlayer.OPPONENT, entire_deck=True)
    return Spell(activation_effect=[effect, effect1])


# Pick 1 of 2 non-champion cards in the enemy's hand or deck and Prank it.
def Prank():
    target = TargetEntity(
        choices=CardFilter(
            quantity=2,
            owner=TargetPlayer.OPPONENT,
            location=[LocEnum.HAND, LocEnum.DECK],
            excluding_flags=CardFlags.IS_CHAMPION,
            type=None,
        ),
    )
    effect1 = BuffCostEffect(value=2, target=..., operator=Ops_.INCREMENT)
    effect2 = BuffEffect(target=..., attack=-2)
    effect3 = BuffEffect(target=..., attack=-1, keyword=KeywordEnum.CANTBLOCK)
    effect4 = BuffEffect(target=..., attack=-1, keyword=KeywordEnum.VULNERABLE)
    effect5 = BuffEffect(target=..., attack=-2)
    effect = ChoiceAction(
        choices=[effect1, effect2, effect3, effect4, effect5], randomized=True
    )
    # TODO if only one target, target for effects (map choice to effect)
    return Spell(activation_effect=effect)


# Deal 1 to a unit. If you have 4+ allies, deal 2 instead.
def GroupShot():
    effect = DamageEffect(value=..., target=TargetShorthand.ANY_BOARD_UNIT)
    # TODO
    return Spell(activation_effect=effect)


# Manifest a Fae and grant it +1|+1.
def FaeSprout():
    effect = ManifestEffect(
        target=BaseCardFilter(subtype=SubTypes_.FAE),
        attack=(Ops_.INCREMENT, 1),
        health=(Ops_.INCREMENT, 1),
    )
    return Spell(activation_effect=effect)


# Create a Ruinous Acolyte or an Obelisk of Power in hand.
def ConstructofDesolation():
    effect2 = ChoiceBaseCard(
        choices=[Set5Units.RuinousAcolyte, Set5Landmarks.ObeliskofPower]
    )
    effect1 = CreateCardEffect(target=effect2)
    return Spell(activation_effect=effect1)


# Give an ally +2|+0 and "Round End: Recall me" this round.
def CloudStance():
    target_obj = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = BuffEffect(target=target_obj, attack=2)
    effect2 = RecallEffect(target=target_obj)
    effect3 = TriggeredAction(
        event_filter=GameStateEnums.ROUND_END,
        activate_once=True,
        action=effect2,
    )
    effect4 = CreateTriggeredAction(triggered_action=effect3)
    return Spell(activation_effect=[effect, effect4])


# Plant 2 Flashbomb Traps randomly in the top 10 cards of the enemy deck.
def AdvancedIntel():
    effect = PlantFlashBombTrap(quantity=2)
    return Spell(activation_effect=effect)


# Grant an ally +0|+3. At the next Round Start, grant it +0|+2.
def ShieldofDurand():
    target_obj = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = BuffEffect(target=target_obj, health=3)
    effect2 = BuffEffect(target=target_obj, health=2)
    effect3 = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START, activate_once=True, action=effect2
    )
    effect4 = CreateTriggeredAction(triggered_action=effect3)
    return Spell(activation_effect=effect)


# Set a unit's stats to 1|6 this round.
def StressDefense():
    effect = BuffEffect(
        target=TargetShorthand.ANY_BOARD_UNIT,
        attack=1,
        health=6,
        operator=Ops_.SET,
        round_only=True,
    )
    return Spell(activation_effect=effect)


# Deal 2 to a unit. If you've added 2+ cards to your hand this round, deal 3 to it instead.
def SumpFumes():
    value = BranchingValue(
        condition=Condition(
            target=TargetPlayer.ORIGIN_OWNER,
            condition=PlayerFlags.HAS_ADDED_CARDS_TO_HAND_THIS_ROUND,
            parameter=2,
        ),
        if_true=3,
        if_false=2,
    )
    effect = DamageEffect(value=value, target=TargetShorthand.ANY_BOARD_UNIT)
    return Spell(activation_effect=effect)


# Deal 1 to two different randomly targeted enemies and create a Crashing Wave in your deck.
def TidalWave():
    effect = DamageEffect(
        target=CardFilter(owner=TargetPlayer.OPPONENT, quantity=2),
        value=1,
    )
    effect1 = CreateCardEffect(target=CrashingWave, location=LocEnum.DECK)
    return Spell(activation_effect=[effect, effect1])


# Deal 2 to four different randomly targeted enemies and create a Colossal Wave in your deck.
def CrashingWave():
    effect = DamageEffect(
        target=CardFilter(owner=TargetPlayer.OPPONENT, quantity=4),
        value=2,
    )
    effect1 = CreateCardEffect(target=ColossalWave, location=LocEnum.DECK)
    return Spell(activation_effect=[effect, effect1])


# Deal 4 to all enemies and the enemy Nexus.
def ColossalWave():
    effect = DamageEffect(
        target=AutoEntitySelector.OPPONENT_NEXUS_AND_BOARD_UNITS,
        value=4,
    )
    return Spell(activation_effect=effect)


# Destroy an allied landmark to give an ally +4|+2 this round.
def UnleashedEnergy():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=2,
        health=1,
        round_only=True,
    )
    effect1 = DestroyLandmarkEffect(target=TargetShorthand.ALLIED_LANDMARK)
    effect2 = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=4,
        health=2,
        round_only=True,
        fizz_if_fail=effect1,
    )
    effect3 = CombinationAction(actions=[effect1, effect2])
    effect4 = ChoiceAction(choices=[effect, effect3])
    return Spell(activation_effect=effect4)


# Deal 1 to an enemy and Stun it.
def Wallop():
    target_obj = TargetEntity(choices=TargetShorthand.OPPONENT_BOARD_UNIT)
    effect = DamageEffect(value=1, target=target_obj)
    effect1 = StunEffect(target=target_obj)
    return Spell(activation_effect=[effect, effect1])


# Give 2 allies +1|+2 this round.
def WeStandTogether():
    effect = BuffEffect(
        target=TargetEntity(CardFilter(quantity=2)),
        attack=1,
        health=2,
        round_only=True,
    )
    return Spell(activation_effect=effect)


# Heal an ally to full. Then, that ally and an enemy strike each other.
def WindsofWar():
    target = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = HealEffect(target=target, value=None, heal_max=True)
    effect1 = MutualStrikeEffect(
        first_striker=target,
        second_striker=TargetShorthand.OPPONENT_BOARD_UNIT,
    )
    return Spell(activation_effect=[effect, effect1])


# Grant 2 allies +2|+2.
def BattleBonds():
    effect = BuffEffect(target=TargetEntity(quantity=2), attack=2, health=2)
    return Spell(activation_effect=effect)


# Costs 2 less if you have a Tristana or if you've summoned or cast cards from 4+ regions this game.Deal 3 to a unit.
def BusterShot():
    # TODO
    effect = DamageEffect(value=3, target=TargetShorthand.ANY_BOARD_UNIT)
    condition1 = Condition(
        target=TargetPlayer.ORIGIN_OWNER,
        condition=PlayerFlags.HAS_UNIT_ON_BOARD,
        parameter=Set5Champions.Tristana,
    )
    condition2 = Condition(
        target=TargetPlayer.ORIGIN_OWNER,
        condition=PlayerFlags.HAS_PLAYED_CARDS_FROM_DIFF_REGIONS,
        parameter=4,
    )
    condition3 = Condition(
        target=condition1, condition=PlayerFlags.OR, parameter=condition2
    )
    cost_mod = DynamicCostModifier(
        value=2, condition=condition3, target=TargetShorthand.SELF
    )
    return Spell(activation_effect=effect)


# To play, discard 1. Manifest a Yordle that costs 3 or less and summon it.
def YordlePortal():
    effect = DiscardEffect(target=TargetShorthand.ALLIED_HAND_CARD)
    effect2 = ManifestEffect(
        target=BaseCardFilter(subtype=SubTypes_.YORDLE), summon_chosen_card=True
    )
    return Spell(activation_effect=effect2, play_requisite=effect)


# Give an ally Barrier or SpellShield this round.
def Friendship():
    target_obj = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect1 = AddKeywordEffect(
        target=target_obj, keyword=KeywordEnum.SPELLSHIELD, round_only=True
    )
    effect2 = AddKeywordEffect(
        target=target_obj, keyword=KeywordEnum.BARRIER, round_only=True
    )
    effect = ChoiceAction(choices=[effect1, effect2])
    return Spell(activation_effect=effect)


# Grant an ally +2|+2 and Impact.
def PrimalStrength():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=2,
        health=2,
        keyword=KeywordEnum.IMPACT,
    )
    return Spell(activation_effect=effect)


# To play, discard 1. Grant all allies +1|+1.
def SpiritPortal():
    effect = DiscardEffect(target=TargetShorthand.ALLIED_HAND_CARD)
    effect2 = BuffEffect(target=CardFilter(), attack=1, health=1)
    return Spell(activation_effect=effect2, play_requisite=effect)


# Recall an ally. The next ally you play this round with equal or less cost, costs 0 instead.
def Transposition():
    target_obj = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect2 = CreateInternalValue(
        value=EntityAttribute(target=target_obj, attribute=Attr_.COST)
    )
    effect = RecallEffect(target=target_obj)
    effect1 = DynamicCostModifier(
        value=0,
        operator=Ops_.SET,
        condition=Condition(
            target=...,
            condition=PlayerFlags.IS_LESS_THAN_OR_EQ_TO,
            parameter=EntityAttribute(target=effect2, attribute=Attr_.INTERNAL_VALUE),
        ),
        target=TargetShorthand.ALLIED_HAND_UNIT,
    )
    # TODO
    return Spell(activation_effect=effect)


# Place an enemy follower into the enemy deck, then your opponent draws 1.
def CoupdeGrace():
    effect = MoveEffect(
        target=TargetEntity(
            choices=CardFilter(owner=TargetPlayer.OPPONENT, flags=CardFlags.IS_FOLLOWER)
        ),
        location=LocEnum.DECK,
    )
    effect1 = DrawEffect(player=TargetPlayer.OPPONENT)
    return Spell(activation_effect=[effect, effect1])


# Stun an enemy and stun all enemies with 2 or less Power.
def EventHorizon():
    effect = StunEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT)
    effect1 = StunEffect(
        target=CardFilter(attack=(0, 2), owner=TargetPlayer.OPPONENT),
        target_exclusion=effect.target,
    )
    # TODO
    return Spell(activation_effect=[effect, effect1])


# An ally strikes an enemy. If it survives, Stun it.
def HeroicCharge():
    target = TargetEntity(choices=TargetShorthand.OPPONENT_BOARD_UNIT)
    effect = StrikeEffect(
        target=target,
        striker=TargetShorthand.ALLIED_BOARD_UNIT,
    )
    effect1 = StunEffect(
        target=target,
        condition=Condition(target=target, condition=CardFlags.IS_ON_THE_BOARD),
    )
    # TODO
    return Spell(activation_effect=[effect, effect1])


# Pick a player to discard their lowest cost card to draw 3.
def MostWanted():
    target = TargetPlayerInput(choices=TargetPlayer.ALL_PLAYERS)
    effect1 = DiscardEffect(
        target=TargetEntity(
            automatic=True,
            sort_by=CardSorter.CHEAPEST,
            choices=CardFilter(
                owner=target,
                location=LocEnum.HAND,
                type=None,
            ),
        )
    )
    effect2 = DrawEffect(player=target, quantity=3)
    return Spell(activation_effect=[effect1, effect2])


# HERE


# Summon a Liminal Guardian.
def NineLives():
    effect = CreateCardEffect(Set5Units.Liminal, LocEnum.HOMEBASE)
    return Spell(activation_effect=effect)


# Grant an ally +1|+0.
def TinySpear():
    effect = BuffEffect(target=TargetShorthand.ALLIED_BOARD_UNIT, attack=1)
    return Spell(activation_effect=effect)


# Deal 1 to ALL Nexuses.
def DanceofTusks():
    effect = DamageEffect(target=TargetPlayer.ALL_PLAYERS, value=1)
    return Spell(activation_effect=effect)


# Deal 2 to an enemy.
def Darkness():
    effect = DamageEffect(value=2, target=TargetShorthand.OPPONENT_BOARD_UNIT)
    return Spell(activation_effect=effect)


# Grant an ally +0|+1.
def TinyShield():
    effect = BuffEffect(target=TargetShorthand.ALLIED_BOARD_UNIT, health=1)
    return Spell(activation_effect=effect)


# Refill your spell mana. Give an ally Elusive and +1|+1 this round.
def ShellGame():
    effect = RefillSpellMana(value=None, operator=Ops_.MAX)
    effect1 = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=1,
        health=1,
        keyword=KeywordEnum.ELUSIVE,
        round_only=True,
    )
    return Spell(activation_effect=effect)


# HERE


# Grant your allies +1|+1. Then deal 1 to EVERYTHING.
def SpiritsUnleashed():
    effect = BuffEffect(target=CardFilter(), attack=1, health=1)
    effect1 = DamageEffect(target=TargetShorthand.ANYTHING, value=1)
    return Spell(activation_effect=effect)


# Create 2 random multi-region followers in hand.
def YordleContraption():
    effect1 = DestroyLandmarkEffect(target=TargetShorthand.ANY_LANDMARK)
    effect2 = CreateCardEffect(
        target=BaseCardFilter(
            flags=[
                CardFlags.IS_MULTIREGION,
                CardFlags.IS_FOLLOWER,
            ]
        )
    )
    effect = ChoiceAction(choices=[effect1, effect2])
    return Spell(activation_effect=effect)


# Give allies +2|+2 this round. If you've summoned or cast cards from 4+ regions, give allies +4|+4 instead.
def YordlesinArms():
    value = BranchingValue(
        condition=Condition(
            target=TargetPlayer.ORIGIN_OWNER,
            condition=PlayerFlags.HAS_PLAYED_CARDS_FROM_DIFF_REGIONS,
            parameter=4,
        ),
        if_true=3,
        if_false=2,
    )
    effect = BuffEffect(
        target=CardFilter(), attack=value, health=value, round_only=True
    )
    return Spell(activation_effect=effect)


# Summon 2 Forge Workers.
def AssemblyLine():
    effect = CreateCardEffect(Set5Units.ForgeWorkers, LocEnum.HOMEBASE, quantity=2)
    return Spell(activation_effect=effect)


# An ally strikes an enemy. If the ally is multi-region, it strikes the enemy again.
def DoubleTap():
    target_obj1 = TargetEntity(choices=TargetShorthand.OPPONENT_BOARD_UNIT)
    target_obj2 = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = StrikeEffect(
        target=target_obj1,
        striker=target_obj2,
    )
    effect1 = StrikeEffect(
        target=target_obj1,
        striker=target_obj2,
        condition=Condition(target=target_obj2, condition=CardFlags.IS_MULTIREGION),
    )
    return Spell(activation_effect=[effect, effect1])


# When you draw or create me in hand or each Round Start: while I'm in your hand, transform me into a random 6+ cost spell.
def HextechAnomaly():
    form = BaseCardFilter(type=Types_.SPELL, cost=(6, 0))
    effect = TransformEffect(
        target=TargetShorthand.SELF,
        new_form=form,
        triggering_effect=[
            GameStateEnums.ROUND_START,
            EntityEvents.DRAW,
            EntityEvents.CREATE_CARD,
        ],
    )
    # TODO
    return Spell(activation_effect=effect)


# Costs 2 less if you've created 2+ cards this game. Draw 2.
def HiddenPathways():
    val = DynamicCostModifier(
        value=2,
        condition=Condition(
            target=TargetPlayer.ORIGIN_OWNER,
            condition=PlayerFlags.HAS_CREATED_X_CARDS,
            parameter=2,
        ),
    )
    effect = DrawEffect(quantity=2)
    return Spell(activation_effect=effect, effects=val)


# Place an enemy unit on top of the enemy deck.
def KeepersVerdict():
    effect = MoveEffect(
        location=LocEnum.DECK,
        target=TargetShorthand.OPPONENT_BOARD_UNIT,
        index=0,
    )
    return Spell(activation_effect=effect)


# Transform a unit into a 3|3 Mini-Minitee and Silence it.
def Minimorph():
    target = TargetEntity(choices=TargetShorthand.ANY_BOARD_UNIT)
    effect = TransformEffect(target=target, new_form=Set5Units.MiniMinitee)
    effect1 = SilenceEffect(target=target)
    return Spell(activation_effect=[effect, effect1])


# Drain 5 from a unit.
def PiercingDarkness():
    effect = DrainEffect(value=5, target=TargetShorthand.ANY_BOARD_UNIT)
    return Spell(activation_effect=effect)


# Create 2 Fleeting 0 cost Stance Swaps in hand.
def ShamansCall():
    effect = CreateCardEffect(StanceSwap, is_fleeting=True, quantity=2, cost=0)
    return Spell(activation_effect=effect)


# Grant a Stance to an ally.
def StanceSwap():
    effect = AcquireChoice(choices=CardGroups.STANCES)
    effect1 = ...
    return Spell(activation_effect=effect)


# Grant an ally +2+0 and Overwhelm.
def WildclawStance():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=2,
        keyword=KeywordEnum.OVERWHELM,
    )
    return Spell(activation_effect=effect)


# Grant an ally +2|+2.
def BearStance():
    effect = BuffEffect(target=TargetShorthand.ALLIED_BOARD_UNIT, attack=2, health=2)
    return Spell(activation_effect=effect)


# Grant an ally +0|+2 and Regeneration.
def BoarStance():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        keyword=KeywordEnum.REGENERATION,
        health=2,
    )
    return Spell(activation_effect=effect)


# Deal 1 to EVERYTHING else.
def RamStance():
    target_obj = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = DamageEffect(
        target=TargetShorthand.ANYTHING, target_exclusion=target_obj, value=1
    )
    return Spell(activation_effect=effect)


# Deal 3 to an enemy or the enemy Nexus, and 3 to another.
def ShockBlast():
    effect = DamageEffect(
        target=TargetEntity(
            quantity=2,
            choices=EntityFilter(
                player=TargetPlayer.OPPONENT,
                filter=CardFilter(owner=TargetPlayer.OPPONENT),
            ),
        ),
        value=2,
    )
    return Spell(activation_effect=effect)


# Kill a unit and give all enemies -2|-0 this round.
def DawningShadow():
    effect = KillAction(target=TargetShorthand.OPPONENT_BOARD_UNIT)
    effect1 = BuffEffect(
        target=CardFilter(owner=TargetPlayer.OPPONENT),
        attack=-2,
        health=0,
        round_only=True,
    )
    return Spell(activation_effect=[effect, effect1])


# Deal 1 to all enemies, then do it again.
def MegaInfernoBomb():
    effect = DamageEffect(target=CardFilter(owner=TargetPlayer.OPPONENT), value=1)
    effect2 = MultipleActivationsEffect(target=effect)
    return Spell(activation_effect=effect2)


# Summon a Stasis Statue to store all allied units and landmarks that died or were destroyed this round inside.
def ServitudeofDesolation():
    effect = CreateCardEffect(Set4Landmarks.StasisStatue, LocEnum.HOMEBASE)
    # TODO map for every
    return Spell(activation_effect=effect)


# Summon Ephemeral copies of the 3 strongest followers you've Recalled this game.
def ChildrenoftheForest():
    target_obj = EventQueryParamGetter(
        query=EventQuery(event=EntityEvents.RECALL),
        parameter=PostEventParameter.TARGET,
    )
    target_obj2 = TargetEntity(
        quantity=3,
        automatic=True,
        sort_by=CardSorter.STRONGEST,
        entity_pool=target_obj,
    )
    effect = CreateCardEffect(target=target_obj2, is_ephemeral=True)
    return Spell(activation_effect=effect)


# Deal 3 to a unit and summon a Trifarian Shieldbreaker.
def WeaponsoftheLost():
    effect = DamageEffect(value=3, target=TargetShorthand.ANY_BOARD_UNIT)
    effect1 = CreateCardEffect(
        target=Set1Units.TrifarianShieldbreaker, location=LocEnum.HOMEBASE
    )
    return Spell(activation_effect=[effect, effect1])


# Fill your hand with random cards. They cost 0 and areFleeting. You can only play 3 more cards this round.
def TreasuredTrash():
    effect = FillHandWithCards(
        target=BaseCardFilter(type=None), is_fleeting=True, cost=0
    )
    effect1 = ...
    # TODO
    return Spell(activation_effect=[effect, effect1])


# Give your allies +2|+0 and Quick Attack this round. If they already have it or Double Attack, give them a random keyword instead.
def AccelerationGate():
    value = BranchingValue(
        # TODO
        condition=Condition(
            target=...,
            condition=PlayerFlags.HAS_KEYWORD,
            parameter=[KeywordEnum.QUICKSTRIKE, KeywordEnum.DOUBLESTRIKE],
        ),
        if_true=KeywordEnum.RANDOM_KEYWORD,
        if_false=KeywordEnum.QUICKSTRIKE,
    )
    effect = BuffEffect(target=CardFilter(), round_only=True, attack=2, keyword=value)
    return Spell(activation_effect=...)
