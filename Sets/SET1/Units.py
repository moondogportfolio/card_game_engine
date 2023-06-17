from Sets.SET1.CustomSpells import HeartoftheFluftEffect
import Sets.SET1.Skills as Set1Skills
import Sets.SET1.Spells as Set1Spells
import Sets.SET1.Champions as Set1Champions
from actions.activations.play_skill import PlaySkill
from actions.attribute.buff import BuffCostEffect, BuffEffect
from actions.attribute.buff_everywhere import BuffEverywhereEffect
from actions.attribute.damage import DamageEffect
from actions.attribute.frostbite import FrostbiteEffect
from actions.attribute.gain_mana_gem import GainManaGemEffect
from actions.attribute.heal import HealEffect
from actions.attribute.rally import RallyEffect
from actions.attribute.refill_mana import RefillSpellMana
from actions.attribute.support import SupportEffect
from actions.base_action import TestBaseAction

from actions.create.create_card import CreateCardEffect
from actions.create.create_copy import CreateExactCopyEffect
from actions.keywords.add_keyword import AddKeywordEffect
from actions.keywords.stun_effect import StunEffect
from actions.meta.create_ta import CreateTriggeredAction
from actions.movement.discard import DiscardEffect
from actions.movement.draw import (
    DrawEffect,
    DrawSpecificReturnRestEffect,
)
from actions.movement.kill import KillAction
from actions.movement.move import MoveEffect
from actions.movement.recall import RecallEffect
from actions.movement.revive import ReviveEffect
from actions.movement.summon import SummonEffect
from actions.postevent import PostEventParamGetter
from actions.reactions.action_modifier import ActionModifier
from actions.reactions.action_replacement import ActionReplacement
from actions.reactions.dynamic_attr_modifier import (
    DynamicCostModifier,
)
from actions.reactions.event_filter import EventFilter
from actions.reactions.onceyouve import OnceYouve
from actions.reactions.state_triggered_action import StateTriggeredAction
from actions.reactions.triggered_action import TriggeredAction
from actions.traps.set_trap import (
    PlantPuffcaps,
)
from card_classes.unit import Unit
from conditions.base_condition import Condition, PostEventTargetCondition
from entity_selectors.base_card_filter import BaseCardFilter, InvokeBaseCardFilter
from entity_selectors.card_filter import (
    CardFilter,
    CardFilterSelector,
    DrawCardFilter,
    SimpleCardFilter,
)
from entity_selectors.input import ChoiceAction, ChoiceBaseCard, Input
from entity_selectors.target_game_card import TargetEntity
from enums.base_action_attribute import BaseActionAttrEnum
from enums.card_rarity import CardRarity
from enums.card_sorters import CardSorter
from enums.counters import TrapEnums
from enums.deck_archetypes import DeckArchetypes
from enums.entity_events import EntityEvents
from enums.keywords import KeywordEnum
from enums.gamestate import GameStateEnums
from enums.location import LocEnum
from enums.operator import Ops_
from enums.origin_enum import OriginEnum
from enums.post_event_param import PostEventParam
from enums.region import RegionEnum
from enums.spell_speed import SpellSpeedEnum
from enums.subtypes import SubTypes_
from enums.types import Types_
from events.event_query import EventQuery
from resolvable_enums.active_cards_selector import TargetShorthand
from resolvable_enums.auto_card_selector import AutoEntitySelector
from resolvable_enums.card_conditions import CardFlags
from resolvable_enums.player_conditions import PlayerFlags
from resolvable_enums.target_player import TargetPlayer
from value.entity_attribute import EntityAttribute
from value.player_statistic import PlayerStatistic


# Attack: Give other attacking allies +1|+0 this round.
def ArenaBattlecaster():
    effect = BuffEffect(
        target=SimpleCardFilter(exclude_origin=True),
        attack=1,
        round_only=True,
    )
    return Unit(attack_commit_effect=effect)


# Round Start: Discard your lowest cost card to draw 1.
def ArenaBookie():
    effect = DiscardEffect(
        target=TargetEntity(
            choices=CardFilter(location=LocEnum.HAND),
            sorter=CardSorter.CHEAPEST,
        )
    )
    effect1 = DrawEffect(fizz_if_fail=effect)
    return Unit(round_start_effects=(effect, effect1))


# When you summon an Elite, grant it +1|+1.
def Battlesmith():
    effect = BuffEffect(
        target=PostEventParam.TARGET,
        attack=1,
        health=1,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        action=effect,
        condition=PostEventTargetCondition(
            condition=CardFlags.IS_SUBTYPE_X,
            parameter=SubTypes_.ELITE,
        ),
    )
    return Unit(effects=ta)


# Nexus Strike: Create in hand an exact copy of a random spell from the enemy's deck.
def ChempunkPickpocket():
    target_obj = CardFilterSelector(
        owner=TargetPlayer.OPPONENT,
        location=LocEnum.DECK,
        type=Types_.SPELL,
    )
    effect = CreateExactCopyEffect(target=target_obj)
    return Unit(nexus_strike_effect=effect)


# When I survive damage, deal 1 to the enemy Nexus.
def CrimsonDisciple():
    effect = DamageEffect(
        target=TargetPlayer.OPPONENT,
        value=1,
    )
    return Unit(damage_survive_effect=effect)


# When you Stun or Recall a unit, grant me +2|+0.
def FaeBladetwirler():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=2,
    )
    ta = TriggeredAction(
        event_filter=(EntityEvents.STUN, EntityEvents.RECALL),
        action=effect,
        ally_enum=OriginEnum.O_ALLY,
    )
    return Unit(effects=ta)


# When you summon an ally, give me +1|+0 this round.
def GreengladeDuo():
    effect = BuffEffect(target=AutoEntitySelector.SELF, attack=1, round_only=True)
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
    )
    return Unit(effects=effect)


# Support: Give my supported ally Elusive this round.
def IntrepidMariner():
    effect = SupportEffect(
        keyword=KeywordEnum.ELUSIVE,
        round_only=True,
    )
    return Unit(support_effect=effect)


# Grant me +1|+1 and Challenger once you've cast a 6+ cost spell this game.
def MageseekerPersuader():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=1,
        health=1,
        keyword=KeywordEnum.CHALLENGER,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL,
        action=effect,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        condition=...,
    )
    return Unit(effects=effect)


