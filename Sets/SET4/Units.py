from random import choice
from Sets.SET3.CustomEffects import MechanizedMimicEffect, MountainSojournersEffect
import Sets.SET3.Skills as Set3Skills
import Sets.SET1.Spells as Set1Spells
import Sets.SET1.Champions as Set1Champions

import Sets.SET4.Champions as Set4Champions
import Sets.SET2.Spells as Set2Spells
import Sets.SET1.Units as Set1Units
import Sets.SET2.Units as Set2Units
import Sets.SET3.Units as Set3Units
import Sets.SET3.Spells as Set3Spells
import Sets.SET4.Spells as Set4Spells
import Sets.SET1.Skills as Set1Skills
import Sets.SET2.Skills as Set2Skills
import Sets.SET4.Skills as Set4Skills
import Sets.SET3.Units as Set4Units
import Sets.SET4.Landmarks as Set4Landmarks
import Sets.SET6.Equipments as Set6Equipments
from actions.action_modifiers.silence import SilenceEffect
from actions.activations.copy_spell import CopySpellWithSameTargets
from actions.activations.multiple_activations import MultipleActivationsEffect
from actions.activations.negate_spell import NegateSpell
from actions.activations.play_skill import PlaySkill
from actions.activations.recast_spell import RecastEventOfAction
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
from actions.attribute.gain_stats_of_another import GainStatsAndKeywords
from actions.attribute.heal import HealEffect
from actions.attribute.phase import PhaseMoonWeaponEffect
from actions.attribute.rally import RallyEffect
from actions.attribute.refill_mana import RefillManaEffect, RefillSpellMana
from actions.attribute.reveal import RevealEffect
from actions.attribute.set_attribute import SetAttribute
from actions.attribute.shuffle_attributes import StatShuffleEfect
from actions.attribute.support import SupportEffect
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
from actions.keywords.copy_keywords import CopyKeywords
from actions.keywords.remove_keyword import PurgeKeywordsEffect, RemoveKeywordEffect
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
from actions.reactions.action_modifier import ActionModifier
from actions.reactions.action_negator import ActionNegator
from actions.reactions.action_replacement import ActionReplacement
from actions.reactions.dynamic_attr_modifier import (
    DynamicAttackModifier,
    DynamicAttributeModifier,
    DynamicCostModifier,
    DynamicKeywordModifier,
)
from actions.reactions.event_filter import EventFilter
from actions.reactions.onceyouve import OnceYouve
from actions.reactions.state_triggered_action import StateTriggeredAction
from actions.reactions.triggered_action import AllyOrigin_TA, TriggeredAction
from actions.reactions.value_triggered_action import (
    EventCounterEnum,
    ValueTriggeredAction,
)
from actions.requisite.action_requisite import ActionRequisite
from actions.transform.transform import TransformEffect
from actions.traps.set_trap import (
    ActivateBoons,
    PlantChimes,
    PlantMysteriousPortalEffect,
    PlantPuffcaps,
    SetTrapEffect,
    TrapMultiplier,
)
from card_classes.spell import Spell
from card_classes.unit import Unit
from conditions.base_condition import Condition
from entity_selectors.base_card_filter import BaseCardFilter, InvokeBaseCardFilter
from entity_selectors.card_filter import (
    BeholdingFilter,
    CardFilter,
    CardFilterSelector,
    DrawCardFilter,
    EntityFilter,
    StackSpellFilter,
)
from entity_selectors.input import ChoiceAction, ChoiceBaseCard, Input
from entity_selectors.target_game_card import TargetEntity
from enums.attribute import AttrEnum
from enums.card_rarity import CardRarity
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
from enums.region import RegionEnum
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


# When you summon a Tech, we share keywords.
def Adaptatron3000():
    # TODO custom func
    effect = CopyKeywords(
        target=AutoEntitySelector.SELF,
        keyword_source=PostEventParam.TARGET,
    )
    effect1 = CopyKeywords(
        target=PostEventParam.TARGET,
        keyword_source=AutoEntitySelector.SELF,
    )
    effect2 = TriggeredAction(
        event=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        action=(effect, effect1),
        condition=Condition(
            target=PostEventParam.TARGET,
            condition=CardFlags.IS_SUBTYPE_X,
            parameter=SubTypes_.TECH,
        ),
    )
    return Unit(effects=effect2)


