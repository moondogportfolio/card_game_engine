from random import choice
import Sets.SET1.Units as Set1Units
import Sets.SET1.Spells as Set1Spells
import Sets.SET2.Units as Set2Units
from Sets.SET3.CustomSpells import ForTheFallenEffect, GiveItAllEffect
import Sets.SET3.Units as Set3Units
import Sets.SET1.Champions as Set1Champions

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
from actions.attack.free_attack import FreeAttackEffect
from actions.attack.overwhelm_effect import OverwhelmEffect
from actions.attribute.buff import BuffCostEffect, BuffEffect
from actions.attribute.buff_everywhere import BuffEverywhereEffect
from actions.attribute.damage import DamageEffect
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
from actions.common.strike import MutualStrikeEffect, StrikeEffect
from actions.create.bladedance import BladedanceEffect

from actions.create.create_card import CreateCardEffect
from actions.create.create_copy import CreateExactCopyEffect
from actions.create.create_hand_cards import ReforgeEffect
from actions.create.fill_location import FillHandWithCards
from actions.create.invoke import InvokeEffect
from actions.create.manifest import ManifestEffect
from actions.create.post_events import CreatePostActParams
from actions.create.summon_specific_cards import SpawnEffect, SummonHuskEffect
from actions.keywords.add_keyword import AddKeywordEffect, AddRandomKeywordEffect
from actions.create.tellstones import TellstonesEffect
from actions.keywords.remove_keyword import RemoveKeywordEffect
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
from value.player_statistic import PlayerStatistic


# Deal 2 to an ally to deal 2 to the enemy Nexus.
def SleepwiththeFishes():
    effect = DamageEffect(value=2, target=TargetShorthand.ALLIED_BOARD_UNIT)
    effect1 = DamageEffect(value=2, target=TargetPlayer.OPPONENT, fizz_if_fail=effect)
    return Spell(activation_effect=[effect, effect1])


# Fully heal an ally.
def SpringGifts():
    effect = HealEffect(value=Ops_.MAX, target=TargetShorthand.ALLIED_BOARD_UNIT)
    return Spell(activation_effect=effect)


# Deal 1 to the enemy Nexus.
def Ignition():
    effect = DamageEffect(value=1, target=TargetPlayer.OPPONENT)
    return Spell(activation_effect=effect)


# The next unit with Nightfall you play this round costs 1 less.
def DuskpetalDust():
    effect = DynamicCostModifier(value=1)
    # TODO ?
    return Spell(activation_effect=effect)


# Reduce the cost of a card in hand by 1.
def Moonsilver():
    effect = BuffCostEffect(value=1, target=TargetShorthand.ALLIED_HAND_CARD)
    return Spell(activation_effect=effect)


# To play, discard 1.Create 2 Daring Poros in hand.
def PoroCannon():
    effect = CreateCardEffect(Set3Units.DaringPoro, quantity=2)
    effect1 = DiscardEffect(target=TargetShorthand.ALLIED_HAND_CARD)
    return Spell(activation_effect=effect, play_requisite=effect1)


# Deal 1 to a unit. Create a Death Ray - Mk 2 in the top 3 cards of your deck.
def DeathRayMk1():
    effect = DamageEffect(value=1, target=TargetShorthand.ANY_BOARD_UNIT)
    effect1 = CreateCardEffect(DeathRayMk2, index=(0, 2))
    return Spell(activation_effect=[effect, effect1])


# Deal 2 to a unit. Create a Death Ray - Mk 3 in the top 3 cards of your deck.
def DeathRayMk2():
    effect = DamageEffect(value=2, target=TargetShorthand.ANY_BOARD_UNIT)
    effect1 = CreateCardEffect(DeathRayMk3, index=(0, 2))
    return Spell(activation_effect=[effect, effect1])


# Deal 3 to a unit.
def DeathRayMk3():
    effect = DamageEffect(value=3, target=TargetShorthand.ANY_BOARD_UNIT)
    return Spell(activation_effect=effect)


# Silence a follower.
def Equinox():
    effect = SilenceEffect(
        target=TargetEntity(choices=CardFilter(owner=None, flags=CardFlags.IS_FOLLOWER))
    )
    return Spell(activation_effect=effect)


# Pick a Moon Weapon to create in hand.
def GiftsFromBeyond():
    effect = ChoiceBaseCard(choices=CardFilter(subtype=SubTypes_.MOONCARD))
    effect1 = CreateCardEffect(target=effect)
    return Spell(activation_effect=effect1)


# Deal 3 to a follower. Phase Severum or Gravitum.
def Calibrum():
    effect = DamageEffect(value=3, target=TargetShorthand.ANY_BOARD_FOLLOWER)
    effect1 = PhaseMoonWeaponEffect(target=[Severum, Gravitum])
    return Spell(activation_effect=effect)


