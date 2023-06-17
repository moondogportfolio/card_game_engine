import Sets.SET1.Units as Set1Units
import Sets.SET2.Units as Set2Units
import Sets.SET1.Units as Set1Spells
import Sets.SET2.Spells as Set2Spells
import Sets.SET3.Spells as Set3Spells
import Sets.SET4.Units as Set4Units
import Sets.SET4.Spells as Set4Spells
import Sets.SET5.Spells as Set5Spells
import Sets.SET5.Landmarks as Set5Landmarks
import Sets.SET6.Units as Set6Units
import Sets.SET6.Champions as Set6Champions
import Sets.SET6.Equipments as Set6Equipments
from actions.activations.copy_spell import CopySpellWithSameTargets
from actions.activations.multiple_activations import MultipleActivationsEffect
from actions.attachments.destroy import DestroyAttachmentsEffect, DestroyEquipEffect
from actions.attachments.transfer_equip import TransferEquipmentEffect
from actions.attribute.buff import BuffCostEffect, BuffEffect
from actions.attribute.damage import DamageEffect
from actions.attribute.frostbite import FrostbiteEffect
from actions.attribute.refill_mana import RefillManaEffect, RefillSpellMana
from actions.common.strike import MutualStrikeEffect, StrikeEffect
from actions.create.bladedance import BladedanceEffect

from actions.create.create_card import CreateCardEffect
from actions.create.create_hand_cards import GenerateCoinEffect, ReforgeEffect
from actions.create.invoke import InvokeEffect
from actions.create.manifest import ManifestEffect
from actions.create.post_events import CreatePostActParams
from actions.create.summon_specific_cards import SpawnEffect, SummonHuskEffect
from actions.keywords.add_keyword import AddKeywordEffect
from actions.create.tellstones import TellstonesEffect
from actions.keywords.remove_keyword import PurgeKeywordsEffect
from actions.keywords.stun_effect import StunEffect
from actions.meta.create_ta import CreateTriggeredAction
from actions.movement.capture import CaptureEffect
from actions.movement.discard import DiscardEffect
from actions.movement.draw import DrawEffect
from actions.movement.kill import KillAction
from actions.movement.obliterate import ObliterateEffect
from actions.movement.predict import PredictEffect
from actions.movement.recall import RecallEffect
from actions.movement.revive import ReviveEffect
from actions.movement.summon import SummonEffect
from actions.movement.toss import TossEffect
from actions.on_play.plunder import PlunderEffect
from actions.postevent import PostEventParamGetter
from actions.reactions.action_replacement import ActionReplacement
from actions.reactions.dynamic_attr_modifier import DynamicCostModifier
from actions.reactions.event_filter import EventFilter
from actions.reactions.triggered_action import AllyOrigin_TA, TriggeredAction
from actions.traps.set_trap import (
    PlantChimes,
    PlantMysteriousPortalEffect,
    SetTrapEffect,
)
from card_classes.spell import Spell
from card_classes.unit import Unit
from entity_selectors.base_card_filter import BaseCardFilter, InvokeBaseCardFilter
from entity_selectors.card_filter import CardFilter
from entity_selectors.input import ChoiceAction
from enums.counters import TrapEnums
from enums.entity_events import EntityEvents
from enums.keywords import KeywordEnum
from enums.gamestate import GameStateEnums
from enums.location import LocEnum
from enums.operator import Ops_
from enums.origin_enum import OriginEnum
from enums.types import Types_
from resolvable_enums.active_cards_selector import TargetShorthand
from resolvable_enums.auto_card_selector import AutoEntitySelector
from resolvable_enums.card_conditions import CardFlags
from resolvable_enums.player_conditions import PlayerFlags
from resolvable_enums.target_player import TargetPlayer



# Deal 1 to the enemy Nexus.
# The next time an ally strikes the Nexus this round, create an Stylish Shot in hand.

def StylishShot():
    effect = DamageEffect(value=1, target=TargetPlayer.OPPONENT)
    create = CreateCardEffect(target=...)
    ta = AllyOrigin_TA(event_filter=EntityEvents.NEXUS_STRIKE, action=create)
    effect1 = CreateTriggeredAction(triggered_action=ta)
    return Spell(activation_effect=[effect, effect1])


# Plunder: I cost 1 less.
# Deal 1 to anything and Stun an enemy.


def Pirouette():
    effect = DamageEffect(value=1, target=TargetShorthand.ANYTHING)
    effect1 = StunEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT)
    effect2 = DynamicCostModifier(value=1, condition=PlayerFlags.PLUNDER)
    # TODO
    return Spell(activation_effect=[effect, effect1])


# Deal 1 to the enemy Nexus or give an ally Challenger this round.


def Flair():
    effect = DamageEffect(target=TargetPlayer.OPPONENT, value=1)
    effect1 = AddKeywordEffect(keyword=KeywordEnum.CHALLENGER, round_only=True)
    effect2 = ChoiceAction(choices=(effect, effect1))
    # PLAY ALTERNATE
    return Spell(activation_effect=effect2)



# Give an ally +2|+0 this round.
# Plunder: Give it +2|+2 instead.
# Create a Samira in your deck.
def SamirasAllOut():
    effect = ...
    return Spell(activation_effect=effect)


