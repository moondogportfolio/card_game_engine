from attr import define
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
from card_classes.cardarchetype import CardArchetype
from card_classes.unit import Unit
from classes.gamestate import GameState
from conditions.base_condition import Condition
from entity_selectors.base_card_filter import BaseCardFilter, InvokeBaseCardFilter
from entity_selectors.card_filter import (
    CardFilter,
    CardFilterSelector,
    DrawCardFilter,
    SimpleCardFilter,
    StackSpellFilter,
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
    async def effect(origin: CardArchetype, gamestate: GameState, *args, **kwargs):
        await BuffEffect(
            target=SimpleCardFilter(exclude_origin=True),
            attack=1,
            round_only=True,
        )
    return Unit(attack_commit_effect=effect)


# Round Start: Discard your lowest cost card to draw 1.
def ArenaBookie():
    async def effect(origin: CardArchetype, gamestate: GameState, *args, **kwargs):
        await DiscardEffect(
            target=CardFilterSelector(
                location=LocEnum.HAND,
                sorter=CardSorter.CHEAPEST,
            )
        )
        return effect

    effect1 = DrawEffect(fizz_if_fail=effect)
    return Unit(round_start_effects=(effect, effect1))


@define
class SummonEvent:
    TARGET: CardArchetype


# When you summon an Elite, grant it +1|+1.
def Battlesmith():
    def effect(postevent: SummonEvent, *args, **kwargs):
        BuffEffect(
            target=postevent.TARGET,
            attack=1,
            health=1,
        )

    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        action=effect,
        condition=Condition(
            target=PostEventParam.TARGET,
            condition=CardFlags.IS_SUBTYPE_X,
            parameter=SubTypes_.ELITE,
        ),
    )
    return Unit(effects=ta)


# Nexus Strike: Create in hand an exact copy of a random spell from the enemy's deck.
def ChempunkPickpocket():
    def effect(origin: CardArchetype, gamestate: GameState, *args, **kwargs):
        target_obj = CardFilter(
            owner=TargetPlayer.OPPONENT,
            location=LocEnum.DECK,
            type=Types_.SPELL,
        ).resolve(gamestate, origin)
        CreateExactCopyEffect(target=target_obj)
        return effect
    return Unit(nexus_strike_effect=effect)


# When I survive damage, deal 1 to the enemy Nexus.
def CrimsonDisciple():
    def effect(origin: CardArchetype, gamestate: GameState, *args, **kwargs):
        DamageEffect(
            target=origin.opponent,
            value=1,
        )
        return effect
    return Unit(damage_survive_effect=effect)


# When you Stun or Recall a unit, grant me +2|+0.
def FaeBladetwirler():
    def effect(origin: CardArchetype, gamestate: GameState, *args, **kwargs):
        BuffEffect(
            target=origin,
            attack=2,
        )
        return effect
    ta = TriggeredAction(
        event_filter=(EntityEvents.STUN, EntityEvents.RECALL),
        action=effect,
        ally_enum=OriginEnum.O_ALLY,
    )
    return Unit(effects=ta)


# When you summon an ally, give me +1|+0 this round.
def GreengladeDuo():
    def effect(origin: CardArchetype, gamestate: GameState, *args, **kwargs):
        BuffEffect(target=origin, attack=1, round_only=True)
        return effect
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
    )
    return Unit(effects=effect)


# Support: Give my supported ally Elusive this round.
def IntrepidMariner():
    SupportEffect(
        keyword=KeywordEnum.ELUSIVE,
        round_only=True,
    )
    return Unit(support_effect=effect)


# Grant me +1|+1 and Challenger once you've cast a 6+ cost spell this game.
def MageseekerPersuader():
    def effect(origin: CardArchetype, gamestate: GameState, *args, **kwargs):
        BuffEffect(
            target=origin,
            attack=1,
            health=1,
            keyword=KeywordEnum.CHALLENGER,
        )
        return effect
    ta = TriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL,
        action=effect,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        condition=...,
    )
    #TODO once youve
    return Unit(effects=effect)