#
def BloodthirstyMarauder():
    return Unit()


# Once you've summoned a landmark this game, grant me +2|+2.
def Chip():
    effect = BuffEffect(target=AutoEntitySelector.SELF, attack=2, health=2)
    ta = OnceYouve(state=PlayerFlags.HAS_SUMMONED_LANDMARK_THIS_GAME, action=effect)
    return Unit(effects=ta)


# The next time you summon another ally, deal 1 to it and grant me +1|+1.
def CrimsonBloodletter():
    effect4 = DamageEffect(target=PostEventParam.TARGET, value=1)
    effect5 = BuffEffect(target=AutoEntitySelector.SELF, attack=1, health=1)
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        action=(effect4, effect5),
        activate_once=True,
    )
    return Unit(effects=ta)


# When I'm Recalled, draw 1.
def DancingDroplet():
    effect = DrawEffect()
    ta = TriggeredAction(
        event_filter=EntityEvents.RECALL,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
    )
    return Unit(effects=ta)


# I have 3 random keywords.
def ExaltedPoro():
    effect = AddRandomKeywordEffect(AutoEntitySelector.SELF, count=3)
    return Unit(summon_effect=effect)


# Round Start: If you've leveled a champion, transform me into Exalted Poro.
def DestinedPoro():
    effect = TransformEffect(
        target=AutoEntitySelector.SELF,
        new_form=ExaltedPoro,
        activation_timing=GameStateEnums.ROUND_START,
        condition=PlayerFlags.HAS_LEVELED_CHAMP_THIS_GAME,
    )
    effect = DrawEffect()
    ta = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START,
        action=effect,
        condition=PlayerFlags.HAS_LEVELED_CHAMP_THIS_GAME,
    )
    return Unit(effects=ta)


# When you play a Dragon, it strikes me and you draw 1.
def DragonChow():
    effect1 = StrikeEffect(
        target=AutoEntitySelector.SELF, striker=PostEventParam.TARGET
    )
    effect2 = DrawEffect()
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        action=(effect1, effect2),
        condition=Condition(
            target=PostEventParam.TARGET,
            condition=CardFlags.IS_SUBTYPE_X,
            parameter=SubTypes_.DRAGON,
        ),
    )
    return Unit(effects=ta)


# If you see me in a Prediction, summon me.
def Dropboarder():
    effect = MoveEffect(
        target=AutoEntitySelector.SELF,
        location=LocEnum.HOMEBASE,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.PREDICTION_SEEN,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
    )
    return Unit(effects=ta)


# When I'm summoned, summon a Sand Soldier.
def Dunekeeper():
    effect = CreateCardEffect(SandSoldier, LocEnum.HOMEBASE)
    return Unit(summon_effect=effect)


# Nexus Strike: Deal 1 to the enemy Nexus.
def SandSoldier():
    effect = DamageEffect(
        target=TargetPlayer.OPPONENT,
        value=1,
    )
    return Unit(nexus_strike_effect=effect)


# When I'm summoned, create a Hexite Crystal in the bottom 10 cards of your deck.
def FallenFeline():
    effect = CreateCardEffect(
        Set4Spells.HexiteCrystal,
        LocEnum.DECK,
        index=(-9, 0),
    )
    return Unit(summon_effect=effect)


# When I'm supported, give me and my supporting ally +1|+1 this round.
def FrightenedIbex():
    effect = BuffEffect(
        target=PostEventParam.SUPPORTER, attack=1, health=1, round_only=True
    )
    effect1 = BuffEffect(
        target=AutoEntitySelector.SELF, attack=1, health=1, round_only=True
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUPPORT,
        ally_enum=OriginEnum.T_SELF,
        action=(effect, effect1),
    )
    return Unit(effects=ta)


# When I'm summoned, if you Behold an Elite, create a Tattered Banner in hand.
def PenitentSquire():
    effect = CreateCardEffect(Set4Spells.TatteredBanner)
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
        condition=Condition(
            target=TargetPlayer.ORIGIN_OWNER,
            condition=PlayerFlags.IS_BEHOLDING_X_CARD,
            parameter=BeholdingFilter(subtype=SubTypes_.ELITE),
        ),
    )
    return Unit(effects=ta)