# Give an ally +1|+2 and Lifesteal this round. Phase Gravitum or Infernum.
def Severum():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=1,
        health=2,
        round_only=True,
        keyword=KeywordEnum.LIFESTEAL,
    )
    effect1 = PhaseMoonWeaponEffect(target=[Infernum, Gravitum])


# Stun an enemy. If it's a follower, Stun it again at the next Round Start. Phase Infernum or Crescendum.
def Gravitum():
    effect = StunEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT)
    effect = TriggeredAction(event=GameStateEnums.ROUND_START)
    effect1 = PhaseMoonWeaponEffect(target=[Infernum, Crescendum])


# Give an ally +2|+1 and Overwhelm this round. Phase Crescendum or Calibrum.
def Infernum():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=2,
        health=1,
        round_only=True,
        keyword=KeywordEnum.OVERWHELM,
    )
    effect1 = PhaseMoonWeaponEffect(target=[Calibrum, Crescendum])


# Summon a 2 cost follower from your deck. If it has Nightfall, activate it. Phase Calibrum or Severum.
def Crescendum():
    effect = ...
    effect1 = PhaseMoonWeaponEffect(target=[Calibrum, Severum])


# Drain 1 from a unit and create 2 copies of me in your deck. Once you've cast me 3 times, transform all copies of me everywhere into Pack Your Bags.
def GoHard():
    effect = DrainEffect(value=1, target=TargetShorthand.ANY_BOARD_UNIT)
    effect1 = CreateCardEffect(GoHard, LocEnum.DECK, quantity=2)
    transform = TransformEffect(
        new_form=PackYourBags, target=CardFilter(location=[LocEnum.HAND, LocEnum.DECK])
    )
    ta = ValueTriggeredAction(
        threshold=3,
        action_on_value=transform,
        event_filter=EntityEvents.PLAY_SPELL,
        ally_enum=OriginEnum.T_SELFCLASS,
    )
    return Spell(activation_effect=[effect, effect1], effects=ta)


# Deal 5 to all enemies and the enemy Nexus. Transform all copies of me everywhere back to Go Hard.
def PackYourBags():
    effect = DamageEffect(
        value=5, target=AutoEntitySelector.OPPONENT_NEXUS_AND_BOARD_UNITS
    )
    transform = TransformEffect(
        new_form=GoHard, target=CardFilter(location=[LocEnum.HAND, LocEnum.DECK])
    )
    return Spell(activation_effect=[effect, transform])


# Create 5 The Messengers in your deck.
def MessengersSigil():
    effect = CreateCardEffect(Set3Units.TheMessenger, LocEnum.DECK, quantity=5)
    return Spell(activation_effect=effect)


# Deal 2 to an ally to grant 2 enemies Vulnerable.
def Shakedown():
    effect = DamageEffect(value=2, target=TargetShorthand.ALLIED_BOARD_UNIT)
    effect1 = AddKeywordEffect(
        keyword=KeywordEnum.VULNERABLE,
        target=TargetEntity(
            quantity=2, choices=CardFilter(owner=TargetPlayer.OPPONENT)
        ),
        fizz_if_fail=effect,
    )
    return Spell(activation_effect=[effect, effect1])


# The next time you summon an ally this round, give it +1|+0 and SpellShield this round.
def ShroudofDarkness():
    effect = BuffEffect(
        target=PostEventParam.TARGET,
        attack=1,
        keyword=KeywordEnum.SPELLSHIELD,
        round_only=True,
    )
    effect1 = TriggeredAction(
        event=EntityEvents.SUMMON,
        action=effect,
        max_activations=1,
        round_only=True,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
    )
    return Spell(activation_effect=effect1)


# Manifest an enemy spell played this game.
def SpellThief():
    # TODO event query
    value = EventQuery(event=EntityEvents.PLAY_SPELL)
    effect = ManifestEffect(target=value)
    return Spell(activation_effect=effect)


# Remove Fleeting from all cards in hand. When I'm discarded, draw 1 Fleeting.
def StressTesting():
    effect = RemoveKeywordEffect(
        keyword=KeywordEnum.FLEETING,
        target=CardFilter(type=None, location=LocEnum.HAND),
    )
    effect1 = DrawEffect(is_fleeting=True)
    ta = TriggeredAction(
        event_filter=EntityEvents.DISCARD, action=effect1, ally_enum=OriginEnum.T_SELF
    )
    return Spell(activation_effect=effect, effects=ta)


# Stun an enemy.If you have a Darius, Rally.
def Apprehend():
    effect = StunEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT)
    effect1 = RallyEffect(
        condition=Condition(
            target=TargetPlayer.ORIGIN_OWNER,
            condition=PlayerFlags.HAS_UNIT_ON_BOARD,
            parameter=Set1Champions.Darius,
        )
    )
    return Spell(activation_effect=[effect, effect1])


