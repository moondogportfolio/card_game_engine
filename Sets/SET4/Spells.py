from random import choice
import Sets.SET1.Units as Set1Units
import Sets.SET1.Spells as Set1Spells
import Sets.SET2.Spells as Set2Spells
import Sets.SET2.Units as Set2Units
import Sets.SET3.Units as Set3Units
import Sets.SET3.Spells as Set3Spells
import Sets.SET3.Units as Set4Units
import Sets.SET3.Landmarks as Set4Landmarks
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
    PlantMysteriousPortalEffect,
    SetTrapEffect,
    TrapMultiplier,
)
from card_classes.spell import Spell
from card_classes.unit import Unit
from conditions.base_condition import Condition
from entity_selectors.base_card_filter import BaseCardFilter, InvokeBaseCardFilter
from entity_selectors.card_filter import CardFilter, DrawCardFilter, StackSpellFilter
from entity_selectors.input import ChoiceAction, ChoiceBaseCard, Input
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


# An ally starts a free attack.
def MidnightRaid():
    effect = FreeAttackEffect(target=TargetShorthand.ALLIED_BOARD_UNIT)
    return Spell(activation_effect=effect)


# Predict.
def FeralPrescience():
    effect = PredictEffect()
    return Spell(activation_effect=effect)


# To play, spend all your mana. Summon random Turrets whose total cost equals the mana spent.
def ProductionSurge():
    effect = SpendAllYourManaSpellEffect()
    value = PostEffectParamGetter(
        effect=effect, parameter=EventParameter.VALUE_SPENT_ALL_MANA
    )
    effect1 = CreateCardEffect(target=...)
    # TODO distribution
    return Spell(activation_effect=effect)


# Kill an ally to draw a Champion.
def RiteofCalling():
    effect = DrawEffect(filter_obj=BaseCardFilter(flags=CardFlags.IS_CHAMPION))
    effect1 = DestroyManaGem()
    effect2 = KillAction(target=TargetShorthand.ALLIED_BOARD_UNIT)
    # TODO alternative cost
    return Spell(activation_effect=effect)


# Grant an enemy Vulnerable. If it's already Vulnerable, the strongest ally starts a free attack Challenging it.
def TheList():
    target_obj = TargetEntity(target=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = AddKeywordEffect(target=target_obj, keyword=KeywordEnum.VULNERABLE)
    effect1 = FreeAttackEffect(target=target_obj)
    effect2 = ChallengeEffect(
        challenger=AutoEntitySelector.STRONGEST_BOARD_UNIT, target=target_obj
    )
    #TODO bundle
    effect3 = BranchingAction(
        condition=Condition(
            target=target_obj,
            condition=CardFlags.HAS_KEYWORD,
            parameter=KeywordEnum.VULNERABLE,
        ),
        if_true=effect2,
        if_false=effect1,
    )
    return Spell(activation_effect=effect3)



# Grant an ally +1|+1.
def BattlefieldProwess():
    effect = BuffEffect(TargetShorthand.ALLIED_BOARD_UNIT, 1, 1)
    return Spell(activation_effect=effect)


# Create a Snapjaw Swarm on top of your deck.
def Bloodbait():
    effect = CreateCardEffect(Set4Units.SnapjawSwarm, LocEnum.DECK, index=0)
    return Spell(activation_effect=effect)


# For the rest of the game, the first time you play a follower each round, pick 1 of 3 followers with the same cost to transform it into.
def ConcurrentTimelines():
    effect = TriggeredAction(event=EntityEvents.PLAY_UNIT, activations_per_round=1)
    #TODO
    effect1 = TransformEffect(
        target=...,
        new_form=BaseCardFilter(
            cost=EntityAttribute(target=..., attribute=AttrEnum.COST),
            quantity=1,
        ),
    )
    return Spell(activation_effect=effect)


# Give an enemy -2|-0 and Vulnerable this round.
def Exhaust():
    effect = BuffEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT,
        attack=-2,
        keyword=KeywordEnum.VULNERABLE,
        round_only=True,
    )
    return Spell(activation_effect=effect)


# Daybreak: Create a random Nightfall card in hand.Nightfall: Create a random Daybreak card in hand.
def HeavensAligned():
    obj = BaseCardFilter(type=None, flags=CardFlags.HAS_DAYBREAK)
    obj1 = BaseCardFilter(type=None, flags=CardFlags.HAS_NIGHTFALL)
    effect = CreateCardEffect(obj, condition=PlayerFlags.NIGHTFALL)
    effect1 = CreateCardEffect(obj1, condition=PlayerFlags.DAYBREAK)
    return Spell(activation_effect=[effect, effect1])

