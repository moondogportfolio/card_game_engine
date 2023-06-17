import Sets.SET2.Champions as Set2Champions
import Sets.SET2.Spells as Set2Spells
from actions.activations.multiple_activations import MultipleActivationsEffect
from actions.activations.play_skill import PlaySkill
from actions.activations.recast_spell import RecastEventOfAction
from actions.attribute.buff import BuffCostEffect, BuffEffect
from actions.attribute.buff_everywhere import BuffEverywhereEffect
from actions.attribute.damage import DamageEffect
from actions.attribute.drain import DrainEffect
from actions.attribute.gain_mana_gem import GainManaGemEffect
from actions.attribute.heal import HealEffect
from actions.attribute.rally import RallyEffect
from actions.attribute.shuffle_attributes import StatShuffleEfect

from actions.create.create_card import CreateCardEffect
from actions.create.create_copy import CreateExactCopyEffect
from actions.keywords.add_keyword import AddKeywordEffect, AddRandomKeywordEffect
from actions.keywords.stun_effect import StunEffect
from actions.meta.create_ta import CreateTriggeredAction
from actions.movement.discard import DiscardEffect
from actions.movement.draw import (
    DrawEffect,
)
from actions.movement.kill import KillAction
from actions.movement.nba import NabEffect
from actions.movement.obliterate import ObliterateEffect
from actions.movement.summon import SummonEffect
from actions.movement.toss import TossEffect
from actions.reactions.action_modifier import ActionModifier
from actions.reactions.action_negator import ActionNegator
from actions.reactions.dynamic_attr_modifier import (
    DynamicAttackModifier,
    DynamicKeywordModifier,
)
from actions.reactions.triggered_action import TriggeredAction
from actions.reactions.value_triggered_action import (
    EventCounterEnum,
    ValueTriggeredAction,
)
from actions.transform.transform import TransformEffect
from card_classes.unit import StackableUnit, Unit
from entity_selectors.base_card_filter import BaseCardFilter
from entity_selectors.card_filter import CardFilter, DrawCardFilter
from enums.entity_events import EntityEvents
from enums.keywords import KeywordEnum
from enums.gamestate import GameStateEnums
from enums.location import LocEnum
from enums.operator import Ops_
from enums.origin_enum import OriginEnum
from enums.post_event_param import PostEventParam
from enums.subtypes import SubTypes_
from enums.types import Types_
from resolvable_enums.active_cards_selector import TargetShorthand
from resolvable_enums.auto_card_selector import AutoEntitySelector
from resolvable_enums.card_conditions import CardFlags
from resolvable_enums.player_conditions import PlayerFlags
from resolvable_enums.target_player import TargetPlayer
from value.player_statistic import PlayerStatistic


# When you draw an enemy card, reduce its cost by 1.
# Plunder: Nab 1.
def BlackMarketMerchant():
    effect = BuffCostEffect(
        target=PostEventParam.TARGET,
        value=1,
    )
    effect1 = TriggeredAction(
        event_filter=EntityEvents.DRAW,
        ally_enum=OriginEnum.T_OPPO_O_ALLY,
        action=effect,
    )
    effect2 = NabEffect()
    return Unit(play_plunder=effect2, effects=effect1)


# When I'm summoned, create in hand a random 1 cost spell from your regions.
def CoralCreatures():
    target_obj = BaseCardFilter(cost=1, owner_same_regions=True, type=Types_.SPELL)
    effect = CreateCardEffect(target_obj)
    return Unit(summon_effect=effect)


#
def Sapling():
    return Unit()


# Play: Kill an ally to summon 2 Saplings.
def BlightedCaretaker():
    effect = KillAction(target=TargetShorthand.ALLIED_BOARD_UNIT)
    effect1 = CreateCardEffect(
        Sapling,
        LocEnum.HOMEBASE,
        quantity=2,
        fizz_if_fail=effect1,
    )
    return Unit(play_effect=(effect, effect1))


# Round Start: Deal 1 to EVERYTHING.
def EmberMaiden():
    effect = DamageEffect(target=AutoEntitySelector.EVERYTHING)
    return Unit(round_start_effects=effect)


# When I'm summoned, create a random Sea Monster in hand.
def JaullHunters():
    effect = CreateCardEffect(target=BaseCardFilter(subtype=SubTypes_.SEA_MONSTER))
    return Unit(summon_effect=effect)


# Last Breath: Deal 1 to the enemy Nexus.
def PowderMonkey():
    effect = DamageEffect(
        target=TargetPlayer.OPPONENT,
        value=1,
    )
    return Unit(last_breath_effect=effect)


