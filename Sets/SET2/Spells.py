from random import choice
import Sets.SET1.Units as Set1Units
import Sets.SET1.Spells as Set1Spells
import Sets.SET2.Units as Set2Units
import Sets.SET6.Equipments as Set6Equipments
from actions.activations.copy_spell import CopySpellWithSameTargets
from actions.activations.multiple_activations import MultipleActivationsEffect
from actions.attachments.destroy import DestroyAttachmentsEffect, DestroyEquipEffect
from actions.attachments.equip import EquipEffect
from actions.attachments.forge import ForgeEffect
from actions.attachments.improvise import ImproviseEffect
from actions.attachments.transfer_equip import TransferEquipmentEffect
from actions.attack.free_attack import FreeAttackEffect
from actions.attribute.buff import BuffCostEffect, BuffEffect
from actions.attribute.buff_everywhere import BuffEverywhereEffect
from actions.attribute.damage import DamageEffect
from actions.attribute.drain import DrainEffect
from actions.attribute.frostbite import FrostbiteEffect
from actions.attribute.gain_mana_gem import GainManaGemEffect
from actions.attribute.heal import HealEffect
from actions.attribute.rally import RallyEffect
from actions.attribute.refill_mana import RefillSpellMana
from actions.attribute.set_attribute import SetAttribute
from actions.branching.branching_action import BranchingAction
from actions.common.strike import MutualStrikeEffect, StrikeEffect
from actions.create.bladedance import BladedanceEffect

from actions.create.create_card import CreateCardEffect
from actions.create.create_hand_cards import ReforgeEffect
from actions.create.invoke import InvokeEffect
from actions.create.manifest import ManifestEffect
from actions.create.post_events import CreatePostActParams
from actions.create.summon_specific_cards import SpawnEffect, SummonHuskEffect
from actions.keywords.add_keyword import AddKeywordEffect, AddRandomKeywordEffect
from actions.create.tellstones import TellstonesEffect
from actions.keywords.stun_effect import StunEffect
from actions.meta.create_ta import CreateTriggeredAction
from actions.movement.discard import DiscardEffect
from actions.movement.draw import DrawEffect, TargetedDrawAction
from actions.movement.kill import KillAction
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
from actions.requisite.action_requisite import ActionRequisite
from actions.transform.transform import TransformEffect
from actions.traps.set_trap import (
    ActivateBoons,
    PlantChimes,
    PlantMysteriousPortalEffect,
    SetTrapEffect,
    TrapMultiplier,
)
from card_classes.spell import Spell
from card_classes.unit import Unit
from conditions.base_condition import Condition, PostEventAttributeCondition
from entity_selectors.base_card_filter import BaseCardFilter, InvokeBaseCardFilter
from entity_selectors.card_filter import CardFilter, DrawCardFilter, EntityFilter
from entity_selectors.input import ChoiceBaseCard, Input
from entity_selectors.target_game_card import TargetEntity
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


# Toss 3.Heal all allies 3.
def SapMagic():
    effect = TossEffect(quantity=3)
    effect1 = HealEffect(value=3, target=CardFilter())
    return Spell(activation_effect=[effect, effect1])


# When drawn, costs 2 less this round.Deal 3 to a unit.
def Gotcha():
    effect = DamageEffect(value=3, target=TargetShorthand.ANY_BOARD_UNIT)
    action = BuffCostEffect(target=AutoEntitySelector.SELF, value=2, round_only=True)
    ta = TriggeredAction(
        event_filter=EntityEvents.DRAW, action=action, ally_enum=OriginEnum.T_SELF
    )
    return Spell(activation_effect=effect, effects=ta)


# When drawn, costs 1 less this round.Grant an ally +2|+1.
def PocketAces():
    action = BuffCostEffect(target=AutoEntitySelector.SELF, value=1, round_only=True)
    ta = TriggeredAction(
        event_filter=EntityEvents.DRAW, action=action, ally_enum=OriginEnum.T_SELF
    )
    effect = BuffEffect(target=TargetShorthand.ALLIED_BOARD_UNIT, attack=2, health=1)
    return Spell(activation_effect=effect, effects=ta)