# Create a random landmark with Countdown in hand.
def ImaginedPossibilities():
    target = TargetEntity(choices=TargetShorthand.ALLIED_COUNTDOWN_LANDMARK)
    effect = AdvanceCountdownEffect(target=target)
    effect1 = CreateCardEffect(target=BaseCardFilter(type=Types_.LANDMARK, quantity=1))
    effect2 = ChoiceAction(choices=[effect, effect1])
    return Spell(activation_effect=effect2)


# Predict.Give an enemy -2|-0 this round.
def ScryingSands():
    effect = PredictEffect()
    effect1 = BuffEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT, attack=-2, round_only=True
    )
    return Spell(activation_effect=[effect, effect1])


# Give an ally +1|+1 this round.If you've summoned a landmark this game, give it +2|+1 instead.
def ShapedStone():
    target_obj = TargetEntity(target=TargetShorthand.ALLIED_BOARD_UNIT)
    effect1 = BuffEffect(target=target_obj, attack=2, health=1, round_only=True)
    effect2 = BuffEffect(target=target_obj, attack=1, health=1, round_only=True)
    effect3 = BranchingAction(
        condition=PlayerFlags.HAS_SUMMONED_LANDMARK_THIS_GAME,
        if_true=effect1,
        if_false=effect2,
    )  # compare value
    return Spell(activation_effect=effect3)


# Manifest a landmark you can afford.
def Stoneweaving():
    effect = ManifestEffect(
        target=BaseCardFilter(
            type=Types_.LANDMARK,
            cost=(
                0,
                EntityAttribute(target=TargetPlayer.OWNER, attribute=AttrEnum.MANA),
            ),
        )
    )
    return Spell(activation_effect=effect)


# Create a Fleeting Flash Freeze, Fury of the North, or Entomb in hand.
def ThreeSisters():
    effect = TellstonesEffect(
        target=[Entomb, Set1Spells.FlashFreeze, Set2Spells.FuryoftheNorth]
    )
    return Spell(activation_effect=effect)


# Grant the top ally in your deck +2|+2.Enlightened: Instead, grant all allies in your deck +2|+2.
def AncestralBoon():
    effect = BuffEffect(target=AutoEntitySelector.TOP_ALLY_IN_DECK, attack=2, health=2)
    effect1 = BuffEffect(target=CardFilter(location=LocEnum.DECK), attack=2, health=2)
    effect2 = BranchingAction(
        condition=PlayerFlags.ENLIGHTENED, if_true=effect1, if_false=effect
    )
    return Spell(activation_effect=effect2)


# Obliterate an ally to summon a Stasis Statue in place with the ally stored inside.
def AncientHourglass():
    effect = ObliterateEffect(target=TargetShorthand.ALLIED_BOARD_UNIT)
    #TODO inplace
    effect1 = CreateCardEffect(Set4Landmarks.StasisStatue, LocEnum.HOMEBASE)
    return Spell(activation_effect=[effect, effect1])



# An ally strikes an enemy, then moves to the top of your deck.
def BoneSkewer():
    effect = TargetEntity(target=TargetShorthand.ALLIED_BOARD_UNIT)
    effect1 = StrikeEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT, striker=effect)
    effect2 = MoveEffect(target=effect, location=LocEnum.DECK, index=0)
    return Spell(activation_effect=[effect1, effect2])



# To play, put a card from hand on top of your deck.Create 2 random Lurkers in hand.
def CallthePack():
    #TODO filter quant
    effect = MoveEffect(
        target=TargetShorthand.ALLIED_HAND_CARD,
        location=LocEnum.DECK,
        index=0,
    )
    effect2 = CreateCardEffect(
        target=BaseCardFilter(quantity=2, flags=CardFlags.IS_LURKER)
    )
    return Spell(activation_effect=effect2, play_requisite=effect)



# Start a free attack with an exact Ephemeral copy of each ally.
def ParallelConvergence():
    effect = CreateCardEffect(
        target=CardFilter(), is_ephemeral=True, location=LocEnum.BATTLEFIELD
    )
    effect1 = FreeAttackEffect()
    return Spell(activation_effect=[effect, effect1])



# Draw 1.Create a Parallel Convergence in your deck.
def CalledShot():
    effect = DrawEffect()
    effect1 = CreateCardEffect(ParallelConvergence, LocEnum.DECK)
    return Spell(activation_effect=[effect, effect1])


# The next time you play a unit this round, grant it Scout. It's now an Elite.
def FieldPromotion():
    effect = AddKeywordEffect(target=PostEventParam.TARGET, keyword=KeywordEnum.SCOUT)
    effect1 = SetAttribute(
        target=PostEventParam.TARGET, attribute=AttrEnum.SUBTYPES, operator=Ops_.PUSH
    )
    ta = TriggeredAction(
        event=EntityEvents.PLAY_UNIT,
        action=[effect, effect1],
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        round_only=True
    )
    effect2 = CreateTriggeredAction(triggered_action=ta)
    return Spell(activation_effect=effect2)