# When I'm summoned, draw a Poro if you Behold a Poro.
def PoroHerder():
    effect = DrawEffect(
        quantity=1,
        filter_obj=DrawCardFilter(subtype=SubTypes_.PORO),
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
        condition=Condition(
            target=TargetPlayer.ORIGIN_OWNER,
            condition=PlayerFlags.IS_BEHOLDING_X_CARD,
            parameter=SubTypes_.PORO,
        ),
    )
    return Unit(effects=ta)


# Last Breath: The next time an Ephemeral ally attacks, revive me attacking.
def SharkChariot():
    effect = ReviveEffect(
        target=AutoEntitySelector.SELF,
        location=LocEnum.BATTLEFIELD,
    )
    effect1 = TriggeredAction(
        event_filter=EntityEvents.PLAYER_ATTACK_COMMIT,
        ally_enum=OriginEnum.T_ALLY,
        action=effect,
        condition=Condition(
            target=TargetPlayer.ORIGIN_OWNER,
            condition=PlayerFlags.HAS_X_CARD_IN_PLAY,
            parameter=CardFilter(keyword=KeywordEnum.EPHEMERAL),
        ),
    )
    return Unit(last_breath_effect=effect1)
    # TODO


# When you cast a spell, grant the top ally in your deck +1|+1.
def StarlitSeer():
    effect = BuffEffect(
        target=AutoEntitySelector.TOP_ALLY_IN_DECK,
        attack=1,
        health=1,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL, action=effect, ally_enum=OriginEnum.T_ALLY
    )
    return Unit(effects=effect)


# When you cast a spell, grant me +1|+1.
def AssemblyBot():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=1,
        health=1,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL, action=effect, ally_enum=OriginEnum.T_ALLY
    )
    return Unit(effects=effect)


# When I'm summoned, give other Spider allies +1|+0 and enemies -1|-0 this round.
def FrenziedSkitterer():
    effect = BuffEffect(
        target=CardFilter(owner=TargetPlayer.OPPONENT),
        attack=-1,
        round_only=True,
    )

    effect1 = BuffEffect(
        target=CardFilter(subtype=SubTypes_.SPIDER),
        target_exclusion=AutoEntitySelector.SELF,
        attack=1,
        round_only=True,
    )
    return Unit(summon_effect=(effect, effect1))


# Attack: Grant me +1|+0 for each Ephemeral ally you have.
def IronHarbinger():
    effect1 = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=CardFilter(
            keyword=KeywordEnum.EPHEMERAL,
            output_count=True,
        ),
    )
    return Unit(attack_commit_effect=effect1)


# When another ally dies, deal 1 to the enemy Nexus.
def PhantomPrankster():
    effect = DamageEffect(target=TargetPlayer.OPPONENT, value=1)
    ta = TriggeredAction(
        event_filter=EntityEvents.DIE, action=effect, ally_enum=OriginEnum.T_ALLY
    )
    return Unit(effects=ta)


# Strike: If I struck a unit with 0 Power, kill it.
def RimefangWolf():
    # `TODO
    effect = KillAction(target=PostEventParam.TARGET)
    ta = TriggeredAction(
        event_filter=EntityEvents.STRIKE,
        ally_enum=OriginEnum.S_STRIKER,
        condition=...,
        action=effect,
    )
    return Unit(effects=ta)


# When I'm summoned, move Draven to the top of your deck if you don't have him in hand or in play.
def DravensBiggestFan():
    target_obj = CardFilter(location=LocEnum.DECK, card_class=Set1Champions.Draven)
    condition = Condition(
        target=Set1Champions.Draven,
        condition=CardFlags.IS_IN_HAND_OR_PLAY,
        invert_result=True,
    )
    effect = MoveEffect(target=target_obj, index=0)
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        condition=condition,
        ally_enum=OriginEnum.T_SELF,
    )
    return Unit(summon_effect=effect)


# Strike: Draw a spell.
def Rivershaper():
    effect = DrawEffect(filter_obj=DrawCardFilter(type=Types_.SPELL))
    return Unit(strike_effect=effect)


# The first time an allied Lucian dies, grant me +1|+1 and Double Attack.
def SennaSentinelofLight():
    effect1 = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=1,
        health=1,
        keyword=KeywordEnum.DOUBLESTRIKE,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.DIE, action=effect1, condition=..., activate_once=True
    )
    return Unit(effects=ta)


# When I'm summoned, Recall all other allies.
def SolitaryMonk():
    effect = RecallEffect(
        target=CardFilter(),
        target_exclusion=AutoEntitySelector.SELF,
    )
    return Unit(summon_effect=effect)


# When I'm summoned, create a For Demacia! in hand.
def VanguardSergeant():
    effect = CreateCardEffect(Set1Spells.ForDemacia)
    return Unit(summon_effect=effect)


# To play me, kill 2 allies.
def AncientCrocolith():
    effect = KillAction(target=TargetEntity(quantity=2, minimum=2))
    return Unit(play_requisite=effect)


# Allegiance: Grant the top ally in your deck +3|+3 and Overwhelm.
def AvarosanOutriders():
    effect = BuffEffect(
        target=AutoEntitySelector.TOP_ALLY_IN_DECK,
        attack=3,
        health=3,
        keyword=KeywordEnum.OVERWHELM,
    )
    return Unit(summon_allegiance_effect=effect)


# Allegiance: Grant me +1|+1 and Overwhelm.
def BasiliskRider():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=1,
        health=1,
        keyword=KeywordEnum.OVERWHELM,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
        condition=CardFlags.ALLEGIANCE,
    )
    return Unit(effects=ta)


# When I'm summoned, create 2 Mushroom Clouds in hand.
def ChumpWhump():
    effect = CreateCardEffect(
        quantity=2,
        target=Set1Spells.MushroomCloud,
    )
    return Unit(summon_effect=effect)


def CrowdFavoriteEffect(origin):
    value = CardFilter(exclude_origin=True)
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=value,
        health=value,
    )
    return effect


# When I'm summoned, grant me +1|+1 for each other ally you have.
def CrowdFavorite():
    return Unit(summon_effect=CrowdFavoriteEffect)