# When I'm summoned, grant me +1|+1 if an ally has Ephemeral.
def ShadowApprentice():
    effect = BuffEffect(target=AutoEntitySelector.SELF, attack=1, health=1)

    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
        condition=Condition(
            target=TargetPlayer.ORIGIN_OWNER,
            condition=PlayerFlags.HAS_X_CARD_IN_PLAY,
            parameter=CardFilter(keyword=KeywordEnum.EPHEMERAL),
        ),
    )
    return Unit(effects=ta)


#
def Sharkling():
    return Unit()


#
def Prey():
    return Unit()


# When I'm summoned, summon a Prey.
def FirstWave():
    effect = CreateCardEffect(Prey, LocEnum.HOMEBASE)
    return Unit(summon_effect=effect)


# To play me, kill an ally.
def LastWind():
    effect = KillAction(target=TargetShorthand.ALLIED_BOARD_UNIT)
    return Unit(play_requisite=effect)


# Play: Play me as First Wave or Last Wind.
def TheWingsandTheWave():
    effect = ChoiceBaseCard(choices=[FirstWave, LastWind])
    effect1 = PlayCard()
    # TODO alternative play card
    return


# When an enemy blocks me, give me +3|+0 this round.
def ThrashingSnapper():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=3,
        round_only=True,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.BLOCK,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
    )
    # TODO declare vs post event
    return Unit(effects=ta)


# When I'm summoned, create a Waking Sands in hand.
def TreasureSeeker():
    effect = CreateCardEffect(Set4Spells.WakingSands)
    return Unit(summon_effect=effect)


#
def XersaiHatchling():
    return Unit()


# Play: Predict.
def AspiringChronomancer():
    effect = PredictEffect()
    return Unit(play_effect=effect)


# When you slay a unit, grant me +1|+0.
def BaccaiReaper():
    effect = BuffEffect(target=AutoEntitySelector.SELF, attack=1)
    ta = TriggeredAction(
        event_filter=EntityEvents.SLAY,
        ally_enum=OriginEnum.O_ALLY,
        action=effect,
    )
    return Unit(effects=ta)


# Reputation: When I'm summoned, transform me into an exact copy of the strongest ally
# that struck this round.
def BlackRoseSpy():
    new_form = ...
    effect = TransformEffect(
        target=AutoEntitySelector.SELF,
        new_form=...,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
        condition=PlayerFlags.REPUTATION,
    )
    # TODO
    return Unit(effects=ta)


# Play: Blade Dance 2.
def BlossomingBlade():
    effect = BladedanceEffect(quantity=2)
    return Unit(play_effect=effect)


# Last Breath: Summon a Crest of Insight.
def BlueSentinel():
    effect = CreateCardEffect(
        Set4Landmarks.CrestofInsight,
        LocEnum.HOMEBASE,
    )
    return Unit(last_breath_effect=effect)


# When I'm summoned, create a Flame Chompers! in hand.
def BoomBaboon():
    effect = CreateCardEffect(Set1Units.FlameChompers)
    return Unit(summon_effect=effect)


# Reputation: I cost 2 and when I'm summoned, grant me Overwhelm.
def CallousBonecrusher():
    # TODO dynamic cost vs state switch
    effect = DynamicCostModifier(
        value=3, condition=PlayerFlags.REPUTATION, operator=Ops_.SET
    )
    effect1 = AddKeywordEffect(
        target=AutoEntitySelector.SELF,
        keyword=KeywordEnum.OVERWHELM,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_SELF,
        action=effect1,
        condition=PlayerFlags.REPUTATION,
    )
    return Unit(effects=(ta, effect))


# Play: I strike an ally or deal 3 to your Nexus.
# When I slay a unit, drain 1 from the enemy Nexus.
def CamavoranDragon():
    effect = DrainEffect(target=TargetPlayer.OPPONENT, value=1)
    ta = TriggeredAction(
        event_filter=EntityEvents.SLAY,
        ally_enum=OriginEnum.O_SELF,
        action=effect,
    )
    effect2 = StrikeEffect(
        target=TargetShorthand.ALLY_NEXUS_OR_BOARD_UNITS,
        striker=AutoEntitySelector.SELF,
    )
    return Unit(effects=ta, play_effect=effect2)