# Give the weakest ally "I can't take damage or die" this round.
def LambsRespite():
    effect = ActionNegator(event_filter=EntityEvents.DIE)
    # TODO
    # target.listener.negate(EntityEvents.DAMAGE, round_only=True)
    # target.listener.negate(EntityEvents.DIE, round_only=True)
    return Spell(activation_effect=...)


# Blade Dance 2.
def FlawlessDuet():
    effect = BladedanceEffect(quantity=2)
    return Spell(activation_effect=effect)


# Recall an ally to create a Flawless Duet in hand.
def LeadandFollow():
    effect = RecallEffect(target=TargetShorthand.ALLIED_BOARD_UNIT)
    effect1 = CreateCardEffect(FlawlessDuet, fizz_if_fail=effect)
    return Spell(activation_effect=[effect, effect1])


# Deal 1 to anything.
def KnockEmDown():
    effect = DamageEffect(value=1, target=TargetShorthand.ANYTHING)
    return Spell(activation_effect=effect)


# Summon a Powder Keg.Create a Knock 'Em Down in hand.
def LineEmUp():
    effect = CreateCardEffect(Set2Units.PowderKeg, LocEnum.HOMEBASE)
    effect1 = CreateCardEffect(KnockEmDown)
    return Spell(activation_effect=[effect, effect1])


# Pick a buff from among 3 to grant an ally.
def LuckyFind():
    effect = ChoiceBaseCard(
        choices=BaseCardFilter(quantity=3, family=CardFamily.LUCKY_FIND)
    )
    effect1 = CreateCardEffect(target=effect1, is_fleeting=True)
    return Spell(activation_effect=[effect, effect1])
    #TODO


# Pick a buff from among 3 to grant an ally.
def LuckyFind():
    effect = AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT, keyword=KeywordEnum.SPELLSHIELD
    )


# Pick a buff from among 3 to grant an ally.
def LuckyFind():
    effect = AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT, keyword=KeywordEnum.CHALLENGER
    )


# Pick a buff from among 3 to grant an ally.
def LuckyFind():
    effect = AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT, keyword=KeywordEnum.FEARSOME
    )


# Pick a buff from among 3 to grant an ally.
def LuckyFind():
    effect = BuffEffect(target=TargetShorthand.ALLIED_BOARD_UNIT, attack=2)


# Pick a buff from among 3 to grant an ally.
def LuckyFind():
    effect = BuffEffect(target=TargetShorthand.ALLIED_BOARD_UNIT, attack=1, health=1)


# Pick a buff from among 3 to grant an ally.
def LuckyFind():
    effect = AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT, keyword=KeywordEnum.QUICKSTRIKE
    )


# Pick a buff from among 3 to grant an ally.
def LuckyFind():
    effect = BuffEffect(target=TargetShorthand.ALLIED_BOARD_UNIT, attack=0, health=2)


# Pick a buff from among 3 to grant an ally.
def LuckyFind():
    effect = AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT, keyword=KeywordEnum.TOUGH
    )


# Pick a buff from among 3 to grant an ally.
def LuckyFind():
    effect = AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT, keyword=KeywordEnum.OVERWHELM
    )


# Draw 1.If you've slain a unit this round, drain 2 from the enemy Nexus.
def RuinousPath():
    effect = DrawEffect()
    effect1 = DrainEffect(
        value=2,
        target=TargetPlayer.OPPONENT,
        condition=PlayerFlags.HAS_SLAIN_UNIT_THIS_ROUND,
    )
    return Spell(activation_effect=[effect, effect1])



# Give an ally +2|+0 to give an enemy Vulnerable this round.
def RuthlessPredator():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT, attack=2, round_only=True
    )
    effect1 = AddKeywordEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT,
        keyword=KeywordEnum.VULNERABLE,
        round_only=True,
        fizz_if_fail=effect
    )
    return Spell(activation_effect=[effect, effect1])



# Grant an ally Lifesteal, Fearsome, and Ephemeral.
def SongoftheIsles():
    effect = AddKeywordEffect(
        keyword=[KeywordEnum.LIFESTEAL, KeywordEnum.FEARSOME, KeywordEnum.EPHEMERAL],
        target=TargetShorthand.ALLIED_BOARD_UNIT,
    )
    return Spell(activation_effect=effect)



# Swap 2 allies.
def Syncopation():
    effect = SwapEffect(target=TargetEntity(quantity=2, minimum=2))
    return Spell(activation_effect=effect)