# If I'm Tossed, draw me instead.
# Deal 5 to ALL units.
def Keelbreaker():
    effect1 = TargetedDrawAction(target=AutoEntitySelector.SELF)
    effect = ActionReplacement(
        event_filter=EntityEvents.TOSS,
        replacement_action=effect1,
        ally_enum=OriginEnum.T_SELF,
    )
    damage = DamageEffect(value=5, target=CardFilter(owner=None))
    return Spell(activation_effect=damage, effects=effect)


# Give an enemy Frostbite and Vulnerable this round.
def CaughtintheCold():
    effect = AddKeywordEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT,
        keyword=[KeywordEnum.FROSTBITE, KeywordEnum.VULNERABLE],
        round_only=True,
    )
    return Spell(activation_effect=effect)


# Give an ally +2|+0 this round.Create a Fleeting Vault Breaker in hand.
def VaultBreaker():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=2,
        health=0,
        round_only=True,
    )
    effect1 = CreateCardEffect(target=VaultBreaker, is_fleeting=True)
    return Spell(activation_effect=[effect, effect1])


# Give an ally +2|+0 this round.
def ResonatingStrike():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=2,
        health=0,
        round_only=True,
    )
    return Spell(activation_effect=effect)


# Summon 2 random 1 cost followers.
def DoubleTrouble():
    effect = CreateCardEffect(
        target=BaseCardFilter(quantity=2, flags=CardFlags.IS_FOLLOWER, cost=1),
        location=LocEnum.HOMEBASE,
    )
    return Spell(activation_effect=effect)


# Plunder: Recall ANY follower into your hand.
def Strongarm():
    effect = RecallEffect(target=TargetShorthand.ANY_BOARD_UNIT)
    # TODO plunder


# Grant an ally +0|+3.
def DragonsProtection():
    effect = BuffEffect(target=TargetShorthand.ALLIED_BOARD_UNIT, attack=0, health=3)
    return Spell(activation_effect=effect)


# Grant an enemy Vulnerable and summon Longtooth.
def ChumtheWaters():
    effect = AddKeywordEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT, keyword=KeywordEnum.VULNERABLE
    )
    effect1 = CreateCardEffect(target=Set2Units.Longtooth, location=LocEnum.HOMEBASE)
    return Spell(activation_effect=[effect, effect1])


# Create 5 random cards in hand. They cost 0 and are Fleeting.If I'm Tossed, draw me instead.
def TreasureTrove():
    effect1 = TargetedDrawAction(target=AutoEntitySelector.SELF, quantity=None)
    effect = ActionReplacement(
        event_filter=EntityEvents.DISCARD,
        replacement_action=effect1,
        ally_enum=OriginEnum.T_SELF,
    )
    effect2 = CreateCardEffect(
        target=BaseCardFilter(quantity=5, type=None), cost=0, is_fleeting=True
    )
    return Spell(activation_effect=effect2, effects=effect)


# Summon 2 Powder Kegs.
def MorePowder():
    effect = CreateCardEffect(
        target=Set2Units.PowderKeg, location=LocEnum.HOMEBASE, quantity=2
    )
    return Spell(activation_effect=effect)


# Grant an ally "I can't take damage or die".
def UnyieldingSpirit():
    effect = ActionNegator(
        event_filter=EntityEvents.DAMAGE, ally_enum=OriginEnum.T_SELF
    )
    effect1 = ActionNegator(event_filter=EntityEvents.DIE, ally_enum=OriginEnum.T_SELF)
    effect2 = CreateTriggeredAction(
        triggered_action=(effect, effect1), target=TargetShorthand.ALLIED_BOARD_UNIT
    )
    return Spell(activation_effect=effect2)


# Deal 1 to anything.If this kills it, deal 1 to the enemy Nexus.
def Parrrley():
    effect = DamageEffect(value=1, target=TargetShorthand.ANYTHING)
    effect1 = DamageEffect(
        value=1,
        target=TargetPlayer.OPPONENT,
        condition=Condition(target=PostEventParam.TARGET_KILLED, parameter=True),
        coevent=effect,
    )
    return Spell(activation_effect=(effect, effect1))