# When I'm summoned, summon an Encroaching Mist.
def CamavoranSoldier():
    effect = CreateCardEffect(EncroachingMist, LocEnum.HOMEBASE)
    return Unit(summon_effect=effect)


# Reduce my cost by 1 for each time an ally attacked this game.
def SandstoneChimera():
    # TODO dynamic modifier has active modifier
    effect = DynamicCostModifier(value=PlayerStatistic.ALLY_ATTACKED_THIS_GAME)
    return Unit(effects=effect)


# When I'm summoned, double other allies' Power and Health and grant them Challenger.
def CithriaLadyofClouds():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=2,
        health=2,
        keyword=KeywordEnum.CHALLENGER,
        operator=Ops_.MULTIPLY,
    )
    return Unit(summon_effect=effect)


# Play: Kill an ally to deal 3 to the enemy Nexus.
def AstralFox():
    effect = PlaySkill(target=Set4Skills.SymmetryInStars)
    return Unit(play_effect=effect)


def AtakhanBringerOfRuinEffect():
    value = ...
    effect = BuffEffect(target=AutoEntitySelector.SELF, attack=value)
    return effect


def AtakhanBringerOfRuin():
    # TODO custom function
    return Unit(attack_commit_effect=AtakhanBringerOfRuinEffect)


# When you Blade Dance, I attack with the Blades.
# Play: Blade Dance 1.
def ZinneiaSteelCrescendo():
    effect1 = MoveEffect(target=AutoEntitySelector.SELF, location=LocEnum.BATTLEFIELD)
    effect = BladedanceEffect(
        quantity=1,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.BLADE_DANCE,
        ally_enum=OriginEnum.T_ALLY,
        action=effect1,
        condition=Condition(
            target=TargetPlayer.ORIGIN_OWNER,
            condition=PlayerFlags.LOCATION_HAS_SPACE,
            parameter=LocEnum.BATTLEFIELD,
        ),
    )
    return Unit(play_effect=effect, effects=ta)


# When I'm summoned, create 2 Instant Centuries in hand.
def TheClockHand():
    effect = CreateCardEffect(Set4Spells.InstantCentury, quantity=2)
    return Unit(summon_effect=effect)


#
def Clockling():
    return Unit()


# Play: If you've slain 13+ units this game, kill all enemy followers, then summon a copy of me.
def SanctumConservator():
    effect = PlaySkill(target=Set4Skills.ConservatorsJudgment)
    ta = TriggeredAction(
        event_filter=EntityEvents.PLAY,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
        condition=...,
    )
    # TODO vta
    return Unit(effects=ta)


# Play: Each Lurker ally strikes a random enemy.
def Jaullfish():
    effect = PlaySkill(target=Set4Skills.FrenziedFeast)
    return Unit(play_effect=effect)


# Reputation: I cost 6. When I'm summoned, Rally.
def IncisiveTactician():
    effect1 = DynamicCostModifier(
        value=6, operator=Ops_.SET, condition=PlayerFlags.REPUTATION
    )
    effect = RallyEffect()
    return Unit(summon_effect=effect, effects=effect1)


# Round Start: If you have 2+ Yetis, summon me from hand and create a copy of me in your deck.
# Play: Draw a Yeti.
def AbominableGuardian():
    effect = MoveEffect(target=AutoEntitySelector.SELF, location=LocEnum.HOMEBASE)
    effect1 = CreateCardEffect(target=AbominableGuardian, location=LocEnum.DECK)
    effect2 = DrawEffect(
        filter_obj=BaseCardFilter(subtype=SubTypes_.YETI),
    )
    condition1 = Condition(
        target=TargetPlayer.ORIGIN_OWNER,
        condition=PlayerFlags.LOCATION_HAS_SPACE,
        parameter=LocEnum.HOMEBASE,
    )
    condition2 = ...
    ta = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START,
        action=(effect, effect1),
        location=LocEnum.HAND,
        condition=(condition2, condition1),
    )
    return Unit(effects=ta, play_effect=effect2)