# Give an ally Overwhelm and +2|+1 this round.
def TheAbsolversReturn():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=2,
        health=1,
        keyword=KeywordEnum.OVERWHELM,
        round_only=True,
    )
    return Spell(activation_effect=effect)


# Give an ally +2|+1 this round. If you have leveled a champion this game, create a The Absolver's Return in hand.
def TheAbsolver():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=2,
        health=1,
        round_only=True,
    )
    effect1 = CreateCardEffect(
        TheAbsolversReturn, condition=PlayerFlags.HAS_LEVELED_CHAMP_THIS_GAME
    )   
    return Spell(activation_effect=[effect, effect1])


# Predict, then draw 1.
def TimeTrick():
    effect = PredictEffect()
    effect1 = DrawEffect()
    return Spell(activation_effect=[effect, effect1])


# Predict and advance an allied landmark 2 rounds.
def TimeinaBottle():
    effect = PredictEffect()
    effect1 = AdvanceCountdownEffect(target=TargetShorthand.ALLIED_LANDMARK, value=2)
    return Spell(activation_effect=[effect, effect1])


# To play, discard 1.Deal 1 to an enemy or the enemy Nexus, then deal 1 to another.
def Timewinder():
    effect = DiscardEffect(target=TargetShorthand.ALLIED_HAND_CARD)
    effect1 = ActionRequisite(requisite=effect)
    target = TargetEntity(choices=CardFilter(owner=TargetPlayer.OPPONENT))
    effect2 = DamageEffect(
        target=target,
        value=1,
    )
    # TODO
    return Spell(activation_effect=[effect1, effect2], play_requisite=effect)


# Draw 1.Nightfall: Activate an ally's Nightfall effect, ignoring any targeted portions.
def UntoDusk():
    effect = DrawEffect()
    effect1 = PlayerFlags.NIGHTFALL
    #TODO
    return Spell(activation_effect=...)


# Give an enemy follower -4|-0 this round.If you have fewer mana gems than your opponent, kill it instead.
def Unworthy():
    effect = TargetEntity(target=TargetShorthand.OPPONENT_BOARD_UNIT)
    effect1 = KillAction(effect)
    effect2 = BuffEffect(target=effect, attack=-4, round_only=True)
    effect3 = BranchingAction(
        condition=Condition(), if_true=effect1, if_false=effect2
    )  #TODO compare value
    return Spell(activation_effect=[effect, effect1])


# Summon a Sandstone Charger.
def WakingSands():
    effect = CreateCardEffect(Set4Units.SandstoneCharger, LocEnum.HOMEBASE)
    return Spell(activation_effect=effect)


# Summon a Sand Soldier.Create a Fleeting Arise! in hand.
def Arise():
    effect = CreateCardEffect(Set4Units.SandSoldier, LocEnum.HOMEBASE)
    effect1 = CreateCardEffect(Arise, is_fleeting=True)
    return Spell(activation_effect=[effect, effect1])


# To Play, place a card from your hand into your deck.Predict, then create an exact copy of the chosen card in hand.
def CarefulPreparation():
    effect2 = MoveEffect(target=TargetShorthand.ALLIED_HAND_CARD, location=LocEnum.DECK)
    effect = PredictEffect()
    effect1 = CreateCardEffect(target=..., exact_copy=True)
    return Spell(activation_effect=[effect, effect1], play_requisite=effect)


# An ally starts a free attack Challenging an enemy.
def Cataclysm():
    target_obj = TargetEntity(target=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = FreeAttackEffect(target=target_obj)
    effect1 = ChallengeEffect(challenger=target_obj)
    # TODO
    return Spell(activation_effect=[effect, effect1])


# An ally you've targeted this round strikes an enemy.
def GrapplingHook():
    # TODO
    striker_obj = EventQuery(event=EntityEvents.TARGETED, round=True)
    effect = StrikeEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT, striker=...)
    return Spell(activation_effect=effect)


# Deal 1 to EVERYTHING.
def IceShard():
    effect = DamageEffect(target=TargetShorthand.EVERYTHING, value=1)
    return Spell(activation_effect=effect)


# Reputation: I cost 1. Pick a spell in play or in hand and create a Fleeting copy of it in hand.
def Mimic():
    effect = DynamicCostModifier(
        value=1, condition=PlayerFlags.REPUTATION, operator=Ops_.SET
    )
    target = TargetEntity(
        target=[
            StackSpellFilter(),
            CardFilter(location=LocEnum.HAND, type=Types_.SPELL),
        ]
    )
    effect1 = CreateCardEffect(target, is_fleeting=True)
    return Spell(activation_effect=effect1, effect=effect)