# Summon a random 1 cost follower.
def Jailbreak():
    effect = CreateCardEffect(
        target=BaseCardFilter(flags=CardFlags.IS_FOLLOWER, cost=1),
        location=LocEnum.HOMEBASE,
    )
    return Spell(activation_effect=effect)


# Place a card from hand into your deck to draw 2 at the next Round Start. Give them Fleeting.
def PickaCard():
    effect = MoveEffect(location=LocEnum.DECK, target=TargetShorthand.ALLIED_HAND_CARD)
    effect1 = DrawEffect(quantity=2, is_fleeting=True)
    effect3 = TriggeredAction(event=GameStateEnums.GAME_START, action=effect1)
    effect2 = CreateTriggeredAction(triggered_action=effect3)
    return Spell(activation_effect=[effect, effect2])


# Remove an attacking ally from combat to Rally.
def PlayfulTrickster():
    effect = MoveEffect(
        location=LocEnum.DECK,
        target=TargetEntity(choices=CardFilter(location=LocEnum.BATTLEFIELD)),
    )
    effect1 = RallyEffect(fizz_if_fail=effect)
    return Spell(activation_effect=[effect, effect1])


# Stun an enemy.Place that unit into the enemy deck if you have a Nautilus.
def Riptide():
    effect = StunEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT)
    effect2 = MoveEffect(location=LocEnum.DECK, target=effect.target, condition=...)
    condition = Condition(
        target=TargetPlayer.ORIGIN_OWNER,
        condition=PlayerFlags.HAS_CARD_X_ON_BOARD,
        parameter=...,
    )
    effect = BranchingAction(condition=condition, if_true=effect2, if_false=effect)
    return Spell(activation_effect=effect)


# Deal 4 to a unit if it's damaged or Stunned.
def RavenousFlock():
    damaged = CardFilter(flags=CardFlags.IS_DAMAGED, owner=None)
    stunned = CardFilter(keyword=KeywordEnum.STUN, owner=None)
    target = TargetEntity(choices=[damaged, stunned])
    effect = DamageEffect(target=target, value=4)
    return Spell(activation_effect=effect)


# Grant the top 3 units in your deck +1|+1.
# Plunder: Draw 1 of them.
def SharedSpoils():
    effect = BuffEffect(
        target=CardFilter(type=None, location=LocEnum.DECK, quantity=3),
        attack=1,
        health=1,
    )
    effect1 = ...
    return Spell(activation_effect=...)
    # TODO plunder


# Stun an enemy to summon a Tail of the Dragon.
def ConcussivePalm():
    effect = StunEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT)
    effect1 = CreateCardEffect(
        target=Set2Units.TailoftheDragon, location=LocEnum.BOARD, fizz_if_fail=effect
    )
    return Spell(activation_effect=[effect, effect1])


# Create 2 random Poros and 2 Poro Snax in hand.
def AuroraPorealis():
    effect = CreateCardEffect(target=BaseCardFilter(subtype=SubTypes_.PORO, quantity=2))
    effect1 = CreateCardEffect(target=Set1Spells.PoroSnax, quantity=2)
    return Spell(activation_effect=[effect, effect1])


# Give an ally Challenger this round.Create a Fleeting Resonating Strike in hand.
def SonicWave():
    effect = AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        keyword=KeywordEnum.CHALLENGER,
        round_only=True,
    )
    effect1 = CreateCardEffect(target=ResonatingStrike, is_fleeting=True)
    return Spell(activation_effect=[effect, effect1])


# Toss 4.
def Jettison():
    effect = TossEffect(quantity=4)
    return Spell(activation_effect=effect)


# Deal 2 to an enemy and 1 to the enemy Nexus.
def DeathsHand():
    effect = DamageEffect(value=2, target=TargetShorthand.OPPONENT_BOARD_UNIT)
    effect1 = DamageEffect(value=1, target=TargetPlayer.OPPONENT)
    return Spell(activation_effect=...)


