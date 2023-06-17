from actions.activations.play_skill import PlaySkill
from actions.attribute.buff import BuffEffect
from actions.attribute.damage import DamageEffect
from actions.attribute.heal import HealEffect
from actions.attribute.rally import RallyEffect
from actions.attribute.refill_mana import RefillSpellMana
from actions.create.create_card import CreateCardEffect
from actions.create.create_copy import CreateExactCopyEffect
from actions.create.create_hand_cards import GenerateCoinEffect
from actions.keywords.add_keyword import AddKeywordEffect
from actions.meta.create_ta import CreateTriggeredAction
from actions.movement.draw import DrawEffect
from actions.movement.predict import PredictEffect
from actions.on_value.empower import EmpowerEffect
from actions.reactions.action_negator import ActionNegator
from actions.reactions.dynamic_attr_modifier import (
    DynamicAttackModifier,
)
import Sets.SET7.Skills as Set7Skills
import Sets.SET7.Spells as Set7Spells
from actions.reactions.event_filter import EventFilter
from actions.reactions.triggered_action import (
    AllyOrigin_TA,
    TriggeredAction,
)
from actions.traps.set_trap import PlantFlashBombTrap
from card_classes.unit import Unit
from conditions.base_condition import Condition
from entity_selectors.base_card_filter import BaseCardFilter, BaseCardRandomSelector
from entity_selectors.card_filter import CardFilter
from entity_selectors.input import ChoiceAction
from enums.entity_events import EntityEvents
from enums.keywords import KeywordEnum
from enums.location import LocEnum
from enums.origin_enum import OriginEnum
from enums.post_event_param import PostEventParam
from resolvable_enums.active_cards_selector import TargetShorthand
from resolvable_enums.auto_card_selector import AutoEntitySelector
from resolvable_enums.target_player import TargetPlayer
from value.player_statistic import PlayerStatistic


class ActivatePlunderEffects:
    ...


# Play: Predict, then draw 1 and reduce its cost by 1.
def AugmentedClockling():
    effect = PredictEffect()
    effect1 = DrawEffect(cost_reduction=1)
    return Unit(play_effect=(effect, effect1), cardcode="07PZ009")


# When you play a Spell, plant 1 Flashbomb Trap randomly in the top 8 cards of the enemy deck.
def FlashbombPeddler():
    effect = PlantFlashBombTrap()
    effect1 = AllyOrigin_TA(
        event_filter=EntityEvents.PLAY_SPELL,
        action=effect,
        ally_enum=OriginEnum.T_ALLY,
    )
    return Unit(effects=effect1, cardcode="07PZ017")


# Plunder: Grant me +2|+0.
def ElegantEdge():
    effect = BuffEffect(target=AutoEntitySelector.SELF, attack=2)
    return Unit(play_plunder=effect, cardcode="07NX008")


# Plunder: Grant me +3|+0.


def DashingDandy():
    effect = BuffEffect(target=AutoEntitySelector.SELF, attack=3)
    return Unit(play_plunder=effect, cardcode="07NX006")


# Plunder: Grant all allies +1|+0.


def DametheDespoiler():
    effect = BuffEffect(target=AutoEntitySelector.ALL_BOARD_UNITS, attack=1)
    return Unit(play_plunder=effect, cardcode="07NX015")


# When I'm summoned, activate all ally Plunder effects.


def AdroitArtificer():
    # TODO activate plunder fx
    effect = ActivatePlunderEffects()
    return Unit(summon_effect=effect, cardcode="07NX004")


# Play: Deal 1 to the enemy Nexus or activate an ally's Plunder effect.


def DaringDemolisher():
    effect = DamageEffect(target=TargetPlayer.OPPONENT, value=1)
    effect1 = ActivatePlunderEffects()
    effect2 = ChoiceAction(choices=(effect, effect1))
    return Unit(effects=effect, cardcode="07NX001T2")


# Play: The next time you play a unit this round, summon an exact Ephemeral copy of it.


def MasterBingwentheSieve():
    action = CreateExactCopyEffect(target=PostEventParam.TARGET, is_ephemeral=True)
    effect = TriggeredAction(
        event_filter=EntityEvents.PLAY,
        round_only=True,
        activate_once=True,
        action=action,
        ally_enum=OriginEnum.T_ALLY,
    )
    effect1 = CreateTriggeredAction(triggered_action=effect)
    return Unit(effects=effect1)


# Play: Recall the strongest enemy.
# If you've spent 16+ mana this round, Recall all enemies instead.


def TheOldTimer():
    effect = PlaySkill(target=Set7Skills.MoreThanYouCanChew)
    return Unit(cardcode="07IO023", play_effect=effect)


# Nexus Strike: Create a Coin in hand.


def AttentiveAccountant():
    return Unit(nexus_strike_effect=GenerateCoinEffect(), cardcode="07IO009")


# Play: Heal an ally or your Nexus 3 and create a Coin in hand.


def SmoothMixologist():
    # ally or nexus
    effect = HealEffect(target=TargetShorthand.ALLY_NEXUS_OR_BOARD_UNITS, value=3)
    effect1 = GenerateCoinEffect()
    return Unit(play_effect=(effect, effect1), cardcode="07IO019")


# When I'm summoned, create a Coin in hand.


def PitProfessional():
    effect = GenerateCoinEffect()
    return Unit(cardcode="07IO013", summon_effect=effect)


# When I'm summoned, create a Fleeting Bout Security in hand and grant other Bout Security +1|+1.
# Empowered 5: Quick Attack.