# Invoke.
def BeholdtheInfinite():
    effect = InvokeEffect()
    return Spell(activation_effect=effect)


# Create an Armed Gearhead, Ballistic Bot, or Nyandroid in hand.
def CalculatedCreations():
    choice_obj = ChoiceBaseCard(
        choices=[
            Set3Units.ArmedGearhead,
            Set3Units.Nyandroid,
            Set3Units.BallisticBot,
        ]
    )
    effect1 = CreateCardEffect(target=choice_obj)
    return Spell(activation_effect=effect1)


# Grant an ally Challenger.
def Confront():
    effect = AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT, keyword=KeywordEnum.CHALLENGER
    )
    return Spell(activation_effect=effect)


# Heal an ally or your Nexus 2. Draw 1.
def GuidingTouch():
    effect = HealEffect(value=2, target=TargetShorthand.ALLY_NEXUS_OR_BOARD_UNITS)
    effect1 = DrawEffect()
    return Spell(activation_effect=[effect, effect1])


# Your opponent discards the weakest follower from hand.
def HunttheWeak():
    effect = DiscardEffect(
        target=CardFilter(
            location=LocEnum.HAND,
            owner=TargetPlayer.OPPONENT,
            sort_by=CardSorter.WEAKEST,
            is_follower=True,
            quantity=1,
        ),
    )
    return Spell(activation_effect=effect)


# Pick a follower. Create a copy of it in hand with +1|+1.
def IterativeImprovement():
    effect = CreateCardEffect(
        target=TargetShorthand.ANY_BOARD_FOLLOWER,
        attack=(Ops_.INCREMENT, 1),
        health=(Ops_.INCREMENT, 1),
    )
    return Spell(activation_effect=effect)


# Summon a Powder Monkey.Plunder: Summon another at the next Round Start.
def MonkeyBusiness():
    effect = CreateCardEffect(Set2Units.PowderMonkey, LocEnum.HOMEBASE)
    effect1 = CreateCardEffect(
        Set2Units.PowderMonkey, LocEnum.HOMEBASE, condition=PlayerFlags.PLUNDER
    )
    return Spell(activation_effect=[effect, effect1])


# Grant an ally +0|+2 and SpellShield.
def Moonglow():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        health=2,
        keyword=KeywordEnum.SPELLSHIELD,
    )
    return Spell(activation_effect=effect)


# Stop a Fast or Slow spell that costs 3 or less.
def Nopeify():
    effect = NegateSpell(
        target=TargetEntity(
            choices=StackSpellFilter(
                cost=(0, 3), spell_speed=[SpellSpeedEnum.FAST, SpellSpeedEnum.SLOW]
            )
        )
    )
    return Spell(activation_effect=effect)


# Give an ally +1|+1 this round.Nightfall: Draw 1.
def PaleCascade():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=1,
        health=1,
        round_only=True,
    )
    effect1 = DrawEffect(condition=PlayerFlags.NIGHTFALL)
    return Spell(activation_effect=[effect, effect1])


# Give an ally +2|+2 and "I can block units with Elusive" this round.
def Sharpsight():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=1,
        health=2,
        round_only=True,
        keyword=KeywordEnum.FLYING,
    )
    return Spell(activation_effect=effect)


# Stun an enemy. Create a Fleeting Paddle Star in hand.
def SleepyTroubleBubble():
    effect1 = StunEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT)
    effect = CreateCardEffect(PaddleStar)
    return Spell(activation_effect=[effect1, effect])


# Deal 4 to an enemy that attacked this round or is Stunned.
def PaddleStar():
    effect = DamageEffect(
        value=5,
        target=TargetEntity(
            choices=CardFilter(
                owner=TargetPlayer.OPPONENT,
                flags=[CardFlags.IS_STUNNED, CardFlags.ATTACKED_THIS_ROUND],
            )
        ),
    )
    return Spell(activation_effect=effect)


# If you Behold The Messenger, grant Celestial allies everywhere +1|+1.
def Starbone():
    condition = Condition(
        target=TargetPlayer.ORIGIN_OWNER,
        condition=PlayerFlags.IS_BEHOLDING_X_CARD,
        parameter=BaseCardFilter(subtype=SubTypes_.CELESTIAL),
    )
    effect = BuffEverywhereEffect(
        filter_obj=BaseCardFilter(subtype=SubTypes_.CELESTIAL),
        attack=1,
        health=1,
        condition=condition,
    )
    return Spell(activation_effect=effect)


# Grant an ally +0|+2.
def SunblessedVigor():
    effect = BuffEffect(target=TargetShorthand.ALLIED_BOARD_UNIT, health=2)
    return Spell(activation_effect=effect)