# When I'm summoned, create a copy of me in hand if you've leveled a champion this game.
def ThrummingSwarm():
    effect = CreateCardEffect(ThrummingSwarm)
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
        condition=PlayerFlags.HAS_LEVELED_CHAMP_THIS_GAME,
    )
    return Unit(effects=ta)


# Play: Kill an ally to kill an enemy.
def TheEtherfiend():
    effect = PlaySkill(target=Set4Skills.TheSecondDeath)
    return Unit(play_effect=effect)


# When I'm summoned, draw a Shen. Allies with Barrier have Double Attack.
def SacredProtector():
    effect = DynamicKeywordModifier(
        value=KeywordEnum.DOUBLESTRIKE,
        target=CardFilter(keyword=KeywordEnum.BARRIER),
    )
    effect2 = AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT, keyword=KeywordEnum.BARRIER
    )
    effect3 = DrawEffect(filter_obj=DrawCardFilter(card_class=Set1Champions.Shen))
    return Unit(play_effect=(effect2, effect3), effects=effect)


# Attack: Give enemies -2|-0 this round.
def RazBloodmane():
    effect = BuffEffect(
        target=CardFilter(owner=TargetPlayer.OPPONENT),
        attack=-2,
        round_only=True,
    )
    return Unit(attack_commit_effect=effect)


# When I'm summoned, draw Jarvan IV.
# If he's already in play, instead give allies Challenger and Scout this round.
def KingJarvanIII():
    effect3 = DrawEffect(
        filter_obj=DrawCardFilter(card_class=Set4Champions.JarvanIV),
    )
    effect = AddKeywordEffect(
        target=CardFilter(),
        keyword=(KeywordEnum.CHALLENGER, KeywordEnum.SCOUT),
        round_only=True,
    )
    effect2 = BranchingAction(
        condition=Condition(
            target=TargetPlayer.ORIGIN_OWNER,
            condition=PlayerFlags.HAS_CARD_X_ON_BOARD,
            parameter=Set4Champions.JarvanIV,
        ),
        if_true=effect,
        if_false=effect3,
    )
    return Unit(summon_effect=effect2)


# When I'm summoned, grant all allied Viegos and other Encroaching Mists everywhere +1|+1.
def EncroachingMist():
    effect = BuffEverywhereEffect(
        attack=1,
        health=1,
        filter_obj=BaseCardFilter(card_class=(EncroachingMist, Set4Champions.Viego)),
    )
    return Unit(summon_effect=effect)


# When I'm summoned or Round Start: Summon an Encroaching Mist.
def InvasiveHydravine():
    effect = CreateCardEffect(
        EncroachingMist,
        LocEnum.HOMEBASE,
    )
    return Unit(summon_effect=effect, round_start_effects=effect)


#
def XersaiDunebreaker():
    return Unit()


# I don't take damage from enemy spells or skills.
def ToweringStonehorn():
    effect = ActionNegator(
        event=EntityEvents.DAMAGE, ally_enum=OriginEnum.O_OPPO, condition=...
    )
    # NEGATOR
    return Unit(effects=effect)


# Play: If you've summoned 4+ landmarks this game, deal 4 to an enemy and 2 to the enemy Nexus.
def Stonebreaker():
    # TODO vta
    effect = PlaySkill(target=Set4Skills.ShakenGround)
    ta = TriggeredAction(
        event_filter=EntityEvents.PLAY,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
        condition=PlayerFlags.HAS_SUMMONED_LANDMARK_THIS_GAME,
    )
    return Unit(effects=ta)


#
def SandstoneCharger():
    return Unit()


# Play: I start a free attack.
def SnapjawSwarm():
    effect = FreeAttackEffect(target=AutoEntitySelector.SELF)
    return Unit(play_effect=effect)


# Play: Draw a Burst spell.
# Enlightened: I have Elusive.
def ScatteredPod():
    effect = DrawEffect(
        filter_obj=DrawCardFilter(
            type=Types_.SPELL,
            speed=(SpellSpeedEnum.BURST, SpellSpeedEnum.SLOW, SpellSpeedEnum.FAST),
        )
    )
    effect2 = DynamicKeywordModifier(value=KeywordEnum.ELUSIVE)
    return Unit(play_effect=effect, enlightened_effect=effect2)


