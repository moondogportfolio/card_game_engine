from random import choice
import Sets.SET1.Units as Set1Units
import Sets.SET1.Spells as Set1Spells
import Sets.SET2.Spells as Set2Spells
import Sets.SET2.Units as Set2Units
import Sets.SET3.Units as Set3Units
import Sets.SET3.Spells as Set3Spells
import Sets.SET6.Spells as Set6Spells
import Sets.SET4.Units as Set4Units
import Sets.SET5.Units as Set5Units
import Sets.SET4.Landmarks as Set4Landmarks
import Sets.SET5.Landmarks as Set5Landmarks
import Sets.SET1.Champions as Set1Champions
import Sets.SET5.Spells as Set5Spells

import Sets.SET6.Units as Set6Units
import Sets.SET6.Champions as Set6Champions

import Sets.SET6.Equipments as Set6Equipments
from actions.action_modifiers.silence import SilenceEffect
from actions.activations.copy_spell import CopySpellWithSameTargets
from actions.activations.countdown import CountdownEffect
from actions.activations.multiple_activations import MultipleActivationsEffect
from actions.activations.negate_spell import NegateSpell
from actions.activations.recast_spell import RecastSpell, RecastEventOfAction
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
    PlantPuffcaps,
    SetTrapEffect,
    TrapMultiplier,
)
from card_classes.landmark import Landmark
from card_classes.spell import Spell
from card_classes.unit import Unit
from conditions.base_condition import AttributeCondition, Condition
from entity_selectors.base_card_filter import (
    BaseCardFilter,
    InvokeBaseCardFilter,
    ManifestBaseCardFilter,
)
from entity_selectors.card_filter import (
    CardFilter,
    CardFilterSelector,
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


# When I'm summoned, summon a Back Alley Barkeep.Your new cards cost 1 less.
def BackAlleyBar():
    effect = CreateCardEffect(
        target=Set1Units.BackAlleyBarkeep,
        location=LocEnum.HOMEBASE,
    )
    effect1 = DynamicCostModifier(
        value=1,
        target=CardFilter(
            type=None, flags=CardFlags.IS_NEW_CARD, location=LocEnum.HAND
        ),
    )
    return Landmark(effects=effect1, summon_effect=effect)


# Countdown 2: Create a Treasure of the Sands in hand.
def BuriedArmory():
    effect = CreateCardEffect(target=Set6Equipments.TreasureoftheSands)
    effect1 = CountdownEffect(effect=effect, countdown=2)
    return Landmark(effects=effect1)


# When you summon a champion, destroy me to grant it +2|+1 and SpellShield.
def ChamberofRenewal():
    effect = DestroyLandmarkEffect(target=AutoEntitySelector.SELF)
    effect1 = BuffEffect(
        target=PostEventParam.TARGET,
        attack=2,
        health=1,
        keyword=KeywordEnum.SPELLSHIELD,
        fizz_if_fail=effect,
    )
    effect2 = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        activate_once=True,
        action=(effect, effect1),
    )
    return Landmark(effects=effect2)


# Countdown 3: Summon Inviolus Vox.
def DragonRoost():
    effect = CreateCardEffect(target=Set3Units.InviolusVox, location=LocEnum.HOMEBASE)
    effect1 = CountdownEffect(effect=effect, countdown=3)
    return Landmark(effects=effect1)


# Countdown 2: Revive the strongest dead ally.
def HauntedTomb():
    effect = ReviveEffect(target=AutoEntitySelector.STRONGEST_DEAD_ALLY)
    effect1 = CountdownEffect(effect=effect, countdown=2)
    return Landmark(effects=effect1)


# When I'm summoned, draw an equipment.
# The first time each round an unequipped ally is Equipped,
# refill 1 spell mana and grant them +1|+0.
def Mistfall():
    effect = DrawEffect(
        filter_obj=DrawCardFilter(filter=CardFilter(type=Types_.EQUIPMENT)),
    )
    effect1 = RefillSpellMana()
    effect2 = BuffEffect(
        target=PostEventParam.TARGET,
        attack=1,
    )
    effect3 = TriggeredAction(
        event_filter=EntityEvents.IS_EQUIPPED_WITH,
        condition=...,  # TODO unequipped
        ally_enum=OriginEnum.T_ALLY,
        activations_per_round=1,
        action=[effect1, effect2],
    )
    return Landmark(effects=effect3, summon_effect=effect)


# When I'm summoned or when I count down, plant 3 Chimes on random cards in your deck.
# Countdown 2: Draw 1.
def MysticVortex():
    effect = PlantChimes(
        quantity=3,
        entire_deck=True,
    )
    effect2 = DrawEffect()
    effect1 = CountdownEffect(effect=(effect, effect2), countdown=2)
    return Landmark(effects=effect1, summon_effect=effect)


# When I am summoned, or when you gain the attack token, summon a Ghastly Band.
def OpulentFoyer():
    effect = CreateCardEffect(target=Set6Units.GhastlyBand)
    effect1 = TriggeredAction(
        event_filter=EntityEvents.GAIN_ATTACK_TOKEN,
        ally_enum=OriginEnum.ALLY,
        action=effect,
    )
    return Landmark(effects=effect1, summon_effect=effect)