# Last Breath: Create in hand a random Epic card from your regions.
def EminentBenefactor():
    effect = CreateCardEffect(
        target=BaseCardFilter(
            type=None, rarity=CardRarity.EPIC, owner_same_regions=True
        ),
    )
    return Unit(last_breath_effect=effect)


# When I'm summoned, deal 1 to all other allies.
def CrimsonAwakener():
    effect = DamageEffect(
        target=CardFilter(),
        target_exclusion=AutoEntitySelector.SELF,
        value=1,
    )
    return Unit(summon_effect=effect)


# All of your spells and skills deal 1 extra damage.
def Funsmith():
    effect = ActionModifier(
        event_filter=EntityEvents.DAMAGE,
        parameter=BaseActionAttrEnum.VALUE,
        operator=Ops_.INCREMENT,
        value=1,
        ally_enum=OriginEnum.O_ALLY,
        condition=...,
    )
    # TODO modifier vs attribute modifier
    return Unit(effects=effect)


# Allegiance: Summon a 1 cost ally from your deck.
def KinkouWayfinder():
    effect = SummonEffect(
        target=CardFilterSelector(location=LocEnum.DECK, cost=1),
    )
    return Unit(summon_allegiance_effect=effect)


# Play: Grant an ally +2|+2.
def LaurentBladekeeper():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=2,
        health=2,
    )
    return Unit(play_effect=effect)


# When you summon a 1 cost ally, grant it +2|+2.
def ProfessorvonYipp():
    effect = BuffEffect(
        target=PostEventParam.TARGET,
        attack=2,
        health=2,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_OPPO_O_ALLY,
    )
    return Unit(effects=ta)


# Grant me +2|+2 once you've cast a 6+ cost spell this game.
def MageseekerInciter():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=2,
        health=2,
    )
    effect1 = OnceYouve(state=PlayerFlags.HAS_PLAYED_A_6_COST_SPELL, action=effect)
    return Unit(effects=effect1)


# Play: Pick a follower. Transform me into an exact copy of it.
def ShadyCharacter():
    play = PlaySkill(target=Set1Skills.Impersonate)
    return Unit(play_effect=play)


# Allegiance: Create a Sumpworks Map in hand. It costs 0 this round.
def SumpsnipeScavenger():
    effect = CreateCardEffect(Set1Spells.SumpworksMap, coevent=effect1)
    effect1 = BuffCostEffect(
        target=PostEventParam.TARGET,
        value=0,
        operator=Ops_.SET,
        round_only=True,
    )
    return Unit(summon_allegiance_effect=(effect, effect1))


# Allegiance: Grant other allies +1|+1.
def VanguardBannerman():
    effect = BuffEffect(
        target=CardFilter(),
        target_exclusion=AutoEntitySelector.SELF,
        attack=1,
        health=1,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
        condition=CardFlags.ALLEGIANCE,
    )
    return Unit(effects=ta)


# Allegiance: Summon a Mistwraith.
def Wraithcaller():
    effect = CreateCardEffect(
        Mistwraith,
        LocEnum.HOMEBASE,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
        condition=CardFlags.ALLEGIANCE,
    )
    return Unit(effects=ta)


# When I'm summoned, grant other Spider allies +2|+0.
def ArachnoidHost():
    effect = BuffEffect(
        target=CardFilter(subtype=SubTypes_.SPIDER),
        target_exclusion=AutoEntitySelector.SELF,
        attack=2,
    )
    return Unit(summon_effect=effect)


# Play: Deal 1 to all enemies.
def ChempunkShredder():
    play = PlaySkill(target=Set1Skills.FaceMelter)
    return Unit(play_effect=play)


# Play: Kill an ally to summon a random follower that costs 2 more.
def EtherealRemitter():
    effect = CreateCardEffect(
        target=BaseCardFilter(cost=CustomFunctionEnum.REMITTER),
        fizz_if_fail=effect2,
    )
    effect2 = KillAction(target=TargetShorthand.ALLIED_BOARD_UNIT, coevent=effect)
    return Unit(play_effect=(effect2, effect))


# Play: Stun an enemy.
def ArachnoidSentry():
    play = PlaySkill(target=Set1Skills.ParalyzingBite)
    return Unit(play_effect=play)


# Play: Give an ally Barrier this round.
def BrightsteelProtector():
    effect = AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        keyword=KeywordEnum.BARRIER,
    )
    return Unit(play_effect=effect)


# Play: Grant an ally in hand +3|+3.
def JeweledProtector():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_HAND_UNIT,
        attack=3,
        health=3,
    )
    return Unit(play_effect=effect)


# Nexus Strike: Summon an exact copy of me.
def MidenstokkeHenchmen():
    effect = CreateExactCopyEffect(
        target=AutoEntitySelector.SELF,
        location=LocEnum.HOMEBASE,
    )
    return Unit(nexus_strike_effect=effect)


# When I'm summoned, grant me Lifesteal and Tough if an ally died this round.
def RadiantGuardian():
    effect = AddKeywordEffect(
        target=AutoEntitySelector.SELF,
        keyword=(KeywordEnum.LIFESTEAL, KeywordEnum.TOUGH),
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
        condition=PlayerFlags.ALLY_DIED_THIS_ROUND,
    )
    return Unit(effects=ta)


# Round Start: Frostbite the strongest enemy.
def RimetuskShaman():
    effect = FrostbiteEffect(
        target=AutoEntitySelector.STRONGEST_OPPONENT_BOARD_UNIT,
    )
    ta = TriggeredAction(event_filter=GameStateEnums.ROUND_START, action=effect)
    return Unit(effects=ta)


# Last Breath: Create a random Elite in hand.
def SwiftwingLancer():
    effect = CreateCardEffect(
        target=BaseCardFilter(subtype=SubTypes_.ELITE, quantity=1),
    )
    return Unit(last_breath_effect=effect)


# When an ally dies, refill your spell mana.
def TorturedProdigy():
    effect = RefillSpellMana(
        value=Ops_.MAX,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.DIE, action=effect, ally_enum=OriginEnum.T_ALLY
    )
    return Unit(effects=ta)