#
def GrumpyRockbear():
    return Unit()


#
def RimefangPack():
    return Unit()


# When I'm summoned, summon a Rimefang Pack.
# Grant it +1|+1 for each time you have Frostbitten enemies this game.
def RimefangDenmother():
    effect1 = BuffEffect(
        target=PostEventParam.TARGET,
        attack=PlayerStatistic.FROSTBITTEN_ENEMIES,
        val=PlayerStatistic.FROSTBITTEN_ENEMIES,
    )
    effect = CreateCardEffect(RimefangPack, LocEnum.HOMEBASE, coevent=effect1)
    return Unit(summon_effect=(effect, effect1))


# When I'm summoned, create a copy of me in your deck.
# When you see me in a Prediction, grant all allied copies of me everywhere +2|+2.
def KhahiritheReturned():
    effect = BuffEverywhereEffect(
        attack=2,
        health=2,
        filter_obj=BaseCardFilter(card_class=KhahiritheReturned),
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.PREDICTION_SEEN,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
    )

    effect1 = CreateCardEffect(
        KhahiritheReturned,
        LocEnum.DECK,
    )
    return Unit(summon_effect=effect1, effects=ta)


# Play: Grant an ally Challenger and +1|+1.
def KadregrintheRuined():
    effect1 = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=1,
        health=1,
        keyword=KeywordEnum.CHALLENGER,
    )
    return Unit(play_effect=effect1)


# When you summon another ally, give it +2|+0 this round.
def InspiringMarshal():
    effect1 = BuffEffect(
        target=PostEventParam.TARGET,
        attack=2,
        round_only=True,
    )
    #TODO origin and target different
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        action=effect1,
    )
    return Unit(effects=ta)


# When you summon an Elite, reduce my cost by 1.
def ArdentTracker():
    effect1 = BuffCostEffect(target=AutoEntitySelector.SELF)
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        action=effect1,
        condition=Condition(
            target=PostEventParam.TARGET,
            condition=CardFlags.IS_SUBTYPE_X,
            parameter=SubTypes_.ELITE
        ),
    )
    return Unit(effects=ta)


# Attack: If I have 8+ Power, give me Fearsome, Overwhelm, and SpellShield this round.
def XerxaRethTheUndertitan():
    effect = AddKeywordEffect(
        target=AutoEntitySelector.SELF,
        keyword=(KeywordEnum.OVERWHELM, KeywordEnum.SPELLSHIELD, KeywordEnum.FEARSOME),
        round_only=True,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.ATTACK_COMMIT,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
        condition=Condition(
            target=AutoEntitySelector.SELF,
            condition=CardFlags.ATTACK_REACHES_AMOUNT,
            parameter=8
        ),
    )
    return Unit(effects=ta)


# Strike: Create a Lucky Find in hand.
def VekauranBruiser():
    effect = CreateCardEffect(Set4Spells.LuckyFind)
    return Unit(strike_effect=effect)


# When you target me, grant me +1|+0.
def RetiredReckoner():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=1,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.TARGETED,
        ally_enum=OriginEnum.T_SELF_O_ALLY,
        action=effect,
    )
    return Unit(effects=ta)


# Play: Cast Cannon Barrage on randomly targeted enemies for each card you've drawn this round,
# up to 6 times.
def RuinedRex():
    effect = PlaySkill(Set2Skills.CannonBarrage)
    effect1 = MultipleActivationsEffect(effect=effect, multiplier=...)
    return Unit(play_effect=effect1)


# Play: If you've slain 4+ units this game, an enemy and I strike each other.
def RampagingBaccai():
    #TODO vta
    effect = PlaySkill(Set4Skills.BaccaiRampage)
    ta = TriggeredAction(
        event_filter=EntityEvents.PLAY,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
        condition=...,
    )
    return Unit(effects=ta)


# Play: Advance an allied landmark 3 rounds.
def Preservationist():
    effect = AdvanceCountdownEffect(
        target=TargetShorthand.ALLIED_COUNTDOWN_LANDMARK,
        value=3,
    )
    return Unit(play_effect=effect)