# Give an enemy -4|-0 and disable its KeywordEnum (excluding any negative KeywordEnum) this round.
def Quicksand():
    target = TargetEntity(choices=TargetShorthand.OPPONENT_BOARD_UNIT)
    effect2 = BuffEffect(attack=-4, round_only=True)
    effect3 = PurgeKeywordsEffect(target=target, purge_positive=True)
    return Spell(activation_effect=[effect2, effect3])


# Grant an ally +1|+2.Plunder: Grant +2|+4 instead.
def SpoilsofWar():
    target_obj = TargetEntity(target=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = BuffEffect(target=target_obj, attack=1, health=2)
    effect1 = BuffEffect(target=target_obj, attack=2, health=4)
    effect2 = BranchingAction(
        condition=PlayerFlags.PLUNDER, if_true=effect1, if_false=effect
    )
    return Spell(activation_effect=effect2)



# Invoke.If you have a Celestial ally, replace your deck with 20 copies of Behold the Infinite.
def StarlitEpiphany():
    effect = InvokeEffect()
    effect2 = CreateCardEffect(Set3Spells.BeholdtheInfinite, location=None, quantity=20)
    effect1 = ReplaceDeck(replacement=effect2)
    return Spell(activation_effect=[effect, effect1])


# Summon 2 Roiling Sands.Draw 1.
def UnraveledEarth():
    effect = CreateCardEffect(Set4Landmarks.RoilingSands, LocEnum.HOMEBASE, quantity=2)
    effect1 = DrawEffect()
    return Spell(activation_effect=[effect, effect1])


# An ally with 5+ Power strikes an enemy.
def BloodyBusiness():
    effect = StrikeEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT,
        striker=TargetEntity(filter=CardFilter(attack=(5, 0))),
    )
    return Spell(activation_effect=effect)


# Recall a unit.Blade Dance 1.
def DefiantDance():
    effect = RecallEffect(target=TargetShorthand.ANY_BOARD_UNIT)
    effect1 = BladedanceEffect(target=None, quantity=1)
    return Spell(activation_effect=[effect, effect1])


# Grant allied Sand Soldiers everywhere +1|+0.Summon 2 Sand Soldiers.
def DesertsWrath():
    effect = BuffEverywhereEffect(
        filter_obj=BaseCardFilter(card_class=Set4Units.SandSoldier), attack=1
    )
    effect1 = CreateCardEffect(Set4Units.SandSoldier, LocEnum.HOMEBASE, quantity=2)
    # TODO buff ever
    return Spell(activation_effect=[effect, effect1])


# Pick a unit to strike your Nexus, then kill it.
def Despair():
    target = TargetEntity(target=TargetShorthand.ANY_BOARD_UNIT)
    effect = StrikeEffect(target=TargetPlayer.ORIGIN_OWNER, striker=target)
    effect1 = KillAction(target=target)
    return Spell(activation_effect=[effect, effect1])


# Give an ally Barrier this round.Rally.
def GoldenAegis():
    effect = AddKeywordEffect(
        keyword=KeywordEnum.BARRIER, target=TargetShorthand.ALLIED_BOARD_UNIT
    )
    effect1 = RallyEffect()
    return Spell(activation_effect=[effect, effect1])


# Stun an enemy. Deal 3 to it if you've summoned a landmark this game.
def GroundSlam():
    target_obj = TargetEntity(target=TargetShorthand.OPPONENT_BOARD_UNIT)
    effect = StunEffect(target=target_obj)
    effect1 = DamageEffect(
        target=target_obj,
        value=3,
        condition=PlayerFlags.HAS_SUMMONED_LANDMARK_THIS_GAME,
    )
    return Spell(activation_effect=[effect, effect1])


# For the rest of the round, when you damage the enemy Nexus, Nab 1.
def LoadedDice():
    effect = NabEffect()
    effect1 = TriggeredAction(
        event=EntityEvents.DAMAGE,
        action=effect,
        round_only=True,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
    )
    return Spell(activation_effect=effect1)


# Draw a Treasure. If there aren't any to draw, create 2 Treasures in your deck instead.
def LostRiches():
    effect = DrawEffect(quantity=None, filter_obj=...)
    effect1 = CreateCardEffect(
        target=BaseCardFilter(type=SubTypes_.TREASURE, quantity=2)
    )
    # TODO
    effect2 = BranchingAction(condition=..., if_true=effect, if_false=effect1)
    return Spell(activation_effect=effect2)


# Grant an allied landmark "My Countdown completion effect activates twice".
def PromisingFuture():
    effect = ...
    effect = TriggeredAction(
        event=EntityEvents.ACTIVATE_COUNTDOWN,
        target=TargetShorthand.ALLIED_LANDMARK,
    )
    # TODO activates twice ?replacement event multiple activations?
    return Spell(activation_effect=...)