# Round Start: Deal 2 to me and summon a Powder Monkey.
def MonkeyIdol():
    effect = DamageEffect(target=AutoEntitySelector.SELF, value=2)
    effect1 = CreateCardEffect(PowderMonkey, LocEnum.HOMEBASE)
    return Unit(summon_effect=effect)


# Powder Kegs stack.
# All of your spells and skills deal 1 extra damage.
# Destroy me when your spell or skill damages enemies or the enemy Nexus.
def PowderKeg():
    effect1 = ObliterateEffect(target=AutoEntitySelector.SELF)
    effect2 = TriggeredAction(
        event_filter=EntityEvents.DAMAGE, ally_enum=OriginEnum.O_ALLY, action=effect1
    )
    effect3 = DynamicAttackModifier
    effect3 = ActionModifier(
        triggering_event=EntityEvents.DAMAGE,
        ally_enum=OriginEnum.O_ALLY,
        condition=...,
        parameter=...,
        operator=Ops_.INCREMENT,
        value=1,
        location=LocEnum.BATTLEFIELD,
    )
    # TODO event modifier
    return StackableUnit(effects=(effect2, effect3))


# Play: Summon a Powder Keg.
def PettyOfficer():
    effect1 = CreateCardEffect(target=PowderKeg, location=LocEnum.HOMEBASE)
    effect2 = CreateCardEffect(
        target=BaseCardFilter(
            cost=1,
        ),
        location=LocEnum.HOMEBASE,
    )
    return Unit(play_effect=(effect1, effect2))


# When I'm summoned or Round Start: Grant me +0|+1 for each card you drew last round,
# then shuffle my stats.
def Slotbot():
    value = PlayerStatistic.CARD_DREW_LAST_ROUND
    effect = BuffEffect(target=AutoEntitySelector.SELF, health=value)
    effect1 = StatShuffleEfect(target=AutoEntitySelector.SELF)
    return Unit(summon_effect=(effect, effect1), round_start_effects=(effect, effect1))


# To play me, discard 2.
# Attack: Draw 2 and give them Fleeting.
def BrashGambler():
    effect = DiscardEffect(quantity=2)
    effect1 = DrawEffect(
        quantity=2,
        is_fleeting=True,
    )
    return Unit(attack_commit_effect=effect1, play_requisite=effect)


# Round Start: Deal 1 to the enemy Nexus.
def Citybreaker():
    effect = DamageEffect(target=TargetPlayer.OPPONENT, value=1)
    return Unit(summon_effect=effect)


#
def LoyalBadgerbear():
    return Unit()


# Last Breath: Summon a Loyal Badgerbear.
def GrizzledRanger():
    effect = CreateCardEffect(
        LoyalBadgerbear,
        LocEnum.HOMEBASE,
    )
    return Unit(last_breath_effect=effect)


# When you play a 2 cost card, draw 1 and give it Fleeting.
def InsightfulInvestigator():
    # TODO condition
    effect = DrawEffect(
        is_fleeting=True,
    )
    effect1 = TriggeredAction(
        event_filter=EntityEvents.PLAY,
        ally_enum=OriginEnum.T_ALLY,
        action=effect,
        condition=...,
    )
    return Unit(summon_effect=effect1)


# When I'm summoned, summon a random 1 cost follower and grant it Scout.
def IslandNavigator():
    effect = CreateCardEffect(
        target=BaseCardFilter(cost=1, flags=CardFlags.IS_FOLLOWER),
        keywords=KeywordEnum.SCOUT,
    )
    return Unit(summon_effect=effect)


# Play: Transform an ally into a random 5 cost follower.
def MystifyingMagician():
    effect = TransformEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        new_form=BaseCardFilter(cost=5, flags=CardFlags.IS_FOLLOWER, quantity=1),
    )
    return Unit(play_effect=effect)


# Allegiance: Nab 1 and create a Warning Shot in hand.
def YordleGrifter():
    effect = NabEffect()
    effect1 = CreateCardEffect(Set2Spells.WarningShot)
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_SELF,
        action=(effect, effect1),
        condition=CardFlags.ALLEGIANCE,
    )
    return Unit(effects=ta)


# Nexus Strike: Draw 1.
def AbyssalEye():
    effect = DrawEffect()
    return Unit(nexus_strike_effect=effect)


# When another ally dies, drain 1 from the enemy Nexus.
def NevergladeCollector():
    effect1 = DrainEffect(target=TargetPlayer.OPPONENT, value=1)
    ta = TriggeredAction(
        event_filter=EntityEvents.DIE,
        ally_enum=OriginEnum.T_ALLY,
        action=effect1,
    )
    return Unit(effects=ta)