# When I'm summoned, draw 1 for each 5+ Power ally you have.
def TrifarianAssessor():
    effect = DrawEffect(
        quantity=CardFilter(
            attack=(5, 0),
            output_count=True,
        ),
    )
    return Unit(summon_effect=effect)


# Grant me +4|+0 and Quick Attack once you've cast a 6+ cost spell this game.
def UnstableVoltician():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=4,
        keyword=KeywordEnum.QUICKSTRIKE,
    )


# Your Burst and Focus spells cost 1 less.
def CloudDrinker():
    effect = DynamicCostModifier(
        value=1,
        target=CardFilter(
            location=LocEnum.HAND,
            type=Types_.SPELL,
            speed=(SpellSpeedEnum.BURST, SpellSpeedEnum.FOCUS),
        ),
        condition=CardFlags.IS_ON_THE_BOARD,
    )
    return Unit(effects=effect)


# Play: Combine all of our Poros into a Fluft of Poros, it gains their stats and keywords.
def HeartoftheFluft():
    effect = HeartoftheFluftEffect()
    return Unit(play_effect=effect)


# Last Breath: Summon a Heart of the Fluft.
def FluftofPoros():
    effect = CreateCardEffect(HeartoftheFluft, LocEnum.HOMEBASE)
    return Unit(last_breath_effect=effect)


# Round Start: Stun the weakest enemy.
def MinotaurReckoner():
    effect = StunEffect(
        target=AutoEntitySelector.WEAKEST_OPPONENT_UNIT,
    )
    ta = TriggeredAction(event_filter=GameStateEnums.ROUND_START, action=effect)
    return Unit(effects=ta)


# Play: Create an exact copy of a card in hand other than Zephyr Sage.
def ZephyrSage():
    effect = CreateCardEffect(
        target=CardFilter(
            type=None, exclude_card_class=ZephyrSage, location=LocEnum.HAND
        ),
        exact_copy=True,
    )
    return Unit(play_effect=effect)


# Round End: Reduce my cost by 1.
def AncientYeti():
    effect = BuffCostEffect(
        target=AutoEntitySelector.SELF,
        value=1,
    )
    ta = TriggeredAction(
        event_filter=GameStateEnums.ROUND_END, action=effect, location=LocEnum.HAND
    )
    return Unit(round_end_effects=effect)


# When I'm summoned, Frostbite enemies with 3 or less Health.
def IcyYeti():
    effect = FrostbiteEffect(
        target=CardFilter(owner=TargetPlayer.OPPONENT, health=(0, 3)),
    )
    return Unit(summon_effect=effect)


# When I'm summoned, revive the strongest dead allied champion.
def TheRekindler():
    effect = ReviveEffect(
        target=CardFilterSelector(
            sorter=CardSorter.STRONGEST,
            location=LocEnum.GRAVEYARD,
            flags=CardFlags.IS_CHAMPION,
        ),
    )
    return Unit(summon_effect=effect)


# When I'm summoned, grant me +1|+1 for each ally that has died.
def TheyWhoEndure():
    effect1 = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=PlayerStatistic.ALLY_DIED_THIS_GAME,
        health=PlayerStatistic.ALLY_DIED_THIS_GAME,
    )
    return Unit(summon_effect=effect1)


# Reduce my cost by 1 for each spell you've cast this game.
def PlazaGuardian():
    effect = DynamicCostModifier(value=PlayerStatistic.ALLY_DIED_THIS_GAME)
    return Unit(effects=effect)


# Reduce my cost by 1 for each ally that died this game.
def Scuttlegeist():
    effect = DynamicCostModifier(value=PlayerStatistic.ALLY_DIED_THIS_GAME)
    return Unit(effects=effect)


# Nexus Strike: Create a copy of me in hand.
def SilentShadowseer():
    effect = CreateCardEffect(SilentShadowseer)
    return Unit(nexus_strike_effect=effect)


# Round End: Grant other allies +1|+1 if an ally died this round.
def Dawnspeakers():
    effect = BuffEffect(
        target=CardFilter(),
        target_exclusion=AutoEntitySelector.SELF,
        attack=1,
        health=1,
    )
    ta = TriggeredAction(
        event_filter=GameStateEnums.ROUND_END,
        action=effect,
        condition=PlayerFlags.ALLY_DIED_THIS_ROUND,
    )
    return Unit(effects=ta)


# Last Breath: Revive me at the next Round Start and grant me +1|+1 for each time I've died.
def TheUndying():
    effect = ReviveEffect(target=AutoEntitySelector.SELF)
    effect1 = BuffEffect(target=AutoEntitySelector.SELF, attack=1, health=1)
    ta = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START,
        action=[effect, effect1],
        activate_once=True,
    )
    create = CreateTriggeredAction(triggered_action=ta)
    return Unit(last_breath_effect=create)


# Strike: Create in hand another random Challenger follower from your regions.
def LaurentChevalier():
    target_obj = BaseCardFilter(keyword=KeywordEnum.CHALLENGER, owner_same_regions=True)
    effect = CreateCardEffect(
        target_obj,
    )
    return Unit(strike_effect=effect)


# When another ally survives damage, grant it +1|+0.
def LegionVeteran():
    effect1 = BuffEffect(
        target=PostEventParam.TARGET,
        attack=1,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.DAMAGE_SURVIVE,
        action=effect1,
        ally_enum=OriginEnum.T_ALLY,
        condition=...,
    )
    return Unit(effects=ta)


#
def ShadowFiend():
    return Unit()


# Strike: Create a Shadow Fiend in hand.
def RenShadowblade():
    effect = CreateCardEffect(ShadowFiend)
    return Unit(strike_effect=effect)


# I deal double damage to the Nexus.
def ShirazatheBlade():
    effect = ActionModifier(
        event=EntityEvents.DAMAGE,
        parameter=...,
        operator=Ops_.MULTIPLY,
        value=2,
        condition=...,
    )
    return Unit(effects=effect)


# When I'm summoned, grant all allies in your deck +1|+1.
def AvarosanHearthguard():
    effect = BuffEffect(
        target=CardFilter(location=LocEnum.DECK),
        attack=1,
        health=1,
    )
    return Unit(summon_effect=effect)