# Destroy one of your mana gems to give all enemies -2|-0 this round.
def RiteofDominance():
    effect = BuffEffect(
        target=CardFilter(owner=TargetPlayer.OPPONENT),
        attack=-2,
        health=0,
        round_only=True,
    )
    effect1 = DestroyManaGem()
    effect2 = KillAction(target=TargetShorthand.ALLIED_BOARD_UNIT)
    # TODO alt cost
    return Spell(activation_effect=[effect, effect1])


# Kill an ally or destroy one of your mana gems to stop all enemy Fast spells, Slow spells, and Skills.
def RiteofNegation():
    effect = NegateSpell(target=StackSpellFilter(owner=None))
    effect1 = DestroyManaGem()
    effect2 = KillAction(target=TargetShorthand.ALLIED_BOARD_UNIT)
    # TODO alt cost
    return Spell(activation_effect=[effect, effect1])


# Reputation: I cost 1. Deal 2 to anything.
def SigilofMalice():
    effect = DynamicCostModifier(
        value=1, condition=PlayerFlags.REPUTATION, operator=Ops_.SET
    )
    effect1 = DamageEffect(target=TargetShorthand.ANYTHING, value=2)
    return Spell(activation_effect=effect1, effects=...)


# Frostbite an enemy.Summon a Frozen Thrall.
def SuccumbtotheCold():
    effect = FrostbiteEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT)
    effect1 = CreateCardEffect(Set4Landmarks.FrozenThrall, LocEnum.HOMEBASE)
    return Spell(activation_effect=[effect, effect1])


# Give an ally +5|+0 this round.
def ThornedBlade():
    effect = BuffEffect(TargetShorthand.ALLIED_BOARD_UNIT, 5, 0, round_only=True)
    return Spell(activation_effect=effect)


# Deal 2 to a champion or 7 to a follower.
def WeightofJudgment():
    effect = DamageEffect(value=..., target=...)
    # TODO ?choice or conditional
    return Spell(activation_effect=effect)


# Transform a follower into a 1|1 Squirrel and Silence it this round.
def Whimsy():
    target = TargetEntity(choices=CardFilter(owner=None, is_follower=True))
    effect = TransformEffect(target=target)
    effect1 = SilenceEffect(target=target, round_only=True)
    # TODO WHI,SY
    return Spell(activation_effect=[effect, effect1])


# Reputation: I cost 2. Draw 2.
def WhisperedWords():
    effect = DrawEffect(quantity=2)
    # TODO rep
    return Spell(activation_effect=effect)


# Get an empty mana gem and grant an ally +0|+2.
def ColdResistance():
    effect = GainManaGemEffect()
    effect1 = BuffEffect(target=TargetShorthand.ANY_BOARD_UNIT, attack=0, health=2)
    return Spell(activation_effect=[effect, effect1])


# Obliterate a unit to summon a Frozen Tomb in place with the unit stored inside.
def Entomb():
    # TODO inplace
    effect = ObliterateEffect(target=CardFilter(owner=TargetPlayer.OPPONENT))
    effect1 = CreateCardEffect(target=Set4Landmarks.FrozenTomb)
    return Spell(activation_effect=[effect, effect1])


# Recall each ally and summon a Living Shadow in its place.
def ShadowsofthePast():
    effect = RecallEffect(target=AutoEntitySelector.ALL_ALLIED_UNITS)
    effect1 = CreateCardEffect(target=Set1Units.LivingShadow)
    # TODO inplace
    return Spell(activation_effect=[effect, effect1])


# An ally strikes a unit.If it dies, grant allied champions everywhere +2|+2.
def SiphoningStrike():
    target_obj = TargetEntity(filter=CardFilter(owner=None))
    effect = StrikeEffect(
        target=target_obj, striker=TargetEntity(exclusion=target_obj)
    )
    # TODO followup
    effect1 = BuffEverywhereEffect(
        filter_obj=CardFilter(flags=CardFlags.IS_CHAMPION), condition=...
    )
    return Spell(activation_effect=[effect, effect1])


# Kill a unit, then revive it.
def SpiritJourney():
    target_obj = TargetEntity(target=TargetShorthand.ANY_BOARD_UNIT)
    effect = KillAction(target=target_obj)
    effect1 = ReviveEffect(target=target_obj)
    return Spell(activation_effect=[effect, effect1])