def BoutSecurity():
    effect = CreateCardEffect(target=BoutSecurity, is_fleeting=True)
    effect1 = BuffEffect(
        target=CardFilter(
            location=LocEnum.HOMEBASE,
            card_type=BoutSecurity,
            exclude_origin=True,
        ),
        attack=1,
        health=1,
    )
    empower = EmpowerEffect(value=5, keywords=KeywordEnum.QUICKSTRIKE)
    return Unit(effects=empower, cardcode="07IO012", summon_effect=(effect1, effect))


# When you refill mana, grant me +1|+0 for each mana refilled.


def MadOlBabs():
    effect = BuffEffect(target=AutoEntitySelector.SELF, attack=PostEventParam.VALUE)
    effect1 = TriggeredAction(
        event_filter=EntityEvents.REFILL_MANA,
        ally_enum=OriginEnum.T_ALLY,
        action=effect,
    )
    return Unit(effects=effect1, cardcode="07BW018")


# Plunder: Summon a random 1 cost follower and grant it Brash.


def BrazenBuccaneer():
    target = BaseCardRandomSelector(cost=1, is_follower=True)
    effect = CreateCardEffect(target=target, keywords=KeywordEnum.BRASH)
    return Unit(play_plunder=effect, cardcode="07BW021")


# When I'm summoned, create a Fleeting Mako in hand.


def Nukkle():
    effect = CreateCardEffect(target=Mako, is_fleeting=True)
    return Unit(summon_effect=effect, cardcode="07BW040")


# When I'm summoned, create a Fleeting Bull in hand.


def Mako():
    effect = CreateCardEffect(target=Bull, is_fleeting=True)
    return Unit(summon_effect=effect, cardcode="07BW040T1")


# When I'm summoned, Rally.


def Bull():
    effect = RallyEffect()
    return Unit(summon_effect=effect, cardcode="07BW040T2")


# Last Breath: Create a Coin in hand.
def PocketPicker():
    effect = GenerateCoinEffect()
    return Unit(last_breath_effect=effect, cardcode="07BW003")


# When I'm summoned, create a Fleeting Prize Fight in hand.
def FivePunchPablo():
    effect1 = CreateCardEffect(target=..., is_fleeting=True)
    return Unit(summon_effect=effect1, cardcode="07BW014")


#


def Angel():
    return Unit(cardcode="07BW013")


# Plunder: Refill 1 Spell mana and create a random 1 cost Unit from your regions in hand.
def FatherFury():
    card = BaseCardRandomSelector(owner_same_regions=True, cost=1)
    effect1 = RefillSpellMana()
    effect = CreateCardEffect(target=card)
    return Unit(play_plunder=(effect1, effect), cardcode="07BW027")


# When you summon an ally, create a Fleeting Prize Fight in hand.
# When an ally survives damage, grant it Brash.
def TheKingsCourt():
    effect1 = AddKeywordEffect(target=PostEventParam.TARGET, keyword=KeywordEnum.BRASH)
    effect = TriggeredAction(
        event_filter=EntityEvents.DAMAGE_SURVIVE,
        ally_enum=...,
        action=effect1,
    )
    effect2 = CreateCardEffect(target=Set7Spells.PrizeFight, is_fleeting=True)
    effect3 = TriggeredAction(
        event_filter=EntityEvents.DAMAGE_SURVIVE,
        ally_enum=...,
        action=effect2,
    )
    return Unit(effects=(effect, effect3), cardcode="07BW004")


# When you activate Plunder, draw 1 and give it Fleeting.
def Inferna():
    effect = DrawEffect(is_fleeting=True)
    effect1 = TriggeredAction(
        event_filter=EntityEvents.ACTIVATE_PLUNDER,
        ally_enum=...,
        action=effect,
    )
    return Unit(effects=effect1, cardcode="07BW025")


# Spend 6 mana to play me as Frostcoat Mother instead.
def FrostcoatCub():
    effect1 = ...
    # TODO play me as X instead
    return Unit(effects=effect1, cardcode="07FR008T2")


#


def FrostcoatMother():
    return Unit(cardcode="07FR008T1")


# I don't take damage from allied spells or skills.
def ThrallBulwark():
    # TODO post event condition
    effect = ActionNegator(
        event_filter=EntityEvents.DAMAGE,
        ally_enum=OriginEnum.T_SELF_O_ALLY,
        condition=Condition(
            target=...
        )
    )
    return Unit(effects=effect, cardcode="07FR005")


#
def CarvedBladetwirler():
    return Unit(cardcode="07BC005")


# Round Start: Heal me and your Nexus 1.
def CosmicYoungling():
    effect = HealEffect(target=AutoEntitySelector.ORIGIN_AND_NEXUS, value=1)
    return Unit(round_start_effects=effect, cardcode="07MT003")


# I have +1|+0 for each Ephemeral ally you've summoned this game.
def FallenSandsGeneral():
    effect = DynamicAttackModifier(value=PlayerStatistic.EPHEMERALS_SUMMONED)
    return Unit(effects=effect, cardcode="07SH023")


# When I'm summoned, create at the bottom of your deck two random level 2 champions
# that aren't in your hand, deck, or play.
def SecretKeeper():
    target = BaseCardFilter(quantity=2, custom_filter=lambda x, y: ...)
    effect1 = CreateCardEffect(target=target, index=-1)
    return Unit(cardcode="07SH018", summon_effect=effect1)