# Invoke a Celestial card that costs 3 or less.
def SupercoolStarchart():
    effect = InvokeEffect(target=InvokeBaseCardFilter(cost=(0, 3)))
    return Spell(activation_effect=effect)


# Give an ally +0|+2 to give an enemy -2|-0 this round.
def TrollChant():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=0,
        health=2,
        round_only=True,
    )
    effect1 = BuffEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT,
        attack=-2,
        health=0,
        round_only=True,
        fizz_if_fail=effect,
    )
    return Spell(activation_effect=[effect, effect1])


# Grant an ally Regeneration. If they already have it, grant them +2|+2 instead.
def TrollGifts():
    target_obj = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = BuffEffect(target=target_obj, attack=2, health=2)
    effect2 = AddKeywordEffect(target=target_obj, keyword=KeywordEnum.REGENERATION)
    effect3 = BranchingAction(
        branching_condition=Condition(
            target=target_obj,
            condition=CardFlags.HAS_KEYWORD,
            parameter=KeywordEnum.REGENERATION,
        ),
        if_true=effect,
        if_false=effect2,
    )
    return Spell(activation_effect=effect3)


# Drain 1 from anything.Nightfall: Create a random Nightfall card in hand.
def UnspeakableHorror():
    effect = DrainEffect(value=1, target=TargetShorthand.ANYTHING)
    effect1 = CreateCardEffect(
        target=BaseCardFilter(type=None, flags=CardFlags.HAS_NIGHTFALL),
        condition=PlayerFlags.NIGHTFALL,
    )
    return Spell(activation_effect=[effect, effect1])


# Give an ally +2|+0 this round. Reforge.
def WeaponHilt():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT, attack=2, round_only=True
    )
    effect1 = ReforgeEffect()
    return Spell(activation_effect=[effect, effect1])


# Give an ally Overwhelm this round.
def HeavyBladeFragment():
    effect = AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        keyword=KeywordEnum.OVERWHELM,
        round_only=True,
    )
    return Spell(activation_effect=effect)


# Give an ally Quick Attack this round.
def KeenBladeFragment():
    effect = AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        keyword=KeywordEnum.QUICKSTRIKE,
        round_only=True,
    )
    return Spell(activation_effect=effect)


# Give an ally +2|+0 this round.
def GlintingBladeFragment():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT, attack=2, round_only=True
    )
    return Spell(activation_effect=effect)


# An ally Captures another ally and gains the captured ally's stats.
def BayouBrunch():
    storage = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    target = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT, exclusion=storage)
    effect = CaptureEffect(storage=storage, target=target, gain_captured_stats=True)
    return Spell(activation_effect=effect)


# Deal 1 to a unit.Then summon Powder Kegs equal to the amount of damage dealt.
def Boomship():
    effect = DamageEffect(value=1, target=TargetShorthand.ANY_BOARD_UNIT)
    effect2 = CreateCardEffect(
        Set2Units.PowderKeg,
        LocEnum.HOMEBASE,
        quantity=PostEventParam.VALUE,
        coevent=effect,
    )
    return Spell(activation_effect=(effect, effect2))


# For the top 4 cards in your deck, draw each Yeti, Poro, and Elnuk.
# Then place the rest into your deck.
def CalltheWild():
    # effect = MoveSpecificReturnRestEffect(
    #     top_x_cards=4,
    #     filter_obj=BaseCardFilter(
    #         subtype=[SubTypes_.YETI, SubTypes_.PORO, SubTypes_.ELNUK], type=None
    #     ),
    # )
    effect = DrawEffect(
        filter_obj=DrawCardFilter(
            top_x_cards=4, subtype=[SubTypes_.YETI, SubTypes_.PORO, SubTypes_.ELNUK]
        )
    )
    return Spell(activation_effect=effect)


# Stun 2 enemies.
def CrescentStrike():
    effect = StunEffect(
        target=TargetEntity(quantity=2, choices=CardFilter(owner=TargetPlayer.OPPONENT))
    )
    return Spell(activation_effect=effect)


# Draw a landmark or destroy a landmark.
def DivergentPaths():
    effect = DrawEffect(filter_obj=DrawCardFilter(type=Types_.LANDMARK))
    effect2 = DestroyLandmarkEffect(target=TargetShorthand.ANY_LANDMARK)
    effect3 = ChoiceAction(choices=[effect, effect2])
    return Spell(activation_effect=effect3)