# Attack: Deal 1 to enemies and the enemy Nexus.
def SumpworksPosse():
    effect = PlaySkill(Set4Skills.CircuitBreaker)
    return Unit(attack_commit_effect=effect)


# When you summon another Chirean Sumpworker, Obliterate me
# and transform allied Chirean Sumpworkers everywhere into Sumpworks Posses.
def ChireanSumpworker():
    effect1 = ObliterateEffect(target=AutoEntitySelector.SELF)
    effect2 = ...  # TODO buffeverywere?
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        action=(effect1, effect2),
        condition=Condition(
            target=PostEventParam.TARGET,
            condition=CardFlags.IS_CARD_CLASS,
            parameter=ChireanSumpworker
        ),
    )
    return Unit(effects=ta)


# Play: Advance an allied landmark 2 rounds.
def ClockworkCurator():
    effect = AdvanceCountdownEffect(
        target=TargetShorthand.ALLIED_LANDMARK,
        value=2,
    )
    return Unit(play_effect=effect)


# When I'm summoned, summon a Prey.
def FadingIcon():
    effect = CreateCardEffect(Prey, LocEnum.HOMEBASE)
    return Unit(summon_effect=effect)


# Play: Kill an ally to grant me its stats and keywords.
def MaskMother():
    #TODO shared target
    target_obj = TargetEntity(target=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = KillAction(target=target_obj)
    effect1 = GainStatsAndKeywords(
        target=target_obj,
        source=PostEventParam.TARGET
    )
    return Unit(play_effect=effect)


# The first time I Challenge an enemy, give me Barrier this round.
def HonoredLord():
    effect = AddKeywordEffect(
        target=AutoEntitySelector.SELF,
        keyword=KeywordEnum.BARRIER,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.CHALLENGE,
        ally_enum=OriginEnum.O_SELF,
        action=effect,
        activate_once=True,
    )
    return Unit(effects=ta)


# Play: Grant an enemy Vulnerable.
def RedfinHammersnout():
    effect = AddKeywordEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT,
        keyword=KeywordEnum.VULNERABLE,
    )
    return Unit(play_effect=effect)


# Play: Blade Dance 1.
def RibbonDancer():
    effect = BladedanceEffect(quantity=1)
    return Unit(play_effect=effect)


# Obliterate me when I leave combat.
def Blade():
    effect = ObliterateEffect(target=AutoEntitySelector.SELF)
    ta = TriggeredAction(
        event_filter=EntityEvents.MOVE,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
        condition=...,
    )
    #TODO postevent condition
    return Unit(effects=ta)


# When I'm summoned, grant 3 random allies in your deck +3|+3.
def XenotypeResearchers():
    effect = BuffEffect(
        target=CardFilterSelector(
            location=LocEnum.DECK,
            quantity=3,
        ),
        attack=3,
        health=3,
    )
    return Unit(summon_effect=effect)


# Play: Predict.
def XersaiCaller():
    effect = PredictEffect()
    return Unit(play_effect=effect)


# When I'm summoned, draw 1.
def EmperorsGuard():
    effect = DrawEffect()
    return Unit(summon_effect=effect)


# When I'm summoned, draw 1.
# Round End: The Strongest enemy and I strike each other.
def EternalGladiator():
    effect = DrawEffect()
    effect1 = MutualStrikeEffect(
        first_striker=AutoEntitySelector.SELF,
        second_striker=AutoEntitySelector.STRONGEST_OPPONENT_BOARD_UNIT,
    )
    return Unit(summon_effect=effect, round_end_effects=effect1)


# Play and Round Start: Summon 2 Sand Soldiers and grant them +2|+2.
def GoldenHerald():
    effect = CreateCardEffect(
        SandSoldier,
        LocEnum.HOMEBASE,
        quantity=2,
        attack=(Ops_.INCREMENT, 2),
        health=(Ops_.INCREMENT, 2),
    )

    return Unit(play_effect=effect, round_start_effects=effect)


# I cost 0 if you've summoned 5+ allies that cost 8+ this game.
# Attack: Obliterate the enemy deck, leaving 3 non-champions.
def Watcher():
    effect = ObliterateEffect()
    effect1 = DynamicCostModifier(
        quantity=...,
    )
    # TODO wtf1