# Summon a Clockling.If you've Predicted this game, summon 2 instead.
def TheTimeHasCome():
    value = EventQuery(event=EntityEvents.PREDICT, target_player=TargetPlayer.OWNER)
    effect = CreateCardEffect(Set4Units.Clockling, LocEnum.HOMEBASE, quantity=1)
    effect2 = CreateCardEffect(Set4Units.Clockling, LocEnum.HOMEBASE, quantity=2)
    # TODO event query
    effect1 = BranchingAction(condition=..., if_true=effect, if_false=effect2)
    return Spell(activation_effect=effect1)


# Drain 2 from 2 enemies.
def WitheringMist():
    effect = DrainEffect(
        value=2,
        target=TargetEntity(
            quantity=2, filter=CardFilter(owner=TargetPlayer.OPPONENT)
        ),
    )
    return Spell(activation_effect=effect)


# Level up all level 1 Ascended allies.
def AscendedsRise():
    # TODO
    effect = LevelupEffect(target=...)
    return Spell(activation_effect=effect)


# Deal 5 to a unit.Plunder: I cost 2 less.
def MonsterHarpoon():
    effect1 = DynamicCostModifier(value=2, condition=PlayerFlags.PLUNDER)
    effect = DamageEffect(value=5, target=TargetShorthand.ANY_BOARD_UNIT)
    return Spell(activation_effect=effect, effects=effect1)


# Reputation: I cost 3. Deal 1 to a random enemy or the enemy Nexus 5 times.
def Ricochet():
    # TODO include player in card filter
    # TODO rep
    effect = DamageEffect(
        value=1,
        target=CardFilter(
            quantity=1,
            filter=CardFilter(owner=TargetPlayer.OPPONENT),
            player=TargetPlayer.OPPONENT,
        ),
    )
    effect1 = MultipleActivationsEffect(target=effect, multiplier=5)
    return Spell(activation_effect=effect1)


# Deal 4 to a unit.Summon 2 Sand Soldiers.
def ShiftingSands():
    effect = DamageEffect(value=4, target=TargetShorthand.ANY_BOARD_UNIT)
    effect1 = CreateCardEffect(Set4Units.SandSoldier, LocEnum.HOMEBASE, quantity=2)
    return Spell(activation_effect=[effect, effect1])


# An ally strikes the strongest and weakest enemies one after another.
def BoomerangBlade():
    target1 = TargetEntity(
        filter=CardFilter(owner=TargetPlayer.OPPONENT, sort_by=CardSorter.STRONGEST)
    )
    target2 = TargetEntity(
        filter=CardFilter(owner=TargetPlayer.OPPONENT, sort_by=CardSorter.WEAKEST)
    )
    effect = StrikeEffect(
        target=[target1, target2], striker=TargetShorthand.ALLIED_BOARD_UNIT
    )
    return Spell(activation_effect=effect)


# Give an allied Champion "The next time I'd die this round, fully heal me and grant me +3|+3 instead".
def Chronoshift():
    effect = HealEffect(value=Ops_.MAX)
    effect1 = BuffEffect(attack=3, health=3)
    effect = ActionReplacement(
        event=EntityEvents.DIE,
        round_only=True,
        handler=...,
        target=TargetEntity(filter=CardFilter(flags=CardFlags.IS_CHAMPION)),
    )
    # TODO
    return Spell(activation_effect=effect)


# Give enemies Vulnerable this round and summon 6 Sand Soldiers.
def EmperorsDivide():
    effect = AddKeywordEffect(
        target=CardFilter(owner=TargetPlayer.OPPONENT), keyword=KeywordEnum.VULNERABLE
    )
    effect1 = CreateCardEffect(Set4Units.SandSoldier, LocEnum.HOMEBASE, quantity=6)
    return Spell(activation_effect=[effect, effect1])


# Give enemies -2|-0 and "Round End: Deal 2 to me" this round.
def SpiritFire():
    target = CardFilter(owner=TargetPlayer.OPPONENT)
    effect = BuffEffect(target=target, attack=-2, health=0, round_only=True)
    effect1 = DamageEffect(target=target, value=2)
    effect2 = TriggeredAction(event=GameStateEnums.ROUND_END, action=effect1)
    return Spell(activation_effect=[effect, effect2])


# Pick an ally to attack alongside the Blades, then Blade Dance 3.
def VanguardsEdge():
    effect = BladedanceEffect(target=TargetShorthand.ALLIED_BOARD_UNIT, quantity=3)
    return Spell(activation_effect=effect)


# Grant an ally in hand +8|+8.
def DestinysCall():
    effect = BuffEffect(target=TargetShorthand.ALLIED_HAND_UNIT, attack=8, health=8)
    return Spell(activation_effect=effect)


# Summon 2 Legion Marauders.
def StrengthinNumbers():
    effect = CreateCardEffect(Set1Units.LegionMarauder, LocEnum.HOMEBASE, quantity=2)
    return Spell(activation_effect=effect)