# Draw 2 different Dragons or grant Dragon allies +1|+1 and Overwhelm.
def DragonsClutch():
    effect = DrawEffect(
        filter_obj=DrawCardFilter(subtype=SubTypes_.DRAGON, unique_class=True),
        quantity=2,
    )
    effect2 = BuffEffect(
        target=CardFilter(subtype=SubTypes_.DRAGON),
        attack=1,
        health=1,
        keyword=KeywordEnum.OVERWHELM,
    )
    effect3 = ChoiceAction(choices=[effect, effect2])
    return Spell(activation_effect=effect3)


# Kill an ally with Last Breath to summon a follower from your deck that costs 1 more.
def Gluttony():
    target = TargetEntity(choices=CardFilter(flags=CardFlags.HAS_LASTBREATH))
    effect = KillAction(target=target)
    effect1 = CreateCardEffect(
        target=BaseCardFilter(
            is_follower=True,
            cost=EntityAttribute(target=target, attribute=AttrEnum.COST),
        ),
        fizz_if_fail=effect,
    )
    # TODO
    return Spell(activation_effect=[effect, effect1])


# Silence a unit this round.
def Hush():
    effect = SilenceEffect(target=TargetShorthand.ANY_BOARD_UNIT, round_only=True)
    return Spell(activation_effect=effect)


# Obliterate all units that were summoned, but not played, this round.
def PassageUnearned():
    effect = ObliterateEffect(target=CardFilter(owner=None, flags=...))
    return Spell(activation_effect=effect)


# Kill a damaged unit or destroy a landmark.
def ScorchedEarth():
    effect = KillAction(
        target=TargetEntity(choices=CardFilter(owner=None, flags=CardFlags.IS_DAMAGED))
    )
    effect2 = DestroyLandmarkEffect(target=TargetShorthand.ANY_LANDMARK)
    effect3 = ChoiceAction(choices=[effect, effect2])
    return Spell(activation_effect=effect3)


# Give an ally +3|+2 this round.
def SharpenedResolve():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=3,
        health=2,
        round_only=True,
    )
    return Spell(activation_effect=effect)


# Pick a follower from the top 4 cards in your deck.
# Draw it, place the rest into your deck, then create an exact Ephemeral copy in hand.
def StalkingShadows():
    effect = TargetEntity(choices=DrawCardFilter(top_x_cards=4, is_follower=True))
    effect1 = TargetedDrawAction(target=effect)
    effect2 = CreateExactCopyEffect(
        target=PostEventParam.TARGET, is_ephemeral=True, coevent=effect1
    )
    return Spell(activation_effect=(effect1, effect2))


# An ally and an enemy strike each other. Then, if the ally is a Dragon, heal it 2.
def StrafingStrike():
    target = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect1 = MutualStrikeEffect(
        first_striker=target, second_striker=TargetShorthand.OPPONENT_BOARD_UNIT
    )
    effect2 = HealEffect(
        target=target,
        value=2,
        condition=Condition(
            target=target,
            condition=CardFlags.IS_SUBTYPE_X,
            parameter=SubTypes_.DRAGON,
        ),
    )
    return Spell(activation_effect=[effect1, effect2])


# Fully heal damaged allies.
def Wish():
    effect = HealEffect(value=Ops_.MAX, target=CardFilter())
    return Spell(activation_effect=effect)


# Grant an ally +1|+2 and Overwhelm.Daybreak: Draw a Zenith Blade.
def ZenithBlade():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=1,
        health=2,
        keyword=KeywordEnum.OVERWHELM,
    )
    effect1 = DrawEffect(
        filter_obj=DrawCardFilter(card_type=ZenithBlade), condition=PlayerFlags.DAYBREAK
    )
    return Spell(activation_effect=[effect, effect1])


# Deal 3 to anything or destroy a landmark.
def Aftershock():
    effect = DamageEffect(value=3, target=TargetShorthand.ANY_BOARD_UNIT)
    effect1 = DestroyLandmarkEffect(target=TargetShorthand.ANY_LANDMARK)
    effect2 = ChoiceAction(choices=[effect, effect1])
    return Spell(activation_effect=effect2)


# Heal an ally 4 and grant it +0|+4.
def AstralProtection():
    target_obj = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect1 = HealEffect(target=target_obj, value=4)
    effect = BuffEffect(target=target_obj, health=4)
    return Spell(activation_effect=[effect1, effect])


# Grant an ally +1|+1 and SpellShield.
def Bastion():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=1,
        health=1,
        keyword=KeywordEnum.SPELLSHIELD,
    )
    return Spell(activation_effect=effect)


# Grant ALL allies in deck and hand +2|+2 and Ephemeral.
def EncroachingShadows():
    effect = BuffEffect(
        target=CardFilter(location=[LocEnum.DECK, LocEnum.HAND]),
        attack=2,
        health=2,
        keyword=KeywordEnum.EPHEMERAL,
    )


