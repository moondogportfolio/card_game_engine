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
from entity_selectors.choose_player import ChoosePlayer
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


# Choose target creature. Whenever that creature is dealt damage this turn,
# it deals that much damage to each other creature and each player.
def Arcbond():
    target = TargetEntity(choices=CardFilter(owner=None))
    effect = DamageEffect(
        target=AutoEntitySelector.EVERYTHING,
        target_exclusion=target,
        value=PostEventParam.VALUE,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.DAMAGE,
        ally_enum=target,
        action=effect,
        round_only=True,
    )
    effect = CreateTriggeredAction(
        triggered_action=ta, target=TargetPlayer.ORIGIN_OWNER
    )
    return Spell(activation_effect=effect)


# TODO bind input to baseaction params upon creation

# 1
# Indestructible
# 2
# As Stuffy Doll enters the battlefield, choose a player.
# 3
# Whenever Stuffy Doll is dealt damage,
# 4
# it deals that much damage to the chosen player.
# {T}: Stuffy Doll deals 1 damage to itself.


def StuffyDoll():
    # 1
    effect = ActionNegator(event_filter=EntityEvents.KILL, ally_enum=OriginEnum.T_SELF)
    effect1 = ActionNegator(event_filter=EntityEvents.DAMAGE, ally_enum=OriginEnum.T_SELF)
    # 2
    target = ChoosePlayer()
    # 3
    effect4 = DamageEffect(target=target, value=PostEventParam.VALUE)
    effect2 = TriggeredAction(
        event_filter=EntityEvents.DAMAGE,
        ally_enum=OriginEnum.T_SELF,
        action=effect4,
    )
    effect3 = DamageEffect(AutoEntitySelector.SELF, 1)
    
    return Unit(summon_effect=target, effects=(effect2, effect, effect1))