# When I'm summoned or Round Start: Create a Fleeting Time and Dedication in hand.
def OrnnsForge():
    effect = CreateCardEffect(
        target=Set6Spells.TimeandDedication,
        is_fleeting=True,
    )
    effect1 = TriggeredAction(event_filter=GameStateEnums.ROUND_START, action=effect)
    return Landmark(effects=effect1, summon_effect=effect)


# ALL spells cost 2 more.Countdown 2.
def PetricitePillar():
    effect1 = DynamicCostModifier(
        value=2, operator=Ops_.INCREMENT, target=AutoEntitySelector.ALL_HAND_SPELLS
    )
    effect = CountdownEffect(countdown=2)
    return Landmark(effects=[effect1, effect])


# Countdown 12: Create a Tybaulk in hand.
# I advance 1 round for each Fast spell, Slow spell, or Skill you've played this game.
def RavenbloomConservatory():
    effect = CreateCardEffect(target=Set6Units.Tybaulk)
    effect1 = CountdownEffect(effect=effect, countdown=12)
    effect2 = AdvanceCountdownEffect(target=AutoEntitySelector.SELF)
    effect3 = TriggeredAction(
        event_filter=EntityEvents.PLAY_FAST_OR_SLOW_OR_SKILL, action=effect
    )
    # TODO
    return Landmark(effects=[effect1, effect3])


# When I'm discarded, summon me. When you summon a Mecha-Yordle, grant it a random keyword.
def SkrappysPartsapalooza():
    effect = AddRandomKeywordEffect(target=PostEventParam.TARGET)
    effect1 = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        condition=Condition(
            target=PostEventParam.TARGET,
            condition=CardFlags.IS_SUBTYPE_X,
            parameter=SubTypes_.MECHA_YORDLE,
        ),
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        action=effect,
    )
    summon = SummonEffect(target=AutoEntitySelector.SELF)
    effect3 = ActionReplacement(
        event_filter=EntityEvents.DISCARD,
        ally_enum=OriginEnum.T_SELF,
        replacement_action=summon,
    )
    return Landmark(effects=[effect3, effect1])


# When you slay a unit, reduce the cost of the next Darkin Unit you play by 1.
def TheAltarofBlood():
    # TODO dynamic cost?
    effect = DynamicCostModifier(
        target=FutureTargetGameCard(
            filter=BaseCardFilter(subtype=SubTypes_.DARKIN), event=EntityEvents.PLAY
        ),
        value=1,
    )
    effect1 = TriggeredAction(
        event_filter=EntityEvents.SLAY,
        action=effect,
        ally_enum=OriginEnum.T_OPPO_O_ALLY,
    )
    return Landmark(effects=effect1)


# When an ally with 5+ Power dies, create a random follower with 5+ Power in hand.
def TheGrayApothecary():
    effect = CreateCardEffect(target=BaseCardFilter(attack=(5, 0), is_follower=True))
    effect1 = TriggeredAction(
        event_filter=EntityEvents.DIE,
        ally_enum=OriginEnum.T_ALLY,
        action=effect,
        condition=AttributeCondition(
            target=PostEventParam.TARGET,
            condition=CardFlags.ATTACK_REACHES_AMOUNT,
            parameter=5
        ),
    )
    return Landmark(effects=effect1)


# When an ally with an attachment attacks, grant that attachment +1|+0.
def ThePapertree():
    effect = BuffEffect(target=PostEventParam.TARGET, attack=1, send_to_attachment=True)
    effect1 = TriggeredAction(
        event_filter=EntityEvents.ATTACK_COMMIT,
        ally_enum=OriginEnum.T_ALLY,
        action=effect,
        condition=CardFlags.HAS_ATTACHMENT,
    )
    return Landmark(effects=effect1)


# Each round, the first time an ally with 5+ Power attacks, Rally.
def TrifarianTrainingPits():
    effect = RallyEffect()
    effect1 = TriggeredAction(
        event_filter=EntityEvents.PLAYER_ATTACK_COMMIT,
        ally_enum=OriginEnum.T_ALLY,
        activations_per_round=1,
        action=effect,
        condition=...,
    )
    return Landmark(effects=effect1)


# When I'm summoned, draw a Yasuo and Stun the strongest enemy.
# When you gain the attack token, Stun the strongest enemy.
def WindsweptHillock():
    effect1 = DrawEffect(filter_obj=BaseCardFilter(card_class=Set1Champions.Yasuo))
    effect2 = StunEffect(target=AutoEntitySelector.STRONGEST_OPPONENT_BOARD_UNIT)
    effect = TriggeredAction(
        event_filter=EntityEvents.GAIN_ATTACK_TOKEN,
        ally_enum=OriginEnum.T_ALLY,
        action=effect1,
    )
    return Landmark(summon_effect=(effect1, effect2), effects=effect)