# Grant an ally +1|+0 and Quick Attack. If it already has it, grant it Double Attack instead.
def FlurryofFists():
    target = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = BuffEffect(
        target=target,
        attack=1,
        keyword=KeywordEnum.QUICKSTRIKE,
    )
    effect1 = BuffEffect(
        target=target,
        attack=1,
        keyword=KeywordEnum.DOUBLESTRIKE,
    )
    effect3 = BranchingAction(
        branching_condition=Condition(
            target=target,
            condition=CardFlags.HAS_KEYWORD,
            parameter=KeywordEnum.QUICKSTRIKE,
        ),
        if_true=effect1,
        if_false=effect,
    )
    return Spell(activation_effect=effect3)


# Recall an ally unit or landmark to Recall an enemy unit or landmark.
def Homecoming():
    effect = RecallEffect(
        target=TargetEntity(choices=CardFilter(type=[Types_.LANDMARK, Types_.UNIT]))
    )
    effect1 = RecallEffect(
        target=TargetEntity(
            choices=CardFilter(
                type=[Types_.LANDMARK, Types_.UNIT], owner=TargetPlayer.OPPONENT
            )
        ),
        fizz_if_fail=effect,
    )
    return Spell(activation_effect=[effect, effect1])


# Summon a Powder Monkey and give a random enemy Vulnerable this round for each time you've activated Plunder this game.
def PowderPandemonium():
    value = EventQuery(event=EntityEvents.ACTIVATE_PLUNDER, discrete_rounds=True)
    effect = AddKeywordEffect(
        keyword=KeywordEnum.VULNERABLE,
        target=TargetEntity(
            quantity=value,
            randomized=True,
            choices=CardFilter(owner=TargetPlayer.OPPONENT),
        ),
    )


# Heal an ally 1 and grant it +1|+0.
def Gem():
    target = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = HealEffect(value=1, target=target)
    effect1 = BuffEffect(attack=1, target=target)
    return Spell(activation_effect=[effect, effect1])


# Fill your hand with Gems.
def ShardsoftheMountain():
    effect = FillHandWithCards(target=Gem)
    return Spell(activation_effect=effect)


# Transform a follower into a 1|1 Squirrel and Silence it this round.
def Whimsy():
    effect = TransformEffect(
        target=TargetShorthand.ANY_BOARD_FOLLOWER, new_form=Set3Units.Squirrel
    )
    effect1 = SilenceEffect(target=..., round_only=True)


# Summon a Mistwraith.
def RisenMists():
    effect = CreateCardEffect(Set1Units.Mistwraith, LocEnum.HOMEBASE)


# Draw a champion. Reduce its cost by 1 and grant it +2|+2.
def WritteninStars():
    effect = DrawEffect(
        filter_obj=BaseCardFilter(flags=CardFlags.IS_CHAMPION), cost_reduction=1
    )
    target_obj = PostEventParamGetter(effect=effect, parameter=...)
    effect1 = BuffEffect(
        target=target_obj,
        attack=2,
        health=2,
    )


# Grant an ally +3|+3.
def BlessingofTargon():
    effect = BuffEffect(target=TargetShorthand.ALLIED_BOARD_UNIT, attack=3, health=3)


# Kill an ally to kill a unit or destroy a landmark.
def Crumble():
    target_obj = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = KillAction(target=target_obj)
    effect2 = KillAction(
        target=TargetShorthand.OPPONENT_BOARD_UNIT, target_exclusion=target_obj
    )
    effect4 = DestroyLandmarkEffect(target=TargetShorthand.ANY_LANDMARK)
    action = ChoiceAction(choices=[effect4])
    return Spell(activation_effect=action)


# Recall an ally to summon an exact Ephemeral copy in its place. Reduce its cost to 0 this round.
def GoGetIt():
    effect = RecallEffect(target=TargetShorthand.ALLIED_BOARD_UNIT)
    effect2 = CreateCardInPlaceOfEffect(
        target=PostEventParam.TARGET,
        is_ephemeral=True,
        location=LocEnum.HOMEBASE,
        to_replace_effect=effect,
    )
    effect3 = BuffCostEffect(
        value=0,
        operator=Ops_.SET,
        target=PostEventParam.CREATED_CARD,
        round_only=True,
        coevent=effect2,
    )
    # TODO
    return Spell(activation_effect=(effect, effect2, effect3))


# Deal 4 to an enemy and 1 to another.
def MeteorShower():
    target_obj = TargetEntity(choices=TargetShorthand.OPPONENT_BOARD_UNIT)
    effect = DamageEffect(value=4, target=target_obj)
    effect1 = DamageEffect(
        value=1,
        target=TargetShorthand.OPPONENT_BOARD_UNIT,
        target_exclusion=target_obj,
    )
    return Spell(activation_effect=[effect, effect1])