# Play: Grant an enemy Vulnerable.
def RazorscaleHunter():
    effect = AddKeywordEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT,
        keyword=KeywordEnum.VULNERABLE,
    )
    return Unit(play_effect=effect)


# Enemies with 4 or less Power cannot damage me.
def ArmoredTuskrider():
    effect = ActionNegator(
        event_filter=EntityEvents.STRIKE,
        condition=...,
        ally_enum=OriginEnum.T_SELF_STRIKER_OPPO,
    )
    # TODO condition
    return Unit(effects=effect)


# Plunder: Heal allies and your Nexus 3, then Rally.
def CitrusCourier():
    effect1 = HealEffect(target=AutoEntitySelector.OWNER_NEXUS_AND_BOARD_UNITS, value=3)
    effect2 = RallyEffect()
    return Unit(play_plunder=(effect1, effect2))


# Plunder: Reduce the cost of allies in your hand and deck by 2.
def SmoothSoloist():
    effect = BuffCostEffect(
        target=CardFilter(location=(LocEnum.HAND, LocEnum.DECK)),
        value=2,
    )
    return Unit(play_plunder=effect)


# When I'm summoned, Draw a Sejuani.Plunder: Double the Power and Health of allies in your deck.
def TheTuskraider():
    effect = BuffEffect(
        target=CardFilter(location=(LocEnum.HAND, LocEnum.DECK)),
        attack=2,
        health=2,
        operator=Ops_.MULTIPLY,
    )
    effect1 = DrawEffect(filter_obj=BaseCardFilter(card_class=Set2Champions.Sejuani))
    return Unit(summon_effect=effect1, play_plunder=effect)


# When I'm summoned, draw a Swain.Round Start: Deal 1 to the enemy Nexus 3 times.
def TheLeviathan():
    effect1 = DrawEffect(
        filter_obj=DrawCardFilter(card_class=Set2Champions.Swain),
    )
    effect2 = DamageEffect(value=1, target=TargetPlayer.OPPONENT)
    # TODO recast
    effect3 = RecastEventOfAction(target=effect2, multiplier=3)
    effect3 = MultipleActivationsEffect(target=effect2, multiplier=3)
    return Unit(summon_effect=effect1, effects=effect3)


# When I'm summoned, draw a Gangplank. Double all damage dealt by your skills, spells and allies.
def TheDreadway():
    effect1 = DrawEffect(
        filter_obj=DrawCardFilter(card_class=Set2Champions.Gangplank),
    )
    effect = ActionModifier(
        triggering_event=EntityEvents.DAMAGE,
        ally_enum=OriginEnum.O_ALLY,
        parameter=...,
        operator=Ops_.MULTIPLY,
        value=2,
    )
    # TODO event parameter
    return Unit(summon_effect=effect1, effects=effect)


# Sea Monster allies have Fearsome. Attack: Give enemies -2|-0 this round.
def TerroroftheTides():
    effect = DynamicKeywordModifier(
        value=KeywordEnum.FEARSOME,
        target=CardFilter(subtype=SubTypes_.SEA_MONSTER),
    )
    effect1 = BuffEffect(
        target=CardFilter(owner=TargetPlayer.OPPONENT),
        attack=-2,
        round_only=True,
        triggering_effect=EntityEvents.ATTACK_COMMIT,
    )
    return Unit(effects=effect, attack_commit_effect=effect1)


# Plunder: Cast Cannon Barrage 6 times on randomly targeted enemies.
def RiptideRex():
    effect = PlaySkill(target=Set2Spells.CannonBarrage)
    effect1 = MultipleActivationsEffect(target=effect, multiplier=6)
    return Unit(play_plunder=effect1)


# When I'm summoned, draw a Miss Fortune.
# While I'm attacking, all your spells and skills deal 1 extra damage.
def TheSyren():
    effect1 = DrawEffect(
        filter_obj=BaseCardFilter(card_class=Set2Champions.MissFortune)
    )
    effect = ActionModifier(
        triggering_event=EntityEvents.DAMAGE,
        ally_enum=OriginEnum.O_ALLY,
        condition=...,
        parameter=...,
        operator=Ops_.INCREMENT,
        value=1,
        location=LocEnum.BATTLEFIELD,
    )
    # TODO spell damage
    return Unit(summon_effect=effect1, effects=effect)


# When I'm summoned, Toss 2 and create 2 Treasures in your deck.
def ShipwreckHoarder():
    effect = TossEffect(quantity=2)
    effect1 = CreateCardEffect(
        target=BaseCardFilter(quantity=2, subtype=SubTypes_.TREASURE),
        location=LocEnum.DECK,
    )
    return Unit(summon_effect=(effect, effect1))