# Deal 1 to the enemy Nexus.
def WarningShot():
    effect = DamageEffect(value=1, target=TargetPlayer.OPPONENT)
    return Spell(activation_effect=effect)


# Deal 1 to three different randomly targeted enemies or the enemy Nexus.
def MakeitRain():
    target = TargetEntity(
        choices=EntityFilter(
            owner=TargetPlayer.OPPONENT,
            player=TargetPlayer.OPPONENT
        ),
        quantity=3,
        minimum=1,
        randomize=True
    )
    effect = DamageEffect(
        value=1,
        target=target,
    )
    return Spell(activation_effect=effect)


# Plunder: Draw a random non-champion card from the enemy hand.
def SleightofHand():
    effect = DrawEffect(
        quantity=None,
        filter_obj=CardFilter(
            owner=TargetPlayer.OPPONENT,
            location=LocEnum.HAND,
            excluding_flags=CardFlags.IS_CHAMPION,
        ),
    )
    # TODO plunder
    return Spell(activation_effect=effect)


# Costs 2 less if you cast 2+ spells last round.
# Draw 2 other spells.
def DeepMeditation():
    # TODO exclusion=DeepMeditation
    effect = DrawEffect(
        DrawCardFilter(type=Types_.SPELL, location=LocEnum.DECK, quantity=2),
    )
    # TODO flow
    return Spell(activation_effect=effect, effects=...)


# Summon an ally that costs 3 or less from hand.
def Return():
    effect = SummonEffect(
        target=TargetEntity(choices=CardFilter(location=LocEnum.HAND, cost=(0, 3)))
    )
    return Spell(activation_effect=effect)


# Give an enemy Vulnerable this round. If it dies this round, draw 1.
def YeBeenWarned():
    effect = AddKeywordEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT,
        keyword=KeywordEnum.VULNERABLE,
        round_only=True,
    )
    effect1 = DrawEffect()
    effect2 = TriggeredAction(
        event_filter=EntityEvents.DIE,
        action=effect1,
        activate_once=True,
        round_only=True,
        ally_enum=OriginEnum.T_SELF,
    )
    effect3 = CreateTriggeredAction(
        target=TargetShorthand.OPPONENT_BOARD_UNIT, triggered_action=effect2
    )
    return Spell(activation_effect=(effect, effect3))


# If I'm Tossed, draw me instead.Summon 3 Vicious Platewyrms.
def PlatewyrmEgg():
    effect1 = TargetedDrawAction(target=AutoEntitySelector.SELF)
    effect = ActionReplacement(
        event_filter=EntityEvents.DISCARD,
        replacement_action=effect1,
    )
    effect2 = CreateCardEffect(
        target=Set2Units.ViciousPlatewyrm,
        location=LocEnum.HOMEBASE,
        quantity=3,
    )
    return Spell(activation_effect=effect2, effects=effect)


# Nab 1.Plunder: Nab 1 more.
def PilferedGoods():
    effect = NabEffect()
    # todo plunder
    effect1 = NabEffect(condition=...)
    return Spell(activation_effect=[effect, effect1])


# Toss 2.Draw 2.
def Salvage():
    effect = TossEffect(quantity=2)
    effect1 = DrawEffect(quantity=2)
    return Spell(activation_effect=[effect, effect1])


# An ally kicks an enemy into the enemy Nexus, striking the enemy then the enemy Nexus.
# If the enemy survives, Recall it.
def DragonsRage():
    effect = StrikeEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT,
        striker=TargetShorthand.ALLIED_BOARD_UNIT,
    )
    effect1 = StrikeEffect(
        target=TargetPlayer.OPPONENT, striker=PostEventParam.STRIKER, coevent=effect
    )
    effect2 = RecallEffect(
        target=PostEventParam.TARGET,
        condition=Condition(target=PostEventParam.TARGET_KILLED, parameter=True),
        coevent=effect,
    )

    return Spell(activation_effect=(effect, effect1, effect2))


# Pick an enemy. 2 allies strike it one after another.
def ConcertedStrike():
    effect = StrikeEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT,
        striker=TargetEntity(choices=CardFilter(), quantity=2),
    )
    return Spell(activation_effect=effect)