# Give allies +2|+2 this round.Daybreak: Activate all ally Daybreak effects at once.
def MorningLight():
    effect = BuffEffect(target=CardFilter(), attack=2, health=2, round_only=True)
    effect1 = ...
    # commit action
    return Spell()


# For the rest of the game, allied buffs (except Barrier) are permanent. Draw 1.
def OutOfTheWay():
    # TODO duration
    effect = DrawEffect()


# Silence 2 enemy units this round.Nightfall: They can't block this round.
def MoonlightAffliction():
    target_obj = TargetEntity(
        choices=TargetEntity(
            quantity=2, choices=CardFilter(owner=TargetPlayer.OPPONENT)
        )
    )
    effect = SilenceEffect(target=target_obj)
    effect1 = AddKeywordEffect(
        keyword=KeywordEnum.CANTBLOCK, round_only=True, target=effect
    )


# Invoke a Celestial card that costs 7 or more, then heal an ally or your Nexus 4.
def Starshaping():
    effect = InvokeEffect(target=InvokeBaseCardFilter(cost=(7, 0)))
    effect1 = HealEffect(value=4, target=TargetShorthand.ALLY_NEXUS_OR_BOARD_UNITS)


# Deal 1 to a unit. Summon a random 1 cost follower.
# While I'm in hand, increase both by 1 when you play a 3 cost card.
def TribeamImprobulator():
    effect = DamageEffect(target=TargetShorthand.ANY_BOARD_UNIT, value=1)
    effect1 = CreateCardEffect(
        target=BaseCardFilter(cost=1, flags=CardFlags.IS_FOLLOWER),
        location=LocEnum.HOMEBASE,
    )
    # TODO
    ef = EventFilter(event=EntityEvents.PLAY)
    effect2 = ...  # EffectModifier(effect=effect, attribute=..., new_value=...)
    effect4 = ...  # EffectModifier(effect=effect, attribute=..., new_value=...)
    effect3 = TriggeredAction(event=ef, action=[effect2, effect4])
    return Spell(activation_effect=[effect, effect1], effects=effect3)


def SurviveByOne():
    ...


# Allies can't drop below 1 health this round.
# When discarded, your strongest ally can't drop below 1 health this round.
def SurvivalSkills():
    effect1 = ActionReplacement(
        event=EntityEvents.DAMAGE,
        condition=lambda x: ...,
        round_only=True,
        bound_entity=TargetEntity(
            automatic=True, choices=CardFilter(sort_by=CardSorter.STRONGEST)
        ),
    )
    effect2 = ActionReplacement(
        event=EntityEvents.DAMAGE,
        condition=lambda x: ...,
        round_only=True,
        bound_entity=CardFilter(),
    )
    effect = TriggeredAction(
        event=EntityEvents.DISCARD, action=effect2, ally_enum=OriginEnum.SELF
    )
    # TODO
    return Spell(activation_effect=effect1, effects=effect)


# An ally strikes an enemy. If it has Overwhelm, deal excess damage to the enemy Nexus.
def WildClaws():
    target_obj = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    opponent = TargetEntity(choices=TargetShorthand.OPPONENT_BOARD_UNIT)
    effect = StrikeEffect(target=opponent, striker=target_obj)
    effect1 = OverwhelmEffect(striker=target_obj, defender=effect)
    return Spell(activation_effect=[effect, effect1])


# Obliterate an enemy unit or landmark.
def FallingComet():
    effect = ObliterateEffect(target=TargetShorthand.ANY_BOARD_UNIT_OR_LANDMARK)


# An ally with Fury strikes the 2 weakest enemies one after another.
def MoltenBreath():
    effect = StrikeEffect(
        target=TargetEntity(
            quantity=2,
            choices=CardFilter(owner=TargetPlayer.OPPONENT, sort_by=CardSorter.WEAKEST),
        ),
        striker=TargetEntity(choices=CardFilter(flags=CardFlags.HAS_FURY)),
    )


# Deal 6 to a unit.Daybreak: Instead, Silence it this round and deal 6 to it.
def Sunburst():
    target_obj = TargetEntity(choices=TargetShorthand.ANY_BOARD_UNIT)
    effect1 = DamageEffect(value=6, target=target_obj)
    effect2 = SilenceEffect(target=target_obj, round_only=True)
    ...


# If you Behold a Celestial card, grant allies everywhere +2|+2.
def CosmicInspiration():
    effect = ActionRequisite(requisite=PlayerFlags.IS_BEHOLDING_CELESTIAL)
    effect1 = BuffEverywhereEffect(filter_obj=None, attack=2, health=2)