# When you summon a follower, kill it to summon an Overgrown Snapvine.
def OvergrownSnapvine():
    effect1 = KillAction(target=PostEventParam.TARGET)
    effect2 = CreateCardEffect(
        target=OvergrownSnapvine, location=LocEnum.HOMEBASE, fizz_if_fail=effect1
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=(effect1, effect2),
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
    )
    return Unit(effects=ta)


# When I'm summoned, grant all enemies Vulnerable.
def SheriffLarietteRose():
    effect = AddKeywordEffect(
        target=CardFilter(owner=TargetPlayer.OPPONENT),
        keyword=KeywordEnum.VULNERABLE,
    )
    return Unit(summon_effect=effect)


# When I'm summoned, give other allies +1|+1 this round.
def GenevieveElmheart():
    effect = BuffEffect(
        target=CardFilter(),
        exclude_origin=True,
        attack=1,
        health=1,
        round_only=True,
    )
    return Unit(summon_effect=effect)


# When you draw a card, give it Fleeting and create an exact copy of it in hand.
def ChiefMechanistZevi():
    effect1 = AddKeywordEffect(
        target=PostEventParam.TARGET,
        keyword=KeywordEnum.FLEETING,
    )
    effect2 = CreateExactCopyEffect(target=PostEventParam.TARGET)
    ta = TriggeredAction(
        event_filter=EntityEvents.DRAW,
        action=(effect1, effect2),
        ally_enum=OriginEnum.T_ALLY,
    )
    return Unit(effects=ta)


# Attack: Stun all damaged enemies.
def AurokGlinthorn():
    effect = StunEffect(
        target=CardFilter(owner=TargetPlayer.OPPONENT, flags=CardFlags.IS_DAMAGED)
    )
    return Unit(attack_commit_effect=effect)


# When I'm summoned, draw 1.
# Then, if you've played at least 10 other cards with different names, grant me +4|+0.
def Subpurrsible():
    effect = DrawEffect()
    effect1 = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=4,
    )
    ta = ValueTriggeredAction(
        event_filter=EntityEvents.PLAY,
        threshold=10,
        action_on_value=effect1,
        ally_enum=OriginEnum.T_ALLY,
        condition=EventCounterEnum.UNIQUE_TARGETS,
    )
    return Unit(summon_effect=effect, effects=ta)


# When I'm summoned, draw a spell that costs 3 or less from your deck.
def ZapSprayfin():
    effect = DrawEffect(filter_obj=DrawCardFilter(type=Types_.SPELL, cost=(0, 3)))
    return Unit(summon_effect=effect)


# Plunder: Grant 1 cost allies everywhere +1|+0.
def JaggedTaskmaster():
    effect = BuffEverywhereEffect(
        filter_obj=BaseCardFilter(cost=1),
        attack=1,
    )
    return Unit(play_plunder=effect)


#
def Dragonling():
    return Unit()


# Round Start: Summon a Dragonling if you cast 2+ spells last round.
def EyeoftheDragon():
    effect = CreateCardEffect(
        Dragonling,
        LocEnum.HOMEBASE,
        condition=PlayerFlags.FLOW,
    )
    return Unit(round_start_effects=effect)


#
def HornsoftheDragon():
    return Unit()


#
def SlipperyWaverider():
    return Unit()


#
def GreathornCompanion():
    return Unit()


#
def TheBeastBelow():
    return Unit()


#
def GoldenNarwhal():
    return Unit()


#
def IronBallista():
    return Unit()


#
def GreenfangWarden():
    return Unit()


# Other allies with 5+ Power have Overwhelm.
def StormclawUrsine():
    effect = DynamicKeywordModifier(
        value=KeywordEnum.OVERWHELM,
        target=CardFilter(attack=(5, 0)),
    )
    return Unit(effects=effect)


# Plunder: I transform into Stormclaw Ursine.
def UrsineSpiritwalker():
    effect = TransformEffect(target=AutoEntitySelector.SELF, new_form=StormclawUrsine)
    return Unit(play_plunder=effect)


# When I'm summoned, summon a Golden Narwhal for your opponent.
def HuntingFleet():
    effect = CreateCardEffect(
        GoldenNarwhal,
        LocEnum.HOMEBASE,
    )
    return Unit(play_effect=effect)


# Plunder: Get an empty mana gem.
def Wolfrider():
    effect = GainManaGemEffect(
        condition=PlayerFlags.PLUNDER,
    )