def BuriedinIceEffect():
    ...


# Obliterate each enemy to summon a Frozen Tomb in place with the enemy stored inside.
def BuriedinIce():
    effect = ObliterateEffect(target=CardFilter(owner=TargetPlayer.OPPONENT))
    effect1 = CreateCardEffect(target=Set4Landmarks.FrozenTomb)
    return Spell(activation_effect=BuriedinIceEffect)


# Your cards have -1 cost, Augment, are created by Glorious Evolution, and are now Tech.
def GloriousEvolution():
    effect = DynamicCostModifier(value=1, target=...)
    # todo buff everywhere
    return Spell(activation_effect=effect)


# If you see me in a Prediction, draw me.Deal 2 to enemies and the enemy Nexus.
def HexiteCrystal():
    # TODO filter
    effect = DamageEffect(
        target=AutoEntitySelector.OPPONENT_NEXUS_AND_BOARD_UNITS, value=2
    )
    effect1 = TriggeredAction(
        event_filter=EntityEvents.PREDICT, action=effect, ally_enum=...
    )
    return Spell(effects=effect1)


# The next time you summon an ally this round, grant it Challenger.
def TatteredBanner():
    effect = AddKeywordEffect(
        target=PostEventParam.TARGET, keyword=KeywordEnum.CHALLENGER
    )
    effect2 = TriggeredAction(
        event=EntityEvents.SUMMON, action=effect, ally_enum=OriginEnum.T_ALLY_O_ALLY
    )
    return Spell(activation_effect=effect2)


# Summon a random landmark with Countdown.
def InstantCentury():
    effect1 = CreateCardEffect(
        target=BaseCardFilter(type=Types_.LANDMARK, flags=CardFlags.HAS_COUNTDOWN)
    )
    effect2 = AdvanceCountdownEffect(
        target=TargetEntity(
            filter=CardFilter(type=Types_.LANDMARK, flags=CardFlags.HAS_COUNTDOWN)
        ),
        value=4,
    )
    effect = ChoiceAction(choices=[effect1, effect2])
    return Spell(activation_effect=effect)


# Grant an ally +3|+2 and Overwhelm.
def SeedofStrength():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=3,
        health=2,
        keyword=KeywordEnum.OVERWHELM,
    )
    return Spell(activation_effect=effect)



def RelicofPower0():
    # _cardcode = "04SH130T11"
    effect = PredictEffect()
    effect1 = DrawEffect()
    return Spell(activation_effect=(effect, effect1))


def RelicofPower1():
    # _cardcode = "04SH130T12"
    effect = CreateCardEffect(
        target=Set4Units.SandstoneCharger, location=LocEnum.HOMEBASE
    )
    return Spell(activation_effect=effect)

def RelicofPower2():
    # _cardcode = "04SH130T9"

    effect = BuffEffect(target=CardFilter(), attack=1, health=0)
    return Spell(activation_effect=effect)

# Pick 1 - Predict then draw 1, summon a Sandstone Charger, or grant all allies +1|+0.
def RelicofPower():
    effect = ChoiceBaseCard(choices=[RelicofPower0, RelicofPower1, RelicofPower1])
    effect1 = PlayEffect()
    return Spell(activation_effect=(effect, effect1))




# Cast a The Absolver's Resurrection, a Fount of Power, or a Shield of the Sentinels.
def SentinelsHoard():
    effect = ChoiceBaseCard(
        choices=[TheAbsolversResurrection, FountofPower, ShieldoftheSentinels]
    )
    effect1 = PlayEffect(target=effect)
    return Spell(activation_effect=(effect, effect1))


# Grant all enemies Vulnerable and create in hand a 0 cost copy of the strongest ally
# that died this game.
def TheAbsolversResurrection():
    effect = AddKeywordEffect(
        target=CardFilter(owner=TargetPlayer.OPPONENT), keyword=KeywordEnum.VULNERABLE
    )
    # TODO
    effect1 = CreateCardEffect(target=value, cost=0)
    return Spell(activation_effect=(effect, effect1))


# Draw 2. Your cards cost 1 less this round.
def FountofPower():
    effect = DrawEffect(quantity=2)
    effect1 = DynamicCostModifier(target=CardFilter(location=None))
    # TODO destroy modifier
    return Spell(activation_effect=(effect, effect1))


# Grant your champions everywhere SpellShield and +2|+2.
def ShieldoftheSentinels():
    effect = BuffEverywhereEffect(
        filter_obj=BaseCardFilter(
            flags=CardFlags.IS_CHAMPION,
            keyword=KeywordEnum.SPELLSHIELD,
            attack=2,
            health=2,
        )
    )
    return Spell(activation_effect=effect)