# When I'm summoned, draw a Poro if you Behold a Poro.
def PoroHerder():
    def effect(origin: CardArchetype, gamestate: GameState, *args, **kwargs):
        DrawEffect(
            quantity=1,
            filter_obj=DrawCardFilter(subtype=SubTypes_.PORO).resolve(gamestate, origin),
        )
        return effect
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
    def effect(origin: CardArchetype, gamestate: GameState, *args, **kwargs):
        ReviveEffect(
            target=origin,
            location=LocEnum.BATTLEFIELD,
        )
        
        return effect
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
    BuffEffect(
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
    BuffEffect(
        target=origin,
        attack=1,
        health=1,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL, action=effect, ally_enum=OriginEnum.T_ALLY
    )
    return Unit(effects=effect)


# When I'm summoned, give other Spider allies +1|+0 and enemies -1|-0 this round.
def FrenziedSkitterer():
    BuffEffect(
        target=CardFilter(owner=TargetPlayer.OPPONENT),
        attack=-1,
        round_only=True,
    )

    effect1 = BuffEffect(
        target=CardFilter(subtype=SubTypes_.SPIDER),
        target_exclusion=origin,
        attack=1,
        round_only=True,
    )
    return Unit(summon_effect=[effect, effect1])


# Attack: Grant me +1|+0 for each Ephemeral ally you have.
def IronHarbinger():
    effect1 = BuffEffect(
        target=origin,
        attack=CardFilter(
            keyword=KeywordEnum.EPHEMERAL,
            output_count=True,
        ),
    )
    return Unit(attack_commit_effect=effect1)


# When another ally dies, deal 1 to the enemy Nexus.
def PhantomPrankster():
    DamageEffect(target=TargetPlayer.OPPONENT, value=1)
    ta = TriggeredAction(
        event_filter=EntityEvents.DIE, action=effect, ally_enum=OriginEnum.T_ALLY
    )
    return Unit(effects=ta)


# Strike: If I struck a unit with 0 Power, kill it.
def RimefangWolf():
    # `TODO
    KillAction(target=PostEventParam.TARGET)
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
    MoveEffect(target=target_obj, index=0)
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        condition=condition,
        ally_enum=OriginEnum.T_SELF,
    )
    return Unit(summon_effect=effect)


# Strike: Draw a spell.
def Rivershaper():
    DrawEffect(filter_obj=DrawCardFilter(type=Types_.SPELL))
    return Unit(strike_effect=effect)