# When I'm summoned, create a Dragon's Protection in hand.
def ScalesoftheDragon():
    effect = CreateCardEffect(
        Set2Spells.DragonsProtection,
        LocEnum.HOMEBASE,
    )
    return Unit(play_effect=effect)


# When I'm drawn, I cost 1 less this round.
def PatrolWardens():
    effect = BuffCostEffect(
        target=AutoEntitySelector.SELF,
        round_only=True,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.DRAW,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
    )
    return Unit(effects=effect)


# When I'm summoned, Toss 3.
def DeadbloomWanderer():
    effect = TossEffect(
        quantity=3,
    )
    return Unit(summon_effect=effect)


# Play: Obliterate an enemy with less Health than me.
def DevoureroftheDepths():
    effect = PlaySkill(target=Set2Spells.Devour)
    return Unit(play_effect=effect)


#
def BubbleBear():
    return Unit()


# When I'm summoned, ALL players draw 1.
def VeteranInvestigator():
    effect = DrawEffect(
        player=TargetPlayer.ALL_PLAYERS,
    )
    return Unit(play_effect=effect)


# Last Breath: Toss 2 and heal your Nexus 2.
def ThornyToad():
    effect = TossEffect(quantity=2)
    effect1 = HealEffect(value=2, target=TargetPlayer.ORIGIN_OWNER)
    return Unit(last_breath_effect=(effect, effect1))


#
def RuthlessRaider():
    return Unit()


# Play: Deal 1 to an ally to deal 2 to the enemy Nexus.
def ImperialDemolitionist():
    effect = PlaySkill(target=Set2Spells.BlackPowderGrenade)
    return Unit(play_effect=effect)


# When I'm summoned, grant the strongest enemy Vulnerable.
def HiredGun():
    effect = AddKeywordEffect(
        target=AutoEntitySelector.STRONGEST_OPPONENT_BOARD_UNIT,
        keyword=KeywordEnum.VULNERABLE,
    )
    return Unit(summon_effect=effect)


# When I'm summoned, summon a Powder Keg.
def DreadwayDeckhand():
    effect = CreateCardEffect(
        PowderKeg,
        LocEnum.HOMEBASE,
    )
    return Unit(summon_effect=effect)


# Summon me from hand the first time you've played 2 spells each round.
def ClawsoftheDragon():
    effect1 = SummonEffect(target=AutoEntitySelector.SELF)
    effect2 = ValueTriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL,
        ally_enum=OriginEnum.T_ALLY,
        action_on_value=effect1,
        threshold=2,
        location=LocEnum.HAND,
    )
    return Unit(effects=effect2)


#
def Shellshocker():
    return Unit()


#
def ProwlingCutthroat():
    return Unit()


# When I'm summoned, draw 1 at the next Round Start and give it Fleeting.
def PoolShark():
    effect = DrawEffect(
        quantity=1,
        is_fleeting=True,
    )
    ta = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START, action=effect, activate_once=True
    )
    effect1 = CreateTriggeredAction(
        triggered_action=ta, target=TargetPlayer.ORIGIN_OWNER
    )
    return Unit(summon_effect=effect1)


# Plunder: Grant me 2 random keywords.
def PlunderPoro():
    effect = AddRandomKeywordEffect(
        target=AutoEntitySelector.SELF,
        count=2,
    )
    return Unit(play_plunder=effect)


# Plunder: Grant me +1|+1.
def JaggedButcher():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=1,
        health=1,
    )
    return Unit(play_plunder=effect)


# When I'm summoned, Toss 3.
def DregDredgers():
    effect = TossEffect(quantity=3)
    return Unit(effects=effect)


# The first time an ally dies, grant me +2|+2.
def Barkbeast():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=2,
        health=2,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.DIE,
        action=effect,
        ally_enum=OriginEnum.T_ALLY,
        activate_once=True,
    )
    return Unit(effects=ta)


# When allies attack, deal 1 to the enemy Nexus.
def CrackshotCorsair():
    effect = PlaySkill(target=Set2Spells.Crackshot)
    ta = TriggeredAction(
        event_filter=EntityEvents.PLAYER_ATTACK_COMMIT,
        action=effect,
        ally_enum=OriginEnum.T_ALLY,
    )
    return Unit(effects=ta)


#
def Valor():
    return Unit()


#
def Longtooth():
    return Unit()


# When I'm Recalled, transform me into Concussive Palm.
def TailoftheDragon():
    effect = TransformEffect(
        target=AutoEntitySelector.SELF,
        new_form=Set2Spells.ConcussivePalm,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.RECALL,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
    )
    return Unit(effects=ta)


#
def ViciousPlatewyrm():
    return Unit()