# Support: Give my supported ally +3|+0 and Overwhelm this round.
def KatoTheArm():
    effect1 = TriggeredEffect(event=EntityEvents.SUPPORT)
    effect = BuffEffect(
        target=PostEventParamGetter(
            effect=effect1, parameter=PostEventParameter.SUPPORTED_CARD
        ),
        attack=3,
        keyword=KeywordEnum.OVERWHELM,
        round_only=True,
    )


# Attack: Deal 1 to ALL battling units.
def TarkaztheTribeless():
    effect = PlaySkill(target=Set1Skills.TarkazsFury)
    return Unit(attack_commit_effect=effect)


# Play: Discard your hand. Draw 3. Deal 3 to an enemy.
def AugmentedExperimenter():
    effect = PlaySkill(target=Set1Skills.RecklessResearch)
    return Unit(play_effect=effect)


# Attack: Grant me +4|+0.
def BatteringRam():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=4,
    )
    return Unit(attack_commit_effect=effect)


# Attack: Give other attacking allies +1|+1 and Fearsome this round.
def CithriatheBold():
    effect = BuffEffect(
        target=CardFilter(),
        attack=1,
        health=1,
        round_only=True,
        target_exclusion=AutoEntitySelector.SELF,
    )
    return Unit(attack_commit_effect=effect)


# When I'm targeted and survive, draw 1.
def JaeMedarda():
    # TODO
    effect = DrawEffect()


# When I survive damage, grant me +3|+0.
def ScarmotherVrynna():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=3,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.DAMAGE_SURVIVE,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
    )
    return Unit(summon_effect=effect)


# When I'm summoned, give other allies +2|+2 this round.
def WindfarerHatchling():
    effect = BuffEffect(
        target=CardFilter(),
        exclude_origin=True,
        attack=2,
        health=2,
        round_only=True,
    )
    return Unit(summon_effect=effect)


# Play: Stun 2 enemies.
def YoneWindchaser():
    effect = PlaySkill(target=Set1Skills.StaggeringStrikes)
    return Unit(play_effect=effect)


# When I'm summoned, create 2 Decimates in hand.
def CaptainFarron():
    effect = CreateCardEffect(
        Set1Spells.Decimate,
        quantity=2,
    )
    return Unit(summon_effect=effect)


# Play: Kill the 2 weakest enemies if an ally died this round.
def RhasatheSunderer():
    effect = PlaySkill(target=Set1Skills.NightHarvest)
    return Unit(attack_commit_effect=effect)


# Play: Pick an ally in hand. Summon an exact copy of it. It's Ephemeral.
def SpectralMatron():
    effect = CreateExactCopyEffect(
        target=TargetShorthand.ALLIED_HAND_UNIT,
        is_ephemeral=True,
        location=LocEnum.HOMEBASE,
    )
    return Unit(play_effect=effect)


# When I'm summoned, Rally.
def TiannaCrownguard():
    effect = RallyEffect()
    return Unit(summon_effect=effect)


# When I'm summoned or Attack: Give all allies Barrier this round.
def BrightsteelFormation():
    effect = AddKeywordEffect(
        target=CardFilter(),
        keyword=KeywordEnum.BARRIER,
    )
    return Unit(attack_commit_effect=effect, summon_effect=effect)


# Play: Deal damage to the enemy Nexus equal to half its Health, rounded up.Last Breath: Return me to hand.
def CommanderLedros():
    effect = MoveEffect(target=AutoEntitySelector.SELF, destination=LocEnum.HAND)
    effect1 = PlaySkill(target=Set1Skills.BladeofLedros)
    return Unit(attack_commit_effect=effect1, last_breath_effect=effect)


# Play: Obliterate the top 5 cards of your deck to deal 1 to all enemies and the enemy Nexus for each spell obliterated.
def CorinaVeraza():
    effect = PlaySkill(target=Set1Skills.MagnumOpus)
    return Unit(attack_commit_effect=effect)


# Play: Recall 3 enemies.
def MinahSwiftfoot():
    effect = PlaySkill(target=Set1Skills.SkywardStrikes)
    return Unit(attack_commit_effect=effect)


# Play: Obliterate ALL followers with 4 or less Power in play and in hands.
def SheWhoWanders():
    effect = PlaySkill(target=Set1Skills.Obliterate)
    return Unit(attack_commit_effect=effect)


# Attack: Deal 1 to the enemy Nexus.
def LegionSaboteur():
    effect = PlaySkill(target=Set1Skills.Sabotage)
    return Unit(attack_commit_effect=effect)


# Play: Deal 1 to an ally and grant it +2|+0.
def CrimsonAristocrat():
    target_obj = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = DamageEffect(target=target_obj, value=1)
    effect1 = BuffEffect(target=target_obj, attack=2)
    return Unit(play_effect=[effect, effect1])


#
def Spiderling():
    return Unit()


# When I'm summoned, summon a Spiderling.
def HouseSpider():
    effect = CreateCardEffect(Spiderling, LocEnum.HOMEBASE)
    return Unit(summon_effect=effect)


# Last Breath: Deal 1 to the enemy Nexus.
def LegionGrenadier():
    effect = DamageEffect(
        target=TargetPlayer.OPPONENT,
        value=1,
    )
    return Unit(last_breath_effect=effect)


# Support: Give my supported ally Quick Attack this round.
def LegionDrummer():
    effect = SupportEffect(
        keyword=KeywordEnum.QUICKSTRIKE,
        round_only=True,
    )
    return Unit(support_effect=effect)


# When I'm summoned, grant me +2|+0 if you have another Noxus ally.
def TrifarianHopeful():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=2,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
        condition=Condition(
            target=TargetPlayer.ORIGIN_OWNER,
            condition=PlayerFlags.HAS_X_CARD_IN_PLAY,
            parameter=CardFilter(regions=RegionEnum.NOXUS),
        ),
    )
    return Unit(effects=ta)


# When I survive damage, create a random Crimson unit in your hand.
def CrimsonCurator():
    target_obj = BaseCardFilter(family=SubTypes_.CRIMSON, quantity=1)
    effect = CreateCardEffect(
        target_obj,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.DAMAGE_SURVIVE,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
    )
    return Unit(effects=ta)