# Deal 2 to an enemy.
# If this kills it, deal 4 to the enemy Nexus.
def DoubleUp():
    effect = DamageEffect(value=10, target=TargetShorthand.OPPONENT_BOARD_UNIT)
    effect1 = DamageEffect(
        value=4,
        target=TargetPlayer.OPPONENT,
        condition=Condition(target=PostEventParam.TARGET_KILLED, parameter=True),
        coevent=effect,
    )
    return Spell(activation_effect=(effect, effect1))


# When drawn, costs 2 less this round.Grow an ally to 4|4.
def SuitUp():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=4,
        health=4,
        operator=Ops_.GROW,
    )
    effect1 = BuffCostEffect(target=AutoEntitySelector.SELF, value=2, round_only=True)
    effect2 = TriggeredAction(
        event_filter=EntityEvents.DRAW,
        action=effect1,
        ally_enum=OriginEnum.T_SELF,
    )
    return Spell(activation_effect=effect, effects=effect2)


# Give all allies Tough this round.
def RangersResolve():
    effect = AddKeywordEffect(
        target=CardFilter(), keyword=KeywordEnum.TOUGH, round_only=True
    )
    return Spell(activation_effect=effect)


# Summon a Sapling at the next Round Start.
def SaplingToss():
    effect = CreateCardEffect(target=Set2Units.Sapling, location=LocEnum.HOMEBASE)
    effect1 = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START, action=effect, activate_once=True
    )
    return Spell(activation_effect=effect1)


# Reduce the cost of Sea Monster allies everywhere by 1.
# Draw a Sea Monster.
def LureoftheDepths():
    effect1 = BuffEverywhereEffect(
        filter_obj=BaseCardFilter(subtype=SubTypes_.SEA_MONSTER), cost=1
    )
    effect2 = DrawEffect(
        filter_obj=DrawCardFilter(subtype=SubTypes_.SEA_MONSTER),
    )
    return Spell(activation_effect=(effect1, effect2))


# Give an ally +3|+4 this round.
def FuryoftheNorth():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=3,
        health=4,
        round_only=True,
    )
    return Spell(activation_effect=effect)


# Toss 3.Deal 7 to a unit.
def Scrapshot():
    effect = TossEffect(quantity=3)
    effect1 = DamageEffect(value=7, target=TargetShorthand.ANY_BOARD_UNIT)
    return Spell(activation_effect=[effect, effect1])


# This round, grow all allies' Power and Health to the number of spells you've cast this game.
def MindMeld():
    # return self.listener.tally(EntityEvents.ACTIVATE_SPELL, round=False)
    effect = BuffEffect(attack=..., health=..., round_only=True)
    return Spell(activation_effect=effect)


# Recall an ally to create a Fleeting Return in hand.
def Retreat():
    effect = RecallEffect(target=TargetShorthand.ALLIED_BOARD_UNIT)
    effect1 = CreateCardEffect(target=Return, is_fleeting=True, fizz_if_fail=effect)
    return Spell(activation_effect=[effect, effect1])


# Create in hand a random 2 cost card from your regions. It costs 0 this round.
def TrailofEvidence():
    effect = CreateCardEffect(
        target=BaseCardFilter(type=None, owner_same_regions=True, cost=2)
    )
    effect1 = BuffCostEffect(
        value=0,
        operator=Ops_.SET,
        round_only=True,
        target=PostEventParam.CREATED,
        coevent=effect,
    )
    return Spell(activation_effect=(effect, effect1))


# Deal 3 to an ally to deal 3 to anything.
def NoxianFervor():
    effect = DamageEffect(target=TargetShorthand.ALLIED_BOARD_UNIT, value=3)
    effect1 = DamageEffect(
        target=TargetShorthand.ANYTHING,
        value=3,
        target_exclusion=effect.target,
        fizz_if_fail=effect,
    )
    return Spell(activation_effect=[effect, effect1])


# Summon Valor.
def BlindingAssault():
    effect = CreateCardEffect(target=Set2Units.Valor, location=LocEnum.HOMEBASE)
    return Spell(activation_effect=effect)