# Give an ally +2|+0 this round.
# Plunder: Give it +2|+2 instead.
def AllOut():
    effect = BuffEffect(target=...)
    effect1 = ...

    return Spell(activation_effect=effect)


# Recall an ally and create a Coin in hand, or spend 5 mana to
# Recall an enemy and create a Coin in hand.
def TagOut():
    effect = ...
    return Spell(activation_effect=effect)


# Coins stack.
# Refill 1 mana.
def Coin():
    effect = RefillManaEffect()
    return Spell(activation_effect=effect)


# Obliterate an enemy. Deal 1 to all other enemies and the enemy Nexus.
def ShowStopper():
    effect = ObliterateEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT)
    effect1 = DamageEffect
    return Spell(activation_effect=effect)


def ta(target):
    ObliterateEffect(target=target)
    DamageEffect(
        value=1,
        target_exclusion=target,
        target=AutoEntitySelector.OPPONENT_NEXUS_AND_BOARD_UNITS,
    )


# Stun 2 enemies and create a Coin in hand.
# Create a Sett in your deck.
def SettsFacebreaker():
    effect = ...
    return Spell(activation_effect=effect)


# Draw 2 and create 2 Coins in hand.
def PlaceYourBets():
    effect1 = DrawEffect(quantity=2)
    effect = CreateCardEffect(target=Coin, quantity=2)
    return Spell(activation_effect=effect)


# Recall an ally and create a Coin in hand.
def TagOut():
    effect = ...
    return Spell(activation_effect=effect)


# Recall an enemy and create a Coin in hand.
def TagOut():
    effect = ...
    return Spell(activation_effect=effect)


# Stun 2 enemies and create a Coin in hand.
def Facebreaker():
    target = CardFilter(quantity=2, owner=TargetPlayer.OPPONENT, location=LocEnum.BOARD)
    effect = StunEffect()
    effect1 = GenerateCoinEffect()
    return Spell(activation_effect=effect)


# Deal 2 to a unit. If this kills it, create 2 Coins in hand.
# Create a Jack in your deck.
def JacksRiskyVenture():
    effect = ...
    return Spell(activation_effect=effect)


# Deal 2 to a unit. If this kills it, create 2 Coins in hand.
def RiskyVenture():
    effect = DamageEffect(
        value=2,
    )
    effect1 = CreateCardEffect(target=..., quantity=2)
    return Spell(activation_effect=effect)


# Plunder: I cost 2 less.
# Draw 2 at the next Round Start and give them Fleeting.
def BarbedChain():
    effect = DrawEffect(quantity=2, is_fleeting=True)
    effect1 = PlunderEffect(action=...)
    return Spell(activation_effect=effect)


# An ally and an enemy strike each other. They can't drop below 1 Health from this strike.
def PrizeFight():
    s1 = TargetShorthand.ALLIED_BOARD_UNIT
    S2 = TargetShorthand.OPPONENT_BOARD_UNIT
    effect = MutualStrikeEffect()
    return Spell(activation_effect=effect)


# Kill a follower with 3 or less Power, or spend 4 mana to kill a champion with 3 or less Power.


def SoulHarvest():
    effect = ...
    return Spell(activation_effect=effect)


# Kill a champion with 3 or less Power.
def SoulHarvest():
    target = CardFilter(
        owner=None, location=LocEnum.BOARD, is_follower=False, attack=(0, 3)
    )
    effect = KillAction()
    return Spell(activation_effect=effect)


# Kill a follower with 3 or less Power.
def SoulHarvest():
    target = CardFilter(
        owner=None, location=LocEnum.BOARD, is_follower=True, attack=(0, 3)
    )
    effect = KillAction()
    return Spell(activation_effect=effect)


# Kill ALL units with 3 or less Power.
def Eradication():
    target = CardFilter(owner=None, location=LocEnum.BOARD, attack=(0, 3))
    effect = KillAction()
    return Spell(activation_effect=effect)


# Deal 1 to a unit. Create a Perilous Pastry in hand.
def PieToss():
    effect = DamageEffect(target=TargetShorthand.ANYTHING, value=1)
    return Spell(activation_effect=effect)


# Deal 1 to anything.
def PerilousPastry():
    effect = DamageEffect(target=TargetShorthand.ANYTHING, value=1)
    return Spell(activation_effect=effect)


# Deal 4 to an enemy that attacked this round or is Stunned.
def FallingStar():
    effect = DamageEffect(target=...)
    return Spell(activation_effect=effect)


# An ally with 4+ Power Captures a unit or an ally Captures a landmark.
def SearchWarrant():
    effect = ...
    return Spell(activation_effect=effect)


# Give an ally +2|+2 this round.
def FormUp():
    effect = BuffEffect(target=TargetShorthand.ALLIED_BOARD_UNIT, attack=2, health=2, round_only=True)
    return Spell(activation_effect=effect)


# An ally Captures a landmark.
def SearchWarrant():
    effect = CaptureEffect(
        target=TargetShorthand.ANY_LANDMARK, storage=TargetShorthand.ANY_ALLIED_UNIT
    )
    return Spell(activation_effect=effect)


# An ally with 4+ Power Captures a unit.
def SearchWarrant():
    captor = CardFilter(attack=(4, 0))
    effect = CaptureEffect(
        target=TargetShorthand.ANY_BOARD_UNIT, storage=captor, target_exclusion=captor
    )
    return Spell(activation_effect=effect)