# Attack: Grant allied Legion Marauders everywhere +1|+1.
def LegionMarauder():
    effect = BuffEverywhereEffect(
        filter_obj=BaseCardFilter(card_class=LegionMarauder),
        attack=1,
        health=1,
    )
    return Unit(summon_effect=effect)


# When I'm summoned, grant me +1|+1 for each unit you've Stunned or Recalled this game.
def LegionGeneral():
    value = PlayerStatistic.STUNNED_OR_RECALLED
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=value,
        health=value,
    )
    return Unit(summon_effect=effect)


# When I'm summoned, create a copy in hand of an ally that died this game.
def ScribeofSorrows():
    effect = CreateCardEffect(target=AutoEntitySelector.RANDOM_DEAD_ALLY)
    return Unit(summon_effect=effect)


# Play: Kill an ally, then revive it.
def ChroniclerofRuin():
    # TODO shared target
    effect3 = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = KillAction(target=effect3)
    effect1 = ReviveEffect(target=effect3)
    return Unit(play_effect=effect)


# To play me, kill an ally.
def RavenousButcher():
    effect = KillAction(target=TargetShorthand.ALLIED_BOARD_UNIT)
    return Unit(play_requisite=effect)


# Last Breath: Summon a Spiderling.
def HaplessAristocrat():
    effect = CreateCardEffect(
        Spiderling,
        LocEnum.HOMEBASE,
    )
    return Unit(last_breath_effect=effect)


# Play: Grant an ally in hand Ephemeral and reduce its cost by 1.
def ObliviousIslander():
    target_obj = TargetEntity(choices=TargetShorthand.ALLIED_HAND_UNIT)
    effect = BuffCostEffect(target=target_obj, value=1)
    effect1 = AddKeywordEffect(target=target_obj, keyword=KeywordEnum.EPHEMERAL)
    return Unit(play_effect=[effect, effect1])


# Last Breath: Create in hand another random Last Breath follower that costs 3 or less.
def WardensPrey():
    effect = CreateCardEffect(
        target=BaseCardFilter(
            keyword=KeywordEnum.LASTBREATH, cost=(0, 3), type=Types_.SPELL
        ),
    )
    return Unit(last_breath_effect=effect)


# When I'm summoned, grant other allied Mistwraiths everywhere +1|+0.
def Mistwraith():
    effect = BuffEverywhereEffect(
        filter_obj=BaseCardFilter(card_class=Mistwraith),
        attack=1,
    )
    return Unit(summon_effect=effect)


# Support: Grant my supported ally +2|+0 and Ephemeral.
def StirredSpirits():
    effect = SupportEffect(attack=2, keyword=KeywordEnum.EPHEMERAL)
    return Unit(support_effect=effect)


"""
-0---------
"""


# When an ally gets Barrier, grant me +2|+0.
def GreengladeCaretaker():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=2,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.ADD_KEYWORD,
        action=effect,
        ally_enum=OriginEnum.T_ALLY,
        condition=...,
    )
    return Unit(effects=ta)


# When I'm summoned, draw 1.
def ShadowAssassin():
    effect = DrawEffect()
    return Unit(summon_effect=effect)


#
def ScaledSnapper():
    effect = BuffEffect(target=AutoEntitySelector.SELF, attack=3, set_init=True)
    effect1 = BuffEffect(target=AutoEntitySelector.SELF, health=3, set_init=True)
    effect2 = ChoiceAction(choices=[effect, effect1])
    return Unit(play_effect=effect2)


# When I'm summoned, grant all allies in hand +1|+1.
def GreengladeElder():
    effect = BuffEffect(
        target=CardFilter(location=LocEnum.HAND),
        attack=1,
        health=1,
    )
    return Unit(summon_effect=effect)


#
def NavoriBrigand():
    return Unit()


# When I'm summoned, summon a Navori Brigand with my stats.
def NavoriHighwayman():
    effect = CreateCardEffect(
        NavoriBrigand,
        LocEnum.HOMEBASE,
        with_my_stats_source=AutoEntitySelector.SELF,
    )
    return Unit(summon_effect=effect)


# Enlightened: I have +4|+4.
def EmeraldAwakener():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=4,
        health=4,
    )
    StateTriggeredAction(action=effect, condition=PlayerFlags.ENLIGHTENED)
    # TODO once youve
    return Unit(effects=effect)


# To play me, Recall an ally.
def NavoriConspirator():
    effect = RecallEffect(target=TargetShorthand.ALLIED_BOARD_UNIT)
    return Unit(play_requisite=effect)


# Support: Give my supported ally Lifesteal this round.
def HeraldofSpring():
    effect = SupportEffect(
        keyword=KeywordEnum.LIFESTEAL,
        round_only=True,
    )
    return Unit(support_effect=effect)


# When I'm summoned, give other allies +1|+0 this round.
def KeeperofMasks():
    effect1 = BuffEffect(
        target=CardFilter(),
        exclude_origin=True,
        attack=1,
        round_only=True,
    )
    return Unit(strike_effect=effect1)


# Strike: Reduce the cost of the most expensive unit in your hand by 1.
def GreengladeLookout():
    effect = BuffCostEffect(
        target=CardFilter(location=LocEnum.HAND, sorter=CardSorter.EXPENSIVEST),
        value=1,
    )
    return Unit(strike_effect=effect)


# When you summon an ally, give me +1|+1 this round.
def SparringStudent():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=1,
        health=1,
        round_only=True,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
    )
    return Unit(effects=ta)


# When I'm summoned, give me Elusive this round.
def NavoriBladescout():
    effect = AddKeywordEffect(
        target=AutoEntitySelector.SELF,
        keyword=KeywordEnum.ELUSIVE,
        round_only=True,
    )
    return Unit(effects=effect)


# Play: Grant an ally in hand +1|+0.
def InspiringMentor():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_HAND_UNIT,
        attack=1,
    )
    return Unit(play_effect=effect)


# When you summon an Elite, reduce my cost by 1.
def VanguardSquire():
    effect = BuffCostEffect(
        target=AutoEntitySelector.SELF,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        condition=...,
        location=LocEnum.HAND,
    )
    return Unit(effects=ta)


# Attack: Grant me +2|+2.
def VanguardFirstblade():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=2,
        health=2,
    )
    return Unit(attack_commit_effect=effect)