# The first time an allied Lucian dies, grant me +1|+1 and Double Attack.
def SennaSentinelofLight():
    effect1 = BuffEffect(
        target=origin,
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
    RecallEffect(
        target=CardFilter(),
        target_exclusion=origin,
    )
    return Unit(summon_effect=effect)


# When I'm summoned, create a For Demacia! in hand.
def VanguardSergeant():
    CreateCardEffect(Set1Spells.ForDemacia)
    return Unit(summon_effect=effect)


# To play me, kill 2 allies.
def AncientCrocolith():
    KillAction(target=TargetEntity(quantity=2, minimum=2))
    return Unit(play_requisite=effect)


# Allegiance: Grant the top ally in your deck +3|+3 and Overwhelm.
def AvarosanOutriders():
    BuffEffect(
        target=AutoEntitySelector.TOP_ALLY_IN_DECK,
        attack=3,
        health=3,
        keyword=KeywordEnum.OVERWHELM,
    )
    return Unit(summon_allegiance_effect=effect)


# Allegiance: Grant me +1|+1 and Overwhelm.
def BasiliskRider():
    BuffEffect(
        target=origin,
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
    CreateCardEffect(
        quantity=2,
        target=Set1Spells.MushroomCloud,
    )
    return Unit(summon_effect=effect)


def CrowdFavoriteEffect(origin):
    value = CardFilter(exclude_origin=True)
    BuffEffect(
        target=origin,
        attack=value,
        health=value,
    )
    return effect


# When I'm summoned, grant me +1|+1 for each other ally you have.
def CrowdFavorite():
    return Unit(summon_effect=CrowdFavoriteEffect)


# Last Breath: Create in hand a random Epic card from your regions.
def EminentBenefactor():
    CreateCardEffect(
        target=BaseCardFilter(
            type=None, rarity=CardRarity.EPIC, owner_same_regions=True
        ),
    )
    return Unit(last_breath_effect=effect)


# When I'm summoned, deal 1 to all other allies.
def CrimsonAwakener():
    DamageEffect(
        target=CardFilter(),
        target_exclusion=origin,
        value=1,
    )
    return Unit(summon_effect=effect)


# All of your spells and skills deal 1 extra damage.
def Funsmith():
    ActionModifier(
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
    SummonEffect(
        target=CardFilter(location=LocEnum.DECK, cost=1),
    )
    return Unit(summon_allegiance_effect=effect)


# Play: Grant an ally +2|+2.
def LaurentBladekeeper():
    BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=2,
        health=2,
    )
    return Unit(play_effect=effect)


# When you summon a 1 cost ally, grant it +2|+2.
def ProfessorvonYipp():
    BuffEffect(
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
    BuffEffect(
        target=origin,
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
    CreateCardEffect(Set1Spells.SumpworksMap, coevent=effect1)
    effect1 = BuffCostEffect(
        target=PostEventParam.TARGET,
        value=0,
        operator=Ops_.SET,
        round_only=True,
    )
    return Unit(summon_allegiance_effect=(effect, effect1))


# Allegiance: Grant other allies +1|+1.
def VanguardBannerman():
    BuffEffect(
        target=CardFilter(),
        target_exclusion=origin,
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
    CreateCardEffect(
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
    BuffEffect(
        target=CardFilter(subtype=SubTypes_.SPIDER),
        target_exclusion=origin,
        attack=2,
    )
    return Unit(summon_effect=effect)


# Play: Deal 1 to all enemies.
def ChempunkShredder():
    play = PlaySkill(target=Set1Skills.FaceMelter)
    return Unit(play_effect=play)


# Play: Kill an ally to summon a random follower that costs 2 more.
def EtherealRemitter():
    CreateCardEffect(
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
    AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        keyword=KeywordEnum.BARRIER,
    )
    return Unit(play_effect=effect)


# Play: Grant an ally in hand +3|+3.
def JeweledProtector():
    BuffEffect(
        target=TargetShorthand.ALLIED_HAND_UNIT,
        attack=3,
        health=3,
    )
    return Unit(play_effect=effect)


# Nexus Strike: Summon an exact copy of me.
def MidenstokkeHenchmen():
    CreateExactCopyEffect(
        target=origin,
        location=LocEnum.HOMEBASE,
    )
    return Unit(nexus_strike_effect=effect)


# When I'm summoned, grant me Lifesteal and Tough if an ally died this round.
def RadiantGuardian():
    AddKeywordEffect(
        target=origin,
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
    FrostbiteEffect(
        target=AutoEntitySelector.STRONGEST_OPPONENT_BOARD_UNIT,
    )
    ta = TriggeredAction(event_filter=GameStateEnums.ROUND_START, action=effect)
    return Unit(effects=ta)


# Last Breath: Create a random Elite in hand.
def SwiftwingLancer():
    CreateCardEffect(
        target=BaseCardFilter(subtype=SubTypes_.ELITE, quantity=1),
    )
    return Unit(last_breath_effect=effect)


# When an ally dies, refill your spell mana.
def TorturedProdigy():
    RefillSpellMana(
        value=Ops_.MAX,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.DIE, action=effect, ally_enum=OriginEnum.T_ALLY
    )
    return Unit(effects=ta)


# When I'm summoned, draw 1 for each 5+ Power ally you have.
def TrifarianAssessor():
    DrawEffect(
        quantity=CardFilter(
            attack=(5, 0),
            output_count=True,
        ),
    )
    return Unit(summon_effect=effect)


# Grant me +4|+0 and Quick Attack once you've cast a 6+ cost spell this game.
def UnstableVoltician():
    BuffEffect(
        target=origin,
        attack=4,
        keyword=KeywordEnum.QUICKSTRIKE,
    )


# Your Burst and Focus spells cost 1 less.
def CloudDrinker():
    DynamicCostModifier(
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
    HeartoftheFluftEffect()
    return Unit(play_effect=effect)


# Last Breath: Summon a Heart of the Fluft.
def FluftofPoros():
    CreateCardEffect(HeartoftheFluft, LocEnum.HOMEBASE)
    return Unit(last_breath_effect=effect)


# Round Start: Stun the weakest enemy.
def MinotaurReckoner():
    StunEffect(
        target=AutoEntitySelector.WEAKEST_OPPONENT_UNIT,
    )
    ta = TriggeredAction(event_filter=GameStateEnums.ROUND_START, action=effect)
    return Unit(effects=ta)


# Play: Create an exact copy of a card in hand other than Zephyr Sage.
def ZephyrSage():
    CreateCardEffect(
        target=CardFilter(
            type=None, exclude_card_class=ZephyrSage, location=LocEnum.HAND
        ),
        exact_copy=True,
    )
    return Unit(play_effect=effect)


# Round End: Reduce my cost by 1.
def AncientYeti():
    BuffCostEffect(
        target=origin,
        value=1,
    )
    ta = TriggeredAction(
        event_filter=GameStateEnums.ROUND_END, action=effect, location=LocEnum.HAND
    )
    return Unit(round_end_effects=effect)


# When I'm summoned, Frostbite enemies with 3 or less Health.
def IcyYeti():
    FrostbiteEffect(
        target=CardFilter(owner=TargetPlayer.OPPONENT, health=(0, 3)),
    )
    return Unit(summon_effect=effect)


# When I'm summoned, revive the strongest dead allied champion.
def TheRekindler():
    ReviveEffect(
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
        target=origin,
        attack=PlayerStatistic.ALLY_DIED_THIS_GAME,
        health=PlayerStatistic.ALLY_DIED_THIS_GAME,
    )
    return Unit(summon_effect=effect1)


# Reduce my cost by 1 for each spell you've cast this game.
def PlazaGuardian():
    DynamicCostModifier(value=PlayerStatistic.ALLY_DIED_THIS_GAME)
    return Unit(effects=effect)


# Reduce my cost by 1 for each ally that died this game.
def Scuttlegeist():
    DynamicCostModifier(value=PlayerStatistic.ALLY_DIED_THIS_GAME)
    return Unit(effects=effect)


# Nexus Strike: Create a copy of me in hand.
def SilentShadowseer():
    CreateCardEffect(SilentShadowseer)
    return Unit(nexus_strike_effect=effect)


# Round End: Grant other allies +1|+1 if an ally died this round.
def Dawnspeakers():
    BuffEffect(
        target=CardFilter(),
        target_exclusion=origin,
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
    ReviveEffect(target=origin)
    effect1 = BuffEffect(target=origin, attack=1, health=1)
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
    CreateCardEffect(
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
    CreateCardEffect(ShadowFiend)
    return Unit(strike_effect=effect)


# I deal double damage to the Nexus.
def ShirazatheBlade():
    ActionModifier(
        event=EntityEvents.DAMAGE,
        parameter=...,
        operator=Ops_.MULTIPLY,
        value=2,
        condition=...,
    )
    return Unit(effects=effect)


# When I'm summoned, grant all allies in your deck +1|+1.
def AvarosanHearthguard():
    BuffEffect(
        target=CardFilter(location=LocEnum.DECK),
        attack=1,
        health=1,
    )
    return Unit(summon_effect=effect)


# Support: Give my supported ally +3|+0 and Overwhelm this round.
def KatoTheArm():
    effect1 = TriggeredEffect(event=EntityEvents.SUPPORT)
    BuffEffect(
        target=PostEventParamGetter(
            effect=effect1, parameter=PostEventParameter.SUPPORTED_CARD
        ),
        attack=3,
        keyword=KeywordEnum.OVERWHELM,
        round_only=True,
    )


# Attack: Deal 1 to ALL battling units.
def TarkaztheTribeless():
    PlaySkill(target=Set1Skills.TarkazsFury)
    return Unit(attack_commit_effect=effect)


# Play: Discard your hand. Draw 3. Deal 3 to an enemy.
def AugmentedExperimenter():
    PlaySkill(target=Set1Skills.RecklessResearch)
    return Unit(play_effect=effect)


# Attack: Grant me +4|+0.
def BatteringRam():
    BuffEffect(
        target=origin,
        attack=4,
    )
    return Unit(attack_commit_effect=effect)


# Attack: Give other attacking allies +1|+1 and Fearsome this round.
def CithriatheBold():
    BuffEffect(
        target=CardFilter(),
        attack=1,
        health=1,
        round_only=True,
        target_exclusion=origin,
    )
    return Unit(attack_commit_effect=effect)


# When I'm targeted and survive, draw 1.
def JaeMedarda():
    # TODO
    DrawEffect()


# When I survive damage, grant me +3|+0.
def ScarmotherVrynna():
    BuffEffect(
        target=origin,
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
    BuffEffect(
        target=CardFilter(),
        exclude_origin=True,
        attack=2,
        health=2,
        round_only=True,
    )
    return Unit(summon_effect=effect)


# Play: Stun 2 enemies.
def YoneWindchaser():
    PlaySkill(target=Set1Skills.StaggeringStrikes)
    return Unit(play_effect=effect)


# When I'm summoned, create 2 Decimates in hand.
def CaptainFarron():
    CreateCardEffect(
        Set1Spells.Decimate,
        quantity=2,
    )
    return Unit(summon_effect=effect)


# Play: Kill the 2 weakest enemies if an ally died this round.
def RhasatheSunderer():
    PlaySkill(target=Set1Skills.NightHarvest)
    return Unit(attack_commit_effect=effect)


# Play: Pick an ally in hand. Summon an exact copy of it. It's Ephemeral.
def SpectralMatron():
    CreateExactCopyEffect(
        target=TargetShorthand.ALLIED_HAND_UNIT,
        is_ephemeral=True,
        location=LocEnum.HOMEBASE,
    )
    return Unit(play_effect=effect)


# When I'm summoned, Rally.
def TiannaCrownguard():
    RallyEffect()
    return Unit(summon_effect=effect)


# When I'm summoned or Attack: Give all allies Barrier this round.
def BrightsteelFormation():
    AddKeywordEffect(
        target=CardFilter(),
        keyword=KeywordEnum.BARRIER,
    )
    return Unit(attack_commit_effect=effect, summon_effect=effect)


# Play: Deal damage to the enemy Nexus equal to half its Health, rounded up.Last Breath: Return me to hand.
def CommanderLedros():
    MoveEffect(target=origin, destination=LocEnum.HAND)
    effect1 = PlaySkill(target=Set1Skills.BladeofLedros)
    return Unit(attack_commit_effect=effect1, last_breath_effect=effect)


# Play: Obliterate the top 5 cards of your deck to deal 1 to all enemies and the enemy Nexus for each spell obliterated.
def CorinaVeraza():
    PlaySkill(target=Set1Skills.MagnumOpus)
    return Unit(attack_commit_effect=effect)


# Play: Recall 3 enemies.
def MinahSwiftfoot():
    PlaySkill(target=Set1Skills.SkywardStrikes)
    return Unit(attack_commit_effect=effect)


# Play: Obliterate ALL followers with 4 or less Power in play and in hands.
def SheWhoWanders():
    PlaySkill(target=Set1Skills.Obliterate)
    return Unit(attack_commit_effect=effect)


# Attack: Deal 1 to the enemy Nexus.
def LegionSaboteur():
    PlaySkill(target=Set1Skills.Sabotage)
    return Unit(attack_commit_effect=effect)


# Play: Deal 1 to an ally and grant it +2|+0.
def CrimsonAristocrat():
    target_obj = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    DamageEffect(target=target_obj, value=1)
    effect1 = BuffEffect(target=target_obj, attack=2)
    return Unit(play_effect=[effect, effect1])


#
def Spiderling():
    return Unit()


# When I'm summoned, summon a Spiderling.
def HouseSpider():
    CreateCardEffect(Spiderling, LocEnum.HOMEBASE)
    return Unit(summon_effect=effect)


# Last Breath: Deal 1 to the enemy Nexus.
def LegionGrenadier():
    DamageEffect(
        target=TargetPlayer.OPPONENT,
        value=1,
    )
    return Unit(last_breath_effect=effect)


# Support: Give my supported ally Quick Attack this round.
def LegionDrummer():
    effect1 = TriggeredEffect(event=EntityEvents.SUPPORT)
    AddKeywordEffect(
        target=PostEventParamGetter(
            effect=effect1, parameter=PostEventParameter.SUPPORTED_CARD
        ),
        keyword=KeywordEnum.QUICKSTRIKE,
        round_only=True,
    )


# When I'm summoned, grant me +2|+0 if you have another Noxus ally.
def TrifarianHopeful():
    BuffEffect(
        target=origin,
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
    CreateCardEffect(
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
    BuffEverywhereEffect(
        filter_obj=BaseCardFilter(card_class=LegionMarauder),
        attack=1,
        health=1,
    )
    return Unit(summon_effect=effect)


# When I'm summoned, grant me +1|+1 for each unit you've Stunned or Recalled this game.
def LegionGeneral():
    value = PlayerStatistic.STUNNED_OR_RECALLED
    BuffEffect(
        target=origin,
        attack=value,
        health=value,
    )
    return Unit(summon_effect=effect)


# When I'm summoned, create a copy in hand of an ally that died this game.
def ScribeofSorrows():
    CreateCardEffect(target=AutoEntitySelector.RANDOM_DEAD_ALLY)
    return Unit(summon_effect=effect)


# Play: Kill an ally, then revive it.
def ChroniclerofRuin():
    # TODO shared target
    effect3 = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    KillAction(target=effect3)
    effect1 = ReviveEffect(target=effect3)
    return Unit(play_effect=effect)


# To play me, kill an ally.
def RavenousButcher():
    KillAction(target=TargetShorthand.ALLIED_BOARD_UNIT)
    return Unit(play_requisite=effect)


# Last Breath: Summon a Spiderling.
def HaplessAristocrat():
    CreateCardEffect(
        Spiderling,
        LocEnum.HOMEBASE,
    )
    return Unit(last_breath_effect=effect)


# Play: Grant an ally in hand Ephemeral and reduce its cost by 1.
def ObliviousIslander():
    target_obj = TargetEntity(choices=TargetShorthand.ALLIED_HAND_UNIT)
    BuffCostEffect(target=target_obj, value=1)
    effect1 = AddKeywordEffect(target=target_obj, keyword=KeywordEnum.EPHEMERAL)
    return Unit(play_effect=[effect, effect1])


# Last Breath: Create in hand another random Last Breath follower that costs 3 or less.
def WardensPrey():
    CreateCardEffect(
        target=BaseCardFilter(
            keyword=KeywordEnum.LASTBREATH, cost=(0, 3), type=Types_.SPELL
        ),
    )
    return Unit(last_breath_effect=effect)


# When I'm summoned, grant other allied Mistwraiths everywhere +1|+0.
def Mistwraith():
    BuffEverywhereEffect(
        filter_obj=BaseCardFilter(card_class=Mistwraith),
        attack=1,
    )
    return Unit(summon_effect=effect)


# Support: Grant my supported ally +2|+0 and Ephemeral.
def StirredSpirits():
    SupportEffect(attack=2, keyword=KeywordEnum.EPHEMERAL)
    return Unit(support_effect=effect)


"""
-0---------
"""


# When an ally gets Barrier, grant me +2|+0.
def GreengladeCaretaker():
    BuffEffect(
        target=origin,
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
    DrawEffect()
    return Unit(summon_effect=effect)


#
def ScaledSnapper():
    BuffEffect(target=origin, attack=3, set_init=True)
    effect1 = BuffEffect(target=origin, health=3, set_init=True)
    effect2 = ChoiceAction(choices=[effect, effect1])
    return Unit(play_effect=effect2)


# When I'm summoned, grant all allies in hand +1|+1.
def GreengladeElder():
    BuffEffect(
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
    CreateCardEffect(
        NavoriBrigand,
        LocEnum.HOMEBASE,
        with_my_stats_source=origin,
    )
    return Unit(summon_effect=effect)


# Enlightened: I have +4|+4.
def EmeraldAwakener():
    BuffEffect(
        target=origin,
        attack=4,
        health=4,
    )
    StateTriggeredAction(action=effect, condition=PlayerFlags.ENLIGHTENED)
    # TODO
    return Unit(effects=effect)


# To play me, Recall an ally.
def NavoriConspirator():
    RecallEffect(target=TargetShorthand.ALLIED_BOARD_UNIT)
    return Unit(play_requisite=effect)


# Support: Give my supported ally Lifesteal this round.
def HeraldofSpring():
    SupportEffect(
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
    BuffCostEffect(
        target=CardFilter(location=LocEnum.HAND, sorter=CardSorter.EXPENSIVEST),
        value=1,
    )
    return Unit(strike_effect=effect)


# When you summon an ally, give me +1|+1 this round.
def SparringStudent():
    BuffEffect(
        target=origin,
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
    AddKeywordEffect(
        target=origin,
        keyword=KeywordEnum.ELUSIVE,
        round_only=True,
    )
    return Unit(effects=effect)


# Play: Grant an ally in hand +1|+0.
def InspiringMentor():
    BuffEffect(
        target=TargetShorthand.ALLIED_HAND_UNIT,
        attack=1,
    )
    return Unit(play_effect=effect)


# When you summon an Elite, reduce my cost by 1.
def VanguardSquire():
    BuffCostEffect(
        target=origin,
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
    BuffEffect(
        target=origin,
        attack=2,
        health=2,
    )
    return Unit(attack_commit_effect=effect)


# When I'm summoned, summon an exact copy of me.
def SilverwingVanguard():
    CreateExactCopyEffect(
        target=origin, location=LocEnum.HOMEBASE
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
    CreateCardEffect(
        target=Set1Spells.Detain,
    )
    effect1 = OnceYouve(state=PlayerFlags.HAS_PLAYED_A_6_COST_SPELL, action=effect)
    return Unit(effects=effect1)


# When I'm summoned, draw a unit if an ally died this round.
def VanguardRedeemer():
    DrawEffect(
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
    AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        keyword=KeywordEnum.CHALLENGER,
        round_only=True,
    )
    return Unit(play_effect=effect)


# When I'm summoned, draw a unit with 5+ Power.
def BabblingBjerg():
    DrawEffect(target=DrawCardFilter(attack=(5, 0)))
    return Unit(summon_effect=effect)


#
def VanguardCavalry():
    return Unit()


# Support: Give my supported ally +1|+1 this round.
def WarChefs():
    SupportEffect(
        attack=1,
        health=1,
        round_only=True,
    )
    return Unit(support_effect=effect)


# Last Breath: Create in hand a random 6+ cost spell from a region other than Demacia.
def MageseekerConservator():
    CreateCardEffect(
        target=BaseCardFilter(
            cost=(6, 0),
            type=Types_.SPELL,
            custom_filter=lambda x, y: y["regions"] != RegionEnum.DEMACIA,
        ),
    )
    return Unit(last_breath_effect=effect)


# When you summon another ally, grant me Challenger.
def FleetfeatherTracker():
    AddKeywordEffect(
        target=origin,
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
    DrawSpecificReturnRestEffect(
        top_x_cards=6,
        filter_obj=DrawCardFilter(subtype=SubTypes_.ELNUK),
        location=LocEnum.HOMEBASE,
    )
    return Unit(effects=effect)


# Round Start: Get an extra mana gem this round.
def WyrdingStones():
    GainManaGemEffect(
        gain_mana=True,
        round_only=True,
    )
    return Unit(round_start_effects=effect)


# When I survive damage, grant me +3|+0.
def ScarthaneSteffen():
    BuffEffect(
        target=origin,
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
    HealEffect(
        target=TargetShorthand.ALLY_NEXUS_OR_BOARD_UNITS,
        value=3,
    )
    return Unit(play_effect=effect)


#
def EnragedYeti():
    return Unit


# When I'm summoned, create an Enraged Yeti in the top 3 cards of your deck.
def AvarosanTrapper():
    CreateCardEffect(
        EnragedYeti,
        location=LocEnum.DECK,
        index=...,
    )
    return Unit(summon_effect=effect)


# Play: Deal 1 to an enemy.
def AvarosanMarksman():
    PlaySkill(Set1Skills.Bullseye)
    return Unit(play_effect=effect)


#
def SnowHare():
    return Unit


# When I'm summoned, the enemy summons a Snow Hare.
def StalkingWolf():
    CreateCardEffect(
        SnowHare,
        LocEnum.HOMEBASE,
        owner=TargetPlayer.OPPONENT,
    )
    return Unit(summon_effect=effect)


# Play: Frostbite an enemy.
def IcevaleArcher():
    FrostbiteEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT,
    )
    return Unit(play_effect=effect)


# Enlightened: I have +4|+4.
def FeralMystic():
    BuffEffect(
        target=origin,
        attack=4,
        health=4,
    )
    # TODO
    return Unit()


# Last Breath: Draw 1.
def AvarosanSentry():
    DrawEffect()
    return Unit(last_breath_effect=effect)


# When I survive damage, grant me +3|+0.
def UnscarredReaver():
    BuffEffect(
        target=origin,
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
    CreateCardEffect(
        EnragedYeti,
        LocEnum.DECK,
        quantity=2,
    )
    return Unit(last_breath_effect=effect)


# When I'm summoned, grant the top 2 allies in your deck +1|+1.
def OmenHawk():
    BuffEffect(
        target=CardFilter(location=LocEnum.DECK, quantity=2),
        attack=1,
        health=1,
    )
    return Unit(summon_effect=effect)


# When I'm summoned, create another random 1 cost Poro in hand.
def LonelyPoro():
    CreateCardEffect(
        target=BaseCardFilter(subtype=SubTypes_.PORO, cost=1),
    )
    return Unit(summon_effect=effect)


# When I'm summoned, create another random 1 cost Poro in hand.
def JubilantPoro():
    CreateCardEffect(
        target=BaseCardFilter(subtype=SubTypes_.PORO, cost=1),
    )
    return Unit(summon_effect=effect)


# When I'm summoned, refill 2 spell mana.
def EagerApprentice():
    RefillSpellMana(value=2)
    return Unit(summon_effect=effect)


# Last Breath: Deal 1 to EACH Nexus.
def CausticCask():
    DamageEffect(
        target=TargetPlayer.ALL_PLAYERS,
        value=1,
    )
    return Unit(last_breath_effect=effect)


#
def AcademyProdigy():
    return Unit


# When you draw a card, give me +1|+0 this round.
def AstuteAcademic():
    BuffEffect(
        target=origin,
        attack=1,
        round_only=True,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.DRAW, action=effect, ally_enum=OriginEnum.T_ALLY
    )
    return Unit(effects=ta)


# Play: Discard a card to draw 1.
def ZauniteUrchin():
    DiscardEffect(target=TargetShorthand.ALLIED_HAND_CARD)
    effect1 = DrawEffect(fizz_if_fail=effect)
    return Unit(play_effect=[effect, effect1])


# Attack: Deal 2 to the enemy Nexus.
def BoomcrewRookie():
    PlaySkill(target=Set1Skills.Undermine)
    return Unit(attack_commit_effect=effect)


# When I'm summoned, create a Mushroom Cloud in hand.
def ClumpofWhumps():
    CreateCardEffect(
        Set1Spells.MushroomCloud,
    )
    return Unit(summon_effect=effect)


# When I'm discarded, summon me.
def FlameChompers():
    effect1 = SummonEffect(target=origin)
    ta = ActionReplacement(
        event_filter=EntityEvents.DISCARD,
        replacement_action=effect1,
        ally_enum=OriginEnum.T_SELF,
    )
    return Unit(effects=ta)


# Support: Create 4 copies of the supported ally in your deck.
def ParadeElectrorig():
    CreateCardEffect(
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
    PlantPuffcaps(quantity=3)
    ta = TriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL, action=effect, ally_enum=OriginEnum.T_ALLY
    )
    return Unit(effects=ta)


# Play: Discard a card to draw 1.
def SumpDredger():
    DiscardEffect(target=TargetShorthand.ALLIED_HAND_CARD)
    effect1 = DrawEffect(fizz_if_fail=effect)
    return Unit(play_effect=[effect, effect1])


# When I'm summoned, summon 2 Caustic Casks.
def UsedCaskSalesman():
    CreateCardEffect(
        CausticCask,
        LocEnum.HOMEBASE,
        quantity=2,
    )
    return Unit(summon_effect=effect)


# When I'm summoned, create in hand a random card for each Back Alley Barkeep you've summoned this game.
def BackAlleyBarkeep():
    value = EventQueryInstances(query=EventQuery(event=EntityEvents.SUMMON))
    target_obj = BaseCardFilter(type=None, quantity=value)
    CreateCardEffect(target_obj)
    return Unit(summon_effect=effect)


#
def EscapedAbomination():
    return Unit


# Last Breath: Summon an Escaped Abomination.
def CursedKeeper():
    CreateCardEffect(
        EscapedAbomination,
        location=LocEnum.HOMEBASE,
    )
    return Unit(last_breath_effect=effect)


# When you summon an Ephemeral ally, grant it +1|+1.
def SoulShepherd():
    BuffEffect(
        target=PostEventParam.TARGET,
        attack=1,
        health=1,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        condition=...,
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
    return Unit


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
    return Unit


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