# Pick a unit in your hand to reveal. Heal your Nexus equal to its Power.Enlightened: Reduce its cost to 0.
def RevitalizingRoar():
    target_obj = TargetEntity(choices=TargetShorthand.ALLIED_HAND_CARD)
    effect = RevealEffect(target=target_obj)
    effect1 = HealEffect(
        value=EntityAttribute(target=target_obj, attribute=AttrEnum.ATTACK),
        target=TargetPlayer.ORIGIN_OWNER,
    )
    effect2 = BuffCostEffect(
        value=0, operator=Ops_.SET, condition=PlayerFlags.ENLIGHTENED
    )
    return Spell(activation_effect=[effect, effect1, effect2])


# If you Behold a Celestial card, Obliterate enemies with 3 or less Power.
def CosmicRays():
    condition = (
        Condition(
            target=TargetPlayer.OWNER,
            condition=PlayerFlags.IS_BEHOLDING_X_CARD,
            parameter=SubTypes_.CELESTIAL,
        ),
    )
    effect1 = ObliterateEffect(
        target=CardFilter(owner=TargetPlayer.OPPONENT, attack=(0, 3)),
        condition=condition,
    )
    return Spell(activation_effect=effect1)


# When you summon an Elite, reduce my cost by 1.
# For each ally that died this round, summon a Dauntless Vanguard.
def ForTheFallen():
    effect1 = BuffCostEffect(target=AutoEntitySelector.SELF)
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect1,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
    )
    return Spell(activation_effect=ForTheFallenEffect(), effects=ta)


# Grow all allies' Power and Health to the highest Power or Health among allies.
# Grant all allies allied keywords.
def GiveItAll():
    return Spell(activation_effect=GiveItAllEffect())


# Place a unit or landmark into its deck.
def SunkCost():
    effect = MoveEffect(
        location=LocEnum.DECK,
        target=TargetShorthand.ANY_BOARD_UNIT_OR_LANDMARK,
    )
    return Spell(activation_effect=effect)


# Get 2 empty mana gems.For the top 5 cards in your deck, draw each card that costs 8+. Then place the rest into your deck.
def VoicesoftheOldOnes():
    effect = GainManaGemEffect(value=2)
    effect1 = DrawEffect(filter_obj=DrawCardFilter(cost=(8, 0), top_x_cards=5))
    return Spell(activation_effect=[effect, effect1])


# If you Behold a Celestial card, Obliterate 2 enemy units or landmarks.
def Supernova():
    target = TargetEntity(
        choices=CardFilter(type=[Types_.LANDMARK, Types_.UNIT], owner=None),
        quantity=2,
    )
    effect1 = ObliterateEffect(
        target=target, condition=PlayerFlags.IS_BEHOLDING_CELESTIAL
    )
    return Spell(activation_effect=effect1)


# Fill your hand with random Fleeting Celestial cards. Refill your mana to full.
def LivingLegends():
    effect = FillHandWithCards(
        target=InvokeBaseCardFilter(quantity=10), is_fleeting=True
    )
    effect1 = RefillManaEffect(value=Ops_.MAX)
    return Spell(activation_effect=[effect, effect1])


# Pick an ally. Recall ALL other units and landmarks.
def SingularWill():
    target = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = RecallEffect(
        target=CardFilter(
            type=[Types_.LANDMARK, Types_.UNIT], owner=None, target_exclusion=target
        ),
    )
    return Spell(activation_effect=effect)


# Recall an ally.
def Sanctuary():
    effect = RecallEffect(target=TargetShorthand.ALLIED_BOARD_UNIT)
    return Spell(activation_effect=effect)


# Summon 2 different, random champions from your hand and deck. Grow their stats up to 10|10.
def FeelTheRush():
    target_obj = TargetEntity(
        choices=TargetEntity(
            choices=CardFilter(
                location=[LocEnum.DECK, LocEnum.HAND],
                flags=CardFlags.IS_CHAMPION,
            ),
            quantity=2,
        )
    )
    effect = SummonEffect(target=target_obj)
    effect2 = BuffEffect(target=target_obj, attack=10, health=10, operator=Ops_.GROW)
    return Spell(activation_effect=...)


# Give ALL units -3|-0 this round. Deal 3 to ALL units.
def Icequake():
    effect = BuffEffect(
        target=AutoEntitySelector.ALL_BOARD_UNITS, attack=-3, round_only=True
    )
    effect1 = DamageEffect(value=3, target=AutoEntitySelector.ALL_BOARD_UNITS)
    return Spell(activation_effect=[effect, effect1])


# Deal 15 to all enemies.Costs 2 less for each Dragon or Celestial ally you have.
def TheSkiesDescend():
    effect = DamageEffect(value=15, target=AutoEntitySelector.ALL_OPPONENT_UNITS)
    cost = DynamicCostModifier(value=...)
    # TODO dynamic value
    return Spell(activation_effect=effect, effects=cost)