# When I'm summoned, summon an exact copy of me.
def SilverwingVanguard():
    effect = CreateExactCopyEffect(
        target=AutoEntitySelector.SELF, location=LocEnum.HOMEBASE
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.SELF,
        condition=...,
        action=effect,
    )
    return Unit(effects=ta)


# Create a Detain in hand once you've cast a 6+ cost spell this game.
def MageseekerInvestigator():
    effect = CreateCardEffect(
        target=Set1Spells.Detain,
    )
    effect1 = OnceYouve(state=PlayerFlags.HAS_PLAYED_A_6_COST_SPELL, action=effect)
    return Unit(effects=effect1)


# When I'm summoned, draw a unit if an ally died this round.
def VanguardRedeemer():
    effect = DrawEffect(
        condition=PlayerFlags.ALLY_DIED_THIS_ROUND,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
        condition=PlayerFlags.ALLY_DIED_THIS_ROUND,
    )
    return Unit(effects=ta)


# Play: Give an ally Challenger this round.
def LaurentDuelist():
    effect = AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        keyword=KeywordEnum.CHALLENGER,
        round_only=True,
    )
    return Unit(play_effect=effect)


# When I'm summoned, draw a unit with 5+ Power.
def BabblingBjerg():
    effect = DrawEffect(filter_obj=DrawCardFilter(attack=(5, 0)))
    return Unit(summon_effect=effect)


#
def VanguardCavalry():
    return Unit()


# Support: Give my supported ally +1|+1 this round.
def WarChefs():
    effect = SupportEffect(
        attack=1,
        health=1,
        round_only=True,
    )
    return Unit(support_effect=effect)


# Last Breath: Create in hand a random 6+ cost spell from a region other than Demacia.
def MageseekerConservator():
    effect = CreateCardEffect(
        target=BaseCardFilter(
            cost=(6, 0),
            type=Types_.SPELL,
            custom_filter=lambda x, y: y["regions"] != RegionEnum.DEMACIA,
        ),
    )
    return Unit(last_breath_effect=effect)


# When you summon another ally, grant me Challenger.
def FleetfeatherTracker():
    effect = AddKeywordEffect(
        target=AutoEntitySelector.SELF,
        keyword=KeywordEnum.CHALLENGER,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_ALLY,
        activate_once=True,
    )
    return Unit(effects=ta)


# Play: For the top 6 cards in your deck, summon each Elnuk and shuffle the rest into your deck.
def TroopofElnuks():
    effect = DrawSpecificReturnRestEffect(
        top_x_cards=6,
        filter_obj=DrawCardFilter(subtype=SubTypes_.ELNUK),
        location=LocEnum.HOMEBASE,
    )
    return Unit(effects=effect)


# Round Start: Get an extra mana gem this round.
def WyrdingStones():
    effect = GainManaGemEffect(
        gain_mana=True,
        round_only=True,
    )
    return Unit(round_start_effects=effect)


# When I survive damage, grant me +3|+0.
def ScarthaneSteffen():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=3,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.DAMAGE_SURVIVE,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
    )
    return Unit(effects=ta)


# Play: Heal an ally or your Nexus 3.
def KindlyTavernkeeper():
    effect = HealEffect(
        target=TargetShorthand.ALLY_NEXUS_OR_BOARD_UNITS,
        value=3,
    )
    return Unit(play_effect=effect)


#
def EnragedYeti():
    return Unit()


# When I'm summoned, create an Enraged Yeti in the top 3 cards of your deck.
def AvarosanTrapper():
    effect = CreateCardEffect(
        EnragedYeti,
        location=LocEnum.DECK,
        index=...,
    )
    return Unit(summon_effect=effect)


# Play: Deal 1 to an enemy.
def AvarosanMarksman():
    effect = PlaySkill(Set1Skills.Bullseye)
    return Unit(play_effect=effect)


#
def SnowHare():
    return Unit


# When I'm summoned, the enemy summons a Snow Hare.
def StalkingWolf():
    effect = CreateCardEffect(
        SnowHare,
        LocEnum.HOMEBASE,
        owner=TargetPlayer.OPPONENT,
    )
    return Unit(summon_effect=effect)


# Play: Frostbite an enemy.
def IcevaleArcher():
    effect = FrostbiteEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT,
    )
    return Unit(play_effect=effect)


# Enlightened: I have +4|+4.
def FeralMystic():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=4,
        health=4,
    )
    effect1 = OnceYouve()
    # TODO once youve
    return Unit()


# Last Breath: Draw 1.
def AvarosanSentry():
    effect = DrawEffect()
    return Unit(last_breath_effect=effect)


# When I survive damage, grant me +3|+0.
def UnscarredReaver():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=3,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.DAMAGE_SURVIVE,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
    )
    return Unit(effects=ta)


# Last Breath: Create 2 Enraged Yetis in your deck.
def YetiYearling():
    effect = CreateCardEffect(
        EnragedYeti,
        LocEnum.DECK,
        quantity=2,
    )
    return Unit(last_breath_effect=effect)


# When I'm summoned, grant the top 2 allies in your deck +1|+1.
def OmenHawk():
    effect = BuffEffect(
        target=CardFilter(location=LocEnum.DECK, quantity=2),
        attack=1,
        health=1,
    )
    return Unit(summon_effect=effect)


# When I'm summoned, create another random 1 cost Poro in hand.
def LonelyPoro():
    effect = CreateCardEffect(
        target=BaseCardFilter(subtype=SubTypes_.PORO, cost=1),
    )
    return Unit(summon_effect=effect)


# When I'm summoned, create another random 1 cost Poro in hand.
def JubilantPoro():
    effect = CreateCardEffect(
        target=BaseCardFilter(subtype=SubTypes_.PORO, cost=1),
    )
    return Unit(summon_effect=effect)


# When I'm summoned, refill 2 spell mana.
def EagerApprentice():
    effect = RefillSpellMana(value=2)
    return Unit(summon_effect=effect)


# Last Breath: Deal 1 to EACH Nexus.
def CausticCask():
    effect = DamageEffect(
        target=TargetPlayer.ALL_PLAYERS,
        value=1,
    )
    return Unit(last_breath_effect=effect)


#
def AcademyProdigy():
    return Unit


# When you draw a card, give me +1|+0 this round.
def AstuteAcademic():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=1,
        round_only=True,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.DRAW, action=effect, ally_enum=OriginEnum.T_ALLY
    )
    return Unit(effects=ta)


# Play: Discard a card to draw 1.
def ZauniteUrchin():
    effect = DiscardEffect(target=TargetShorthand.ALLIED_HAND_CARD)
    effect1 = DrawEffect(fizz_if_fail=effect)
    return Unit(play_effect=[effect, effect1])


# Attack: Deal 2 to the enemy Nexus.
def BoomcrewRookie():
    effect = PlaySkill(target=Set1Skills.Undermine)
    return Unit(attack_commit_effect=effect)


# When I'm summoned, create a Mushroom Cloud in hand.
def ClumpofWhumps():
    effect = CreateCardEffect(
        Set1Spells.MushroomCloud,
    )
    return Unit(summon_effect=effect)


# When I'm discarded, summon me.
def FlameChompers():
    effect1 = SummonEffect(target=AutoEntitySelector.SELF)
    ta = ActionReplacement(
        event_filter=EntityEvents.DISCARD,
        replacement_action=effect1,
        ally_enum=OriginEnum.T_SELF,
    )
    return Unit(effects=ta)


# Support: Create 4 copies of the supported ally in your deck.
def ParadeElectrorig():
    effect = CreateCardEffect(
        PostEventParam.TARGET,
        LocEnum.DECK,
        quantity=4,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUPPORT,
        action=effect,
        ally_enum=OriginEnum.SUPPORTER_SELF,
    )
    return Unit(effects=ta)


# When you cast a spell, plant 3 Poison Puffcaps on random cards in the enemy deck.
def PuffcapPeddler():
    effect = PlantPuffcaps(quantity=3)
    ta = TriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL, action=effect, ally_enum=OriginEnum.T_ALLY
    )
    return Unit(effects=ta)


# Play: Discard a card to draw 1.
def SumpDredger():
    effect = DiscardEffect(target=TargetShorthand.ALLIED_HAND_CARD)
    effect1 = DrawEffect(fizz_if_fail=effect)
    return Unit(play_effect=[effect, effect1])


# When I'm summoned, summon 2 Caustic Casks.
def UsedCaskSalesman():
    effect = CreateCardEffect(
        CausticCask,
        LocEnum.HOMEBASE,
        quantity=2,
    )
    return Unit(summon_effect=effect)


def BackAlleyBarkeepEffect():
    target_obj = BaseCardFilter(type=None, quantity=PlayerStatistic.BARKEEP_SUMMONED)
    effect = CreateCardEffect(target_obj)
    return


# When I'm summoned, create in hand a random card for each Back Alley Barkeep
# you've summoned this game.
def BackAlleyBarkeep():
    return Unit(summon_effect=BackAlleyBarkeepEffect)


#
def EscapedAbomination():
    return Unit


# Last Breath: Summon an Escaped Abomination.
def CursedKeeper():
    effect = CreateCardEffect(
        EscapedAbomination,
        location=LocEnum.HOMEBASE,
    )
    return Unit(last_breath_effect=effect)


# When you summon an Ephemeral ally, grant it +1|+1.
def SoulShepherd():
    effect = BuffEffect(
        target=PostEventParam.TARGET,
        attack=1,
        health=1,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        condition=PostEventTargetCondition(
            condition=CardFlags.HAS_KEYWORD, parameter=KeywordEnum.EPHEMERAL
        ),
    )
    return Unit(effects=ta)


"""
------------------
NORMAL CARDS
"""


#
def AffectionatePoro():
    return Unit


#
def CithriaofCloudfield():
    return Unit


#
def DaringPoro():
    return Unit


#
def LegionRearguard():
    return Unit


#
def NimblePoro():
    return Unit


#
def PluckyPoro():
    return Unit


#
def PreciousPet():
    return Unit


#
def SinisterPoro():
    return Unit


#
def AcademyProdigy():
    return Unit()


#
def ArachnoidHorror():
    return Unit


#
def ScrapScuttler():
    return Unit


#
def TrifarianGloryseeker():
    return Unit


#
def VanguardDefender():
    return Unit


#
def VanguardLookout():
    return Unit


#
def SpectralRider():
    return Unit


#
def RecklessTrifarian():
    return Unit


#
def LaurentProtege():
    return Unit


#
def DauntlessVanguard():
    return Unit()


#
def GoldenCrushbot():
    return Unit


#
def AmateurAeronaut():
    return Unit


#
def MightyPoro():
    return Unit


#
def DarkwaterScourge():
    return Unit


#
def KinkouLifeblade():
    return Unit


#
def SilverwingDiver():
    return Unit


#
def BullElnuk():
    return Unit


#
def Yusari():
    return Unit


#
def TrifarianShieldbreaker():
    return Unit()


#
def ScarmaidenReaver():
    return Unit()


#
def AlphaWildclaw():
    return Unit()


#
def LivingShadow():
    return Unit()


#
def Soulgorger():
    return Unit()


#
def SavageReckoner():
    return Unit()


#
def TheEmpyrean():
    return Unit


#
def THex():
    return Unit()


#
def Mk0WindupShredder():
    return Unit()


#
def Mk1Wrenchbot():
    return Unit()


#
def Mk2EvolutionTurret():
    return Unit()


#
def Mk6FloorBGone():
    return Unit()


#
def Mk3ApexTurret():
    return Unit()


#
def Mk5RocketBlaster():
    return Unit()


#
def Mk4Stormlobber():
    return Unit()


#
def Mk7ArmoredStomper():
    return Unit()


#
def Catastrophe():
    return Unit()


#
def Vilemaw():
    return Unit()


#
def UnleashedSpirit():
    return Unit()


#
def IllegalContraption():
    return Unit()


crimsons = [
    CrimsonAristocrat,
    CrimsonAwakener,
    CrimsonCurator,
    CrimsonDisciple,
]


turrets = [
    Mk0WindupShredder,
    Mk1Wrenchbot,
    Mk2EvolutionTurret,
    Mk3ApexTurret,
    Mk4Stormlobber,
    Mk5RocketBlaster,
    Mk6FloorBGone,
    Mk7ArmoredStomper,
    THex,
]
