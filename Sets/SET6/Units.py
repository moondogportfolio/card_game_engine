import Sets.SET1.Units as Set1Units
import Sets.SET2.Units as Set2Units
import Sets.SET3.Spells as Set3Spells
import Sets.SET6.Spells as Set6Spells
import Sets.SET6.Skills as Set6Skills
import Sets.SET4.Landmarks as Set4Landmarks
import Sets.SET6.Equipments as Set6Equipments
import Sets.SET6.Units as Set6Units
from actions.activations.play_skill import PlaySkill
from actions.attachments.destroy import DestroyEquipEffect
from actions.attachments.equip import EquipEffect
from actions.attachments.forge import ForgeEffect
from actions.attachments.improvise import ImproviseEffect
from actions.attack.free_attack import FreeAttackEffect
from actions.attribute.buff import BuffCostEffect, BuffEffect
from actions.attribute.buff_everywhere import BuffEverywhereEffect
from actions.attribute.countdown import AdvanceCountdownEffect
from actions.attribute.damage import DamageEffect
from actions.attribute.gain_mana_gem import GainManaGemEffect
from actions.attribute.gain_stats_of_another import GainStatsAndKeywords
from actions.attribute.heal import HealEffect
from actions.attribute.refill_mana import RefillSpellMana
from actions.attribute.set_attribute import SetAttribute
from actions.attribute.support import SupportEffect
from actions.common.strike import MutualStrikeEffect

from actions.create.create_card import CreateCardEffect
from actions.create.create_copy import CreateExactCopyEffect
from actions.create.create_hand_cards import ReforgeEffect
from actions.create.manifest import ManifestEffect
from actions.create.summon_specific_cards import SpawnEffect, SummonHuskEffect
from actions.keywords.add_keyword import AddKeywordEffect, AddRandomKeywordEffect
from actions.keywords.copy_keywords import CopyKeywords
from actions.movement.draw import DrawEffect
from actions.movement.kill import KillAction
from actions.movement.move import MoveEffect
from actions.movement.predict import PredictEffect
from actions.movement.recall import RecallEffect
from actions.postevent import PostEventParamGetter
from actions.reactions.action_negator import ActionNegator
from actions.reactions.dynamic_attr_modifier import (
    DynamicAtkHPModifier,
    DynamicAttackModifier,
    DynamicAttributeModifier,
    DynamicCostModifier,
    DynamicKeywordModifier,
)
from actions.reactions.event_filter import EventFilter
from actions.reactions.onceyouve import OnceYouve
from actions.reactions.triggered_action import AllyOrigin_TA, TriggeredAction
from actions.requisite.action_requisite import ActionRequisite
from actions.transform.transform import TransformEffect
from actions.traps.set_trap import (
    PlantChimes,
    PlantMysteriousPortalEffect,
    TrapMultiplier,
)
from card_classes.cardarchetype import CardArchetype
from card_classes.unit import Unit
from conditions.base_condition import (
    AttributeCondition,
    Condition,
    ConditionOperator,
    PostEventAttributeCondition,
)
from entity_selectors.base_card_filter import (
    BaseCardFilter,
    BaseCardRandomSelector,
    InvokeBaseCardFilter,
    ManifestBaseCardFilter,
)
from entity_selectors.card_filter import (
    CardFilter,
    CardFilterSelector,
    DrawCardFilter,
    EntityFilter,
)
from entity_selectors.input import ChoiceAction, ChoiceBaseCard, Input
from entity_selectors.target_game_card import TargetEntity
from enums.attribute import AttrEnum
from enums.card_sorters import CardSorter
from enums.counters import TrapEnums
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
from events.event_query_enum import EventQueryParamGetter
from resolvable_enums.active_cards_selector import TargetShorthand
from resolvable_enums.auto_card_selector import AutoEntitySelector
from resolvable_enums.card_conditions import CardFlags
from resolvable_enums.player_conditions import PlayerFlags
from resolvable_enums.target_player import TargetPlayer
from value.branching_value import BranchingValue
from value.entity_attribute import EntityAttribute
from value.player_statistic import PlayerStatistic
from value.player_statistic_list import PlayerStatisticList


# When I'm summoned, plant a Chime on the top card of your deck.
def ByrdTheBellringer():
    effect = PlantChimes(quantity=1, top_x_cards=1)
    return Unit(summon_effect=effect, cardcode="06BC026")


#
def Tentacle():
    return Unit(cardcode="06BW006T3")


class Husk(Unit):
    def __attrs_post_init__(self):
        effect = KillAction(target=AutoEntitySelector.SELF)
        effect1 = GainStatsAndKeywords(
            target=PostEventParam.TARGET,
            source=AutoEntitySelector.SELF,
        )
        effect2 = TriggeredAction(
            event=EntityEvents.SUMMON,
            ally_enum=OriginEnum.T_ALLY_O_ALLY,
            action=(effect, effect1),
        )
        self.effects = effect2
        return super().__attrs_post_init__()


# Round Start: Deal 2 to me and Spawn 1.
def WatchfulIdol():
    effect = DamageEffect(target=AutoEntitySelector.SELF, value=2)
    effect1 = SpawnEffect(quantity=1)
    return Unit(cardcode="06BW007", round_start_effects=(effect, effect1))


# When I'm summoned, grow my stats to that of your strongest Tentacle
# and grant me its keywords.
def NagakabourosTentacle():
    effect = GainStatsAndKeywords(
        target=AutoEntitySelector.SELF,
        source=AutoEntitySelector.ALLIED_STRONGEST_TENTACLE,
        operator=Ops_.GROW,
    )
    return Unit(summon_effect=effect, cardcode="06BW011T2")


# Play: Advance all your Frozen Thralls 1 round.
def HarbingerofThralls():
    effect = CreateCardEffect(Set4Landmarks.FrozenThrall, LocEnum.HOMEBASE)
    effect1 = AdvanceCountdownEffect(
        target=CardFilter(type=None, card_class=Set4Landmarks.FrozenThrall),
        value=1,
    )
    effect2 = ChoiceAction(choices=(effect, effect1))
    return Unit(play_effect=effect2, cardcode="06FR030T1")


# I have +1|+0 for each different round you've damaged the enemy Nexus.
def WharfRat():
    effect = DynamicAttackModifier(
        value=PlayerStatistic.DISTINCT_ROUNDS_DAMAGE_OPPO_NEXUS
    )
    return Unit(effects=effect, cardcode="06BW036")


# Play: Stun an enemy.
def TheStagehand():
    effect = PlaySkill(target=Set6Skills.StunningPerformance)
    return Unit(play_effect=effect, cardcode="06IO003")


# When I'm summoned, plant a Chime on the top card of your deck.
# Support: Grant my supported ally +1|+1.
def EsmusBreathoftheWorld():
    effect = PlantChimes()
    effect1 = SupportEffect(attack=1, health=1)
    return Unit(summon_effect=effect, support_effect=effect1, cardcode="06MT029")


# Play: Stun an enemy or if it's already Stunned deal 2 to it instead.
def SpellSlinger():
    effect = PlaySkill(target=Set6Skills.StiffenedSinews)
    return Unit(play_effect=effect)


# When an ally attacks, I attack with it.
def ObedientDrakehound():
    action = MoveEffect(
        target=AutoEntitySelector.SELF,
        location=LocEnum.BATTLEFIELD,
    )
    te = TriggeredAction(
        event_filter=EntityEvents.PLAYER_ATTACK_COMMIT,
        ally_enum=OriginEnum.T_ALLY,
        action=action,
    )
    return Unit(effects=te, cardcode="06NX032")


# When I'm summoned, create a random Yordle in hand.
# Attack: Grant other allied Yordles +1|+0.
def PaparotheGreat():
    effect = CreateCardEffect(
        target=BaseCardRandomSelector(subtype=SubTypes_.YORDLE),
    )
    effect1 = BuffEffect(
        target=CardFilter(subtype=SubTypes_.YORDLE),
        attack=1,
        exclude_origin=True,
    )
    return Unit(summon_effect=effect, attack_commit_effect=effect1, cardcode="06BC036")


# Play: A 1 cost ally starts a free attack.
def BuhruLeader():
    target_obj = TargetEntity(choices=CardFilter(cost=1))
    effect1 = FreeAttackEffect(target=target_obj)
    return Unit(play_effect=effect1, cardcode="06BW009")


# Attack: Spawn 1 and give your strongest Tentacle Overwhelm this round.
def TheSeasVoice():
    effect = AddKeywordEffect(
        target=TargetShorthand.ALLIED_STRONGEST_TENTACLE,
        keyword=KeywordEnum.OVERWHELM,
        round_only=True,
    )
    effect1 = SpawnEffect(quantity=1)
    return Unit(effects=(effect1, effect), cardcode="06BW035")


# Last Breath: Get an empty mana gem.
def HuntingBoar():
    effect = GainManaGemEffect()
    return Unit(last_breath_effect=effect)


# Play: Recall a unit with less Power than me.
def TheMaker():
    effect = PlaySkill(target=Set6Skills.PeerlessArtistry)
    return Unit(play_effect=effect)


# When you play a Fast spell, Slow spell, or Skill, grant me +1|+0.
def ThePrefect():
    effect = BuffEffect(target=AutoEntitySelector.SELF, attack=1)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.PLAY_FAST_OR_SLOW_OR_SKILL,
        ally_enum=OriginEnum.T_ALLY,
        action=effect,
    )
    return Unit(effects=ta1)


# Each round, the first time you play a Fast spell, Slow spell, or Skill, I play Magic Embers.
def ManasoulStudent():
    effect = PlaySkill(Set6Skills.MagicEmbers)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.PLAY_FAST_OR_SLOW_OR_SKILL,
        ally_enum=OriginEnum.T_ALLY,
        action=effect,
        activations_per_round=1,
    )
    return Unit(effects=ta1)


# Once you're Deep, heal your allies and Nexus 3.
def Megatusk():
    action = HealEffect(target=AutoEntitySelector.OWNER_NEXUS_AND_BOARD_UNITS, value=3)
    effect = OnceYouve(
        state=PlayerFlags.DEEP,
        action=action,
    )
    return Unit(effects=effect)


# Attack: I deal 3 damage to my blocker.
# If it's dead or gone, I deal 3 damage to the enemy Nexus instead.
def CaptiveGreyback():
    effect = PlaySkill(Set6Skills.ObeyedOrder)
    return Unit(attack_commit_effect=effect)


# When I'm summoned, Spawn 3.
def BuhruLookout():
    effect = SpawnEffect(quantity=3)
    return Unit(summon_effect=effect)


# I gain all allied everywhere buffs.
def LegionDeserter():
    pass
    # TODO wtf


# When an enemy is Challenged, give it -2|-0 this round.
def BaccaiWitherclaw():
    action = BuffEffect(
        target=PostEventParam.TARGET,
        attack=-2,
        round_only=True,
    )
    effect1 = TriggeredAction(
        event=EntityEvents.CHALLENGE,
        action=action,
        ally_enum=OriginEnum.T_OPPO,
    )
    return Unit(effects=effect1)


# When I'm summoned, plant a Chime on the top card of your deck,
# then double the boons in your deck.
def MaduliTheGatekeeper():
    effect = PlantChimes()
    effect2 = TrapMultiplier(trap=TrapEnums.BOON)
    return Unit(summon_effect=(effect, effect2))


# When I'm summoned, grant units in your deck my stats, then draw a unit with 5+ Power.
def RevnatheLorekeeper():
    effect = BuffEffect(
        target=CardFilter(location=LocEnum.DECK),
        attack=EntityAttribute(
            target=AutoEntitySelector.SELF, attribute=AttrEnum.ATTACK
        ),
        health=EntityAttribute(
            target=AutoEntitySelector.SELF, attribute=AttrEnum.HEALTH
        ),
    )
    effect1 = DrawEffect(filter_obj=DrawCardFilter(attack=(5, 0)))
    return Unit(summon_effect=[effect, effect1])


# Play: Stun an enemy, then deal 2 to all Stunned or damaged enemies.
def Tibbers():
    effect = PlaySkill(target=Set6Skills.PyroclasticArrival)
    return Unit(play_effect=effect)


# Play: Deal 2 to an enemy.
# Your Fast spells, Slow spells, and Skills have
# "When I damage a Stunned or damaged enemy, kill it."
def LordBroadmane():
    effect = PlaySkill(target=Set6Skills.KashuriGauntlet)
    effect1 = KillAction(target=PostEventParam.TARGET)
    effect2 = TriggeredAction(
        event_filter=EntityEvents.DAMAGE,
        ally_enum=OriginEnum.T_OPPO_O_ALLY,
        action=effect1,
        condition=...,
    )
    return Unit(play_effect=effect, effects=effect2)


# When I'm summoned, grant allies everywhere +1|+0 and for the rest of the game,
# all of your spells and Skills deal 1 extra damage.
def Tybaulk():
    # TODO buff everywhere
    effect = BuffEverywhereEffect(filter_obj=BaseCardFilter(), attack=1)
    effect1 = BuffEverywhereEffect(
        filter_obj=BaseCardFilter(type=Types_.SKILL), buff_obj=...
    )

    effect = DynamicAttackModifier(value=1, target=CardFilter(location=None))
    return Unit(summon_effect=[effect, effect1])


# Nightfall: Give other allies +2|+1 and Overwhelm this round.
def TheWindingLight():
    effect = BuffEffect(
        target=CardFilter(exclude_origin=True),
        attack=2,
        health=1,
        keyword=KeywordEnum.OVERWHELM,
        round_only=True,
    )
    return Unit(play_nightfall=effect)


# Round Start: Spawn 2. Then, if your strongest Tentacle has 12+ Power,
# create a Nagakabouros' Tantrum in hand.
def Nagakabouros():
    effect = SpawnEffect(quantity=2)
    effect1 = CreateCardEffect(
        target=Set6Spells.NagakabourosTantrum,
        condition=AttributeCondition(
            target=AutoEntitySelector.ALLIED_STRONGEST_TENTACLE,
            attribute=AttrEnum.ATTACK,
            parameter=12,
            operator=ConditionOperator.AT_LEAST,
        ),
    )
    return Unit(round_start_effects=(effect, effect1))


# Attack: Draw a unit. If it's a Dragon, summon it attacking.
def ProtectiveBroodfather():
    effect = DrawEffect(filter_obj=DrawCardFilter())
    effect1 = SummonEffect(
        target=PostEventParam.TARGET,
        destination=LocEnum.BATTLEFIELD,
        condition=Condition(
            target=PostEventParam.TARGET,
            condition=CardFlags.IS_SUBTYPE_X,
            parameter=SubTypes_.DRAGON,
        ),
        coevent=effect,
    )
    return Unit(attack_commit_effect=(effect, effect1))


# When I'm summoned, plant a Mysterious Portal randomly in the top 4 cards of your deck.
def TheTeaMaker():
    effect = PlantMysteriousPortalEffect()
    return Unit(summon_effect=effect)


# When I'm summoned, if one of your traps or boons has activated this round, draw 1.
def LivingLibrary():
    action = DrawEffect()
    effect = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_SELF,
        action=action,
        condition=PlayerFlags.ACTIVATED_TRAP_OR_BOON_THIS_ROUND,
    )
    return Unit(effect=effect)


# Last Breath: Plant a Mysterious Portal randomly in the top 4 cards of your deck.
def JunkConstruct():
    effect = PlantMysteriousPortalEffect()
    return Unit(last_breath_effect=effect)


# Each round, the first time one of your traps or boons activate,
# give all allies +1|+1 and Impact this round.
def RealmsCaretaker():
    effect = BuffEffect(
        target=CardFilter(),
        attack=1,
        health=1,
        round_only=True,
        keyword=KeywordEnum.IMPACT,
    )
    effect1 = TriggeredAction(
        event=EntityEvents.ACTIVATE_TRAP,
        activations_per_round=1,
        action=effect,
        ally_enum=OriginEnum.O_ALLY,
    )
    return Unit(effects=effect1)


# When I'm summoned, I Improvise.
def PiltovanCastaway():
    effect = ImproviseEffect()
    return Unit(summon_effect=effect)


# When I'm summoned, I Improvise and Forge me.
def CombatCook():
    effect = ImproviseEffect()
    effect1 = ForgeEffect(target=AutoEntitySelector.SELF)
    return Unit(summon_effect=(effect, effect1))


# Once you've Equipped an ally this game, grant me Scout.
def RangerKnightDefector():
    effect = DynamicAttributeModifier(
        attribute=AttrEnum.KEYWORDS,
        value=KeywordEnum.SCOUT,
        condition=PlayerFlags.HAS_EQUIPPED_ALLY_THIS_GAME,
    )
    effect1 = OnceYouve(
        state=PlayerFlags.HAS_EQUIPPED_ALLY_THIS_GAME,
        action=effect,
    )
    return Unit(effects=effect1)


# The first time you equip an ally, Forge it.
def WeaponsmithsApprentice():
    effect = ForgeEffect(target=PostEventParam.TARGET)
    effect1 = TriggeredAction(
        event=EntityEvents.IS_EQUIPPED_WITH,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        action=effect,
        activate_once=True,
    )
    return Unit(summon_effect=effect1)


# Play: Forge an ally and heal it and your Nexus 3.
def HearthbloodMender():
    target = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = ForgeEffect(target=target)
    effect1 = HealEffect(target=TargetPlayer.ORIGIN_OWNER, value=3)
    effect2 = HealEffect(target=target, value=3)
    return Unit(play_effect=(effect, effect1, effect2))


# Play: Forge an ally.
def AdeptWeaponsmith():
    effect = ForgeEffect(target=TargetShorthand.ALLIED_BOARD_UNIT)
    return Unit(play_effect=effect)


# When I'm summoned, create a Time and Dedication in hand.
def FavoredArtisan():
    effect = CreateCardEffect(
        target=Set6Spells.TimeandDedication,
    )
    return Unit(summon_effect=effect)


# The first time I'm Equipped, create a copy of me in hand.
# Grant it the equipment's stats.
def WroughtColossus():
    def event(event):
        created = CreateCardEffect(target=WroughtColossus)
        BuffEffect(
            target=created, attack=event.equipment.attack, health=event.equipment.health
        )

    ta = TriggeredAction(
        event=EntityEvents.IS_EQUIPPED_WITH,
        ally_enum=OriginEnum.T_SELF,
        action=event,
        activate_once=True,
    )
    return Unit(effects=ta)


# The first time I'm Equipped, create a copy of me in hand. Grant it the equipment's stats.
def WroughtColossus():
    # TODO multiple postevent / coevent / custom function
    effect = CreateCardEffect(target=WroughtColossus)
    effect2 = BuffEffect(
        target=PostEventParam.CREATED,
        attack=EntityAttribute(
            target=PostEventParam.EQUIPMENT,
            attribute=AttrEnum.ATTACK,
        ),
        health=EntityAttribute(
            target=PostEventParam.EQUIPMENT,
            attribute=AttrEnum.HEALTH,
        ),
        coevent=effect,
    )
    ta = TriggeredAction(
        event=EntityEvents.IS_EQUIPPED_WITH,
        ally_enum=OriginEnum.T_SELF,
        action=(effect, effect2),
        activate_once=True,
    )
    return Unit(effects=ta)


# When I'm summoned, create a Preparation in hand.
def DiscipleofDoran():
    effect = CreateCardEffect(target=Set6Spells.Preparation)
    return Unit(summon_effect=effect)


# The first time I am Equipped, give me Barrier and Lifesteal this round.
def JuntheProdigy():
    action = AddKeywordEffect(
        target=AutoEntitySelector.SELF,
        keyword=(KeywordEnum.BARRIER, KeywordEnum.BARRIER),
        round_only=True,
    )
    effect = TriggeredAction(
        event=EntityEvents.IS_EQUIPPED_WITH,
        activate_once=True,
        ally_enum=OriginEnum.T_SELF,
        action=action,
    )
    return Unit(effects=effect)


# Nexus Strike: Recall me and transform me into Shimon Wind
def VastayanDisciple():
    effect = RecallEffect(target=AutoEntitySelector.SELF)
    effect1 = TransformEffect(
        new_form=Set6Spells.ShimonWind, target=AutoEntitySelector.SELF
    )
    return Unit(nexus_strike_effect=(effect, effect1))


# Once you've Equipped an ally this game, create a Shadow Fiend in hand.
def ShadowbladeFanatic():
    effect = CreateCardEffect(target=Set1Units.ShadowFiend)
    effect1 = OnceYouve(
        state=PlayerFlags.HAS_EQUIPPED_ALLY_THIS_GAME,
        action=effect,
    )
    return Unit(effects=effect1)


# Play: Pick an ally, it Improvises. If you don't, I Improvise.
def WanderingShepherd():
    return Unit(play_effect=...)
    # TODO pass option


# Attack: Grow my Power to that of the strongest equipped ally this round.
def NoxianDefector():
    value = EntityAttribute(
        target=CardFilterSelector(
            flags=CardFlags.IS_EQUIPPED, sort_by=CardSorter.STRONGEST
        ),
        attribute=AttrEnum.ATTACK,
    )
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=value,
        operator=Ops_.GROW,
    )
    return Unit(attack_commit_effect=effect)


# Round End: The Strongest enemy and I strike each other.
def NaganekaofZuretta():
    effect = MutualStrikeEffect(
        first_striker=AutoEntitySelector.SELF,
        second_striker=AutoEntitySelector.STRONGEST_OPPONENT_BOARD_UNIT,
    )
    return Unit(round_end_effects=effect)


# When I'm summoned, I Improvise.
def IonianHookmaster():
    effect = ImproviseEffect()
    return Unit(summon_effect=effect)


# When I'm summoned, I Improvise.
def FirethReaperoftheSands():
    effect = ImproviseEffect()
    return Unit(summon_effect=effect)


# The first time I'm Equipped grant me +2|+2.
def Darkinthrall():
    effect1 = BuffEffect(target=AutoEntitySelector.SELF, attack=2, health=2)
    effect = TriggeredAction(
        event=EntityEvents.IS_EQUIPPED_WITH,
        activate_once=True,
        ally_enum=OriginEnum.T_SELF,
        action=effect1,
    )
    return Unit(effects=effect)


# To play me, kill an ally.Last Breath: Create a The Darkin Bloodletters in hand.
def Xolaani():
    effect1 = KillAction(target=TargetShorthand.ALLIED_BOARD_UNIT)
    effect2 = CreateCardEffect(target=Set6Equipments.TheDarkinBloodletters)
    return Unit(last_breath_effect=effect2, play_requisite=effect1)


def ForsakenBaccaiCondition(origin, gamestate, event):
    target = event.target
    value = CardFlags.IS_EQUIPMENT.resolve(target)
    value1 = CardFlags.IS_SUBTYPE_X.resolve(target, SubTypes_.DARKIN)
    return value or value1


# Play: Predict. If you pick a Darkin or an equipment, grant me +1|+1.
def ForsakenBaccai():
    effect = PredictEffect()
    effect1 = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=1,
        health=1,
        condition=ForsakenBaccaiCondition,
    )
    # TOIMP custom condition
    return Unit(play_effect=(effect, effect1))


# Once you've Equipped an ally this game, grant me Lifesteal.
def KeeperoftheBox():
    effect = AddKeywordEffect(
        target=AutoEntitySelector,
        keyword=KeywordEnum.LIFESTEAL,
    )
    effect1 = OnceYouve(state=PlayerFlags.HAS_EQUIPPED_ALLY_THIS_GAME, action=effect)
    return Unit(effects=effect1)


# Support: Grow my supported ally's stats to mine. Give it my positive KeywordEnum this round.
def Horazi():
    effect = SupportEffect(
        attack=EntityAttribute(
            target=AutoEntitySelector.SELF, attribute=AttrEnum.ATTACK
        ),
        health=EntityAttribute(
            target=AutoEntitySelector.SELF, attribute=AttrEnum.HEALTH
        ),
        round_only=True,
        operator=Ops_.GROW,
    )
    effect1 = CopyKeywords(
        target=PostEventParam.TARGET,
        source=AutoEntitySelector.SELF,
        round_only=True,
    )
    return Unit(support_effect=(effect, effect1))


def TaaroshEffect():
    target_obj = EventQuery()
    effect2 = CreateCardEffect(
        target=TargetEntity(entity_pool=target_obj, sort_by=CardSorter.STRONGEST)
    )


# Each round, the first time I attack, fill your attackers with revived Ephemeral copies
# of the strongest followers you've slain this game.
def Taarosh():
    effect3 = TriggeredAction(
        event=EntityEvents.ATTACK_COMMIT,
        activations_per_round=1,
        ally_enum=OriginEnum.T_SELF,
        action=...,
    )
    return Unit(effects=effect3)


#
def IcathianMirage():
    pass


# When I'm summoned, summon a random Husk.
def Steem():
    effect = SummonHuskEffect()
    return Unit(summon_effect=effect)


# Other allies and your Nexus have Tough.
def LordEldredMageseekerLeader():
    effect = DynamicKeywordModifier(
        value=KeywordEnum.TOUGH,
        target=EntityFilter(exclude_origin=True, player=TargetPlayer.ORIGIN_OWNER),
    )
    return Unit(effects=effect)


# When another ally gets Barrier, give me Barrier this round if I don't have it.
def KinkouStudent():
    effect = AddKeywordEffect(
        target=AutoEntitySelector.SELF,
        keyword=KeywordEnum.BARRIER,
    )
    condition1 = PostEventAttributeCondition(
        attribute=PostEventParam.VALUE, parameter=KeywordEnum.BARRIER
    )
    condition = Condition(
        target=AutoEntitySelector.SELF,
        condition=CardFlags.HAS_KEYWORD,
        invert_result=True,
        parameter=KeywordEnum.BARRIER,
    )
    effect1 = TriggeredAction(
        event_filter=EntityEvents.ADD_KEYWORD,
        condition=(condition1, condition),
        action=effect,
        ally_enum=OriginEnum.T_ALLY,
    )
    return Unit(effect=effect1)


# My Fated buffs are granted to allied Starhound Packs everywhere.
def StarhoundPack():
    effect = BuffEverywhereEffect(
        filter_obj=BaseCardFilter(card_type=StarhoundPack), attack=...
    )

    pass
    # TODO wtf


# Daybreak: Give other allies +0|+2 this round.
def SolariStellacorn():
    effect = HealEffect(
        target=CardFilter(exclude_origin=True),
        value=3,
    )
    return Unit(play_daybreak=effect)


# Reputation: I cost 3.
def CaptiveYeti():
    effect = DynamicCostModifier(
        value=3, operator=Ops_.SET, condition=PlayerFlags.REPUTATION
    )
    return Unit(effects=effect)


# When I'm summoned, summon a random Husk.
# When you summon a 1 cost ally, grant it a random keyword.
def Solitude():
    effect = SummonHuskEffect()
    action = AddRandomKeywordEffect(target=PostEventParam.TARGET)
    effect1 = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        action=action,
        condition=...,
    )
    return Unit(summon_effect=effect, effects=effect1)


# Play: Pick a card in hand.
# Create 4 exact copies of it in your deck and reduce their costs by 1.
def EvilImperfectionist():
    effect1 = TargetEntity(choices=TargetShorthand.ALLIED_HAND_CARD)
    effect = CreateExactCopyEffect(
        target=effect1,
        location=LocEnum.DECK,
        quantity=4,
        cost=(Ops_.DECREMENT, 1),
    )
    return Unit(play_effect=(effect1, effect))


def VoidlingRandomEffect(origin):
    # TODO randomizer,
    value = ...
    effect = SetAttribute(
        target=origin,
        attribute=AttrEnum.INTERNAL_VALUE,
        value=value,
    )
    return effect


def VoidlingSummonEffect(origin):
    keyword = EntityAttribute(
        target=AutoEntitySelector.SELF, attribute=AttrEnum.INTERNAL_VALUE
    )
    effect1 = AddKeywordEffect(target=origin, keyword=keyword)
    return effect1


# While in hand, I have a random keyword that changes each round.
# When I'm summoned, grant me this keyword.
def Voidling():
    ta = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START,
        action=VoidlingRandomEffect,
        location=LocEnum.HAND,
    )
    return Unit(effects=ta, summon_effect=VoidlingSummonEffect)


def VoidAbominationEffect(origin):
    value = PlayerStatisticList.KEYWORDS_ALLIES_GAINED.resolve()
    effect = AddKeywordEffect(
        target=origin,
        keyword=value,
    )
    return effect

def VoidAbominationCondition(origin):
    return 


# When I'm summoned, grant me all positive keyword allies have had this game.
# When I see an ally with a new positive keyword, grant it to me.
def VoidAbomination():
    effect3 = AddKeywordEffect(
        target=AutoEntitySelector.SELF,
        keyword=PostEventParam.VALUE,
    )
    effect2 = TriggeredAction(
        event=EntityEvents.ADD_KEYWORD,
        ally_enum=OriginEnum.T_ALLY,
        action=effect3,
        condition=VoidAbominationCondition
    )
    return Unit(summon_effect=VoidAbominationEffect, effects=effect2)


def HiveHeraldEffect(BaseTarget):
    ...


# Play: Grant a unit and me each other's positive KeywordEnum.
def HiveHerald():
    # TODO targeting
    target_obj = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = CopyKeywords(target=AutoEntitySelector.SELF, source=target_obj)
    ...
    return Unit(play_effect=HiveHeraldEffect)


# When I'm summoned, summon a random Husk.
# When you summon a 1 cost ally, grant it +1|+0.
def Domination():
    effect = SummonHuskEffect()
    effect1 = BuffEffect(
        target=PostEventParam.TARGET,
        attack=1,
    )
    effect2 = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        action=effect1,
        condition=...,
    )
    return Unit(summon_effect=effect, effects=effect2)


def EternalDancersEffect(origin):
    upper = origin.attack
    effect = CreateCardEffect(
        target=CardFilterSelector(
            location=LocEnum.GRAVEYARD,
            sort_by=CardSorter.STRONGEST,
            exclude_card_class=EternalDancers,
        ),
        attack=(0, upper),
        location=LocEnum.BATTLEFIELD,
        is_ephemeral=True,
    )
    return effect


# Attack: Revive an attacking Ephemeral copy of the  strongest dead ally
# other than Eternal Dancers with my power or less.
def EternalDancers():
    return Unit(attack_commit_effect=EternalDancersEffect)


# When I'm summoned,  summon a random Husk.
def Vora():
    effect = SummonHuskEffect()
    return Unit(summon_effect=effect)


# When I'm summoned, summon a random Husk.
def Sultur():
    effect = SummonHuskEffect()
    return Unit(summon_effect=effect)


# Last Breath: Create a Ghastly Band in hand.
def ConductorOfTheMists():
    effect = CreateCardEffect(target=GhastlyBand)
    return Unit(last_breath_effect=effect)


#
def PhantomButler():
    pass


#
def BelvethiElder():
    pass


#
def GhastlyBand():
    pass


#
def GhostlyParamour():
    pass


#
def BoisterousHost():
    pass


# Nexus Strike: Reduce the cost of the most expensive spell in your hand by 1.
def AcorntheHextechnician():
    effect = BuffCostEffect(
        target=CardFilter(
            location=LocEnum.HAND,
            type=Types_.SPELL,
            sorter=CardSorter.EXPENSIVEST,
        ),
        value=1,
    )
    return Unit(nexus_strike_effect=effect)


# Once you've Equipped an ally this game,
# create a new spell that costs 2 in hand and set its cost to 0.
def AmbitiousCultist():
    action = CreateCardEffect(
        target=BaseCardFilter(
            type=Types_.SPELL,
            cost=2,
            is_new=True,
        ),
        cost=0,
    )
    effect = OnceYouve(action=action, state=PlayerFlags.HAS_EQUIPPED_ALLY_THIS_GAME)
    return Unit(effects=effect)


# HERE


# Play: Equip me with an equipment that costs 2 or less from hand.
# The first time I would die while Equipped, fully heal me and destroy the equipment instead.
def BloodcursedHarpy():
    equip_target = TargetEntity(
        choices=CardFilter(
            type=Types_.EQUIPMENT,
            cost=(0, 2),
            location=LocEnum.HAND,
        )
    )
    action = EquipEffect(
        equipment=equip_target,
        target=AutoEntitySelector.SELF,
    )
    heal = HealEffect(target=AutoEntitySelector.SELF, heal_max=True)
    destroy = DestroyEquipEffect(target=AutoEntitySelector.EQUIPMENT)
    effect = TriggeredAction(
        event=EntityEvents.DIE,
        activate_once=True,
        action=(heal, destroy),
        ally_enum=OriginEnum.T_SELF,
        condition=CardFlags.IS_EQUIPPED,
    )
    return Unit(play_effect=action, effects=effect)


# Once you've Equipped an ally this game, grant me Elusive.
def BloomingCultist():
    action = AddKeywordEffect(
        target=AutoEntitySelector.SELF,
        keyword=KeywordEnum.ELUSIVE,
    )
    effect = TriggeredAction(
        action=action,
        activate_once=True,
        event_filter=EntityEvents.IS_EQUIPPED_WITH,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
    )
    return Unit(effects=effect)


# When Equipped allies attack, deal 1 to the enemy nexus.
def BuhruCultist():
    effect = PlaySkill(target=Set6Skills.PiercingBolt)
    ta = TriggeredAction(
        event_filter=EntityEvents.PLAYER_ATTACK_COMMIT,
        ally_enum=OriginEnum.T_ALLY,
        action=effect,
    )
    return Unit(effects=ta)


# Play: I strike an enemy.
def CamouflagedHorror():
    effect = PlaySkill(target=Set6Skills.FeedtheVoid)
    return Unit(play_effect=effect)


# Round Start: Flow: Summon a The Empyrean and grant it Ephemeral.
def Dragoncaller():
    effect = CreateCardEffect(
        target=Set6Units,
        location=LocEnum.HOMEBASE,
        is_ephemeral=True,
    )
    effect1 = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START,
        condition=PlayerFlags.FLOW,
        action=effect,
    )
    return Unit(effects=effect1)


# If an ally died this round, I cost 2 less.
# Play: Equip me with an equipment that costs 2 or less from hand.
def FaithfulWolfdog():
    equip_target = TargetEntity(
        choices=CardFilter(type=Types_.EQUIPMENT, cost=(0, 2), location=LocEnum.HAND)
    )
    effect2 = EquipEffect(
        equipment=equip_target,
        target=AutoEntitySelector.SELF,
    )
    effect = DynamicCostModifier(value=2, condition=PlayerFlags.ALLY_DIED_THIS_ROUND)
    return Unit(play_effect=effect2, effects=effect)


# Play: Manifest a spell that costs 5 and set its cost to 2.
def FanclubPresident():
    effect = ManifestEffect(
        target=ManifestBaseCardFilter(type=Types_.SPELL, cost=5), cost=2
    )
    return Unit(play_effect=effect)


# I have +1|+1 for each card you've drawn this game.
# I can only be blocked by enemies with 4 or more Power.
def Ibaaros():
    # TODO dynamic
    effect = DynamicAtkHPModifier(
        attack=PlayerStatistic.CARD_DREW_THIS_GAME,
        health=PlayerStatistic.CARD_DREW_THIS_GAME,
    )
    effect1 = ActionNegator(
        event_filter=EntityEvents.BLOCK,
        ally_enum=OriginEnum.T_OPPO_O_OPPO,
        condition=Condition(
            target=PostEventParam.TARGET,
            condition=CardFlags.ATTACK_REACHES_AMOUNT,
            parameter=4,
        ),
    )
    return Unit(effects=(effect, effect1))


# Your Equipped allies have Overwhelm.
def IcevaleCultist():
    effect = DynamicKeywordModifier(
        value=KeywordEnum.OVERWHELM,
        target=CardFilter(flags=CardFlags.IS_EQUIPPED),
    )
    return Unit(effects=effect)


# Your opponent's spells cost 2 more while I am attacking.
def Joraal():
    effect = DynamicCostModifier(
        value=2,
        operator=Ops_.INCREMENT,
        target=CardFilter(location=LocEnum.HAND, type=Types_.SPELL),
        origin_location=LocEnum.BATTLEFIELD,
    )
    return Unit(effects=effect)


# When I'm summoned, give Equipped allies Barrier this round.
def KindheartedRecruit():
    effect = AddKeywordEffect(
        keyword=KeywordEnum.BARRIER,
        target=CardFilter(flags=CardFlags.IS_EQUIPPED),
    )
    return Unit(summon_effect=effect)


# When I'm summoned or once you've Equipped an ally this game, create a Gem in hand.
def LunariCultist():
    effect = CreateCardEffect(target=Set3Spells.Gem)
    effect1 = OnceYouve(
        state=PlayerFlags.HAS_EQUIPPED_ALLY_THIS_GAME,
        action=effect,
    )
    return Unit(effects=effect1, summon_effect=effect)


# When you summon an Ephemeral ally, grant it +1|+0.
# Nightfall: Summon a Sapling.
def MoonlitGlenkeeper():
    condition = Condition(
        target=PostEventParam.TARGET,
        condition=CardFlags.HAS_KEYWORD,
        parameter=KeywordEnum.EPHEMERAL,
    )
    effect1 = BuffEffect(target=PostEventParam.TARGET, attack=1)
    effect2 = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_ALLY,
        action=effect1,
        condition=condition,
    )
    effect = CreateCardEffect(target=Set2Units.Sapling)
    return Unit(effects=effect2, play_nightfall=effect)


# When I'm summoned, Reforge.
def RuneSquire():
    effect = ReforgeEffect()
    return Unit(summon_effect=effect)


# The first time I see an ally Equipped, grant me Tough.
def SteadfastElkin():
    action = AddKeywordEffect(target=AutoEntitySelector.SELF, keyword=KeywordEnum.TOUGH)
    effect = TriggeredAction(
        action=action,
        event_filter=EntityEvents.IS_EQUIPPED_WITH,
        ally_enum=OriginEnum.T_ALLY,
        activate_once=True,
    )
    return Unit(effects=effect)


# Attack: Draw 2, then reduce those cards' costs by 2.
def Styraatu():
    effect = DrawEffect(quantity=2, cost_reduction=2)
    return Unit(attack_commit_effect=effect)


# Flow: I cost 2 less.
# When I'm summoned, draw a spell.
def TheSpiritofWuju():
    effect4 = DynamicCostModifier(value=2, condition=PlayerFlags.FLOW)
    effect = DrawEffect(filter_obj=DrawCardFilter(type=Types_.SPELL))
    return Unit(summon_effect=effect, effects=effect4)


# Flow: I cost 2 less.
# Play: Stun an enemy.
def TheWitness():
    effect = DynamicCostModifier(value=2, condition=PlayerFlags.FLOW)
    effect = PlaySkill(target=Set6Skills.ScintillatingArtifact)
    return Unit(play_effect=effect)


# Play: Deal 1 to all enemies. If you've played 6+ new spells this game, deal 3 instead.
def TheZaunDiva():
    effect = PlaySkill(target=Set6Skills.FatalEncore)
    return Unit(play_effect=effect)


# Daybreak: Give Daybreak allies +1|+1 this round.
# Nightfall: Grant Nightfall allies +1|+0.
def TwilitProtector():
    effect = BuffEffect(
        target=CardFilter(flags=CardFlags.HAS_DAYBREAK),
        attack=1,
        health=1,
        round_only=True,
    )
    effect1 = BuffEffect(
        target=CardFilter(flags=CardFlags.HAS_NIGHTFALL),
        attack=1,
        health=0,
    )
    return Unit(play_nightfall=effect1, play_daybreak=effect)


def WardenoftheTribesEffect(origin: CardArchetype):
    val = PlayerStatistic.UNIQUE_SUBTYPES_SUMMONED
    effect = BuffEffect(target=CardFilter(), attack=val, health=val)
    return effect


# When I'm summoned, grant allies +1|+1 for each different subtype you�ve summoned this game.
def WardenoftheTribes():
    return Unit(summon_effect=WardenoftheTribesEffect)


# Play: Equip me with an equipment that costs 2 or less from hand.
def WidowedHuntress():
    equip_target = TargetEntity(
        choices=CardFilter(
            type=Types_.EQUIPMENT,
            cost=(0, 2),
            location=LocEnum.HAND,
        ),
        message="Select equipment.",
    )
    effect2 = EquipEffect(equipment=equip_target, target=AutoEntitySelector.SELF)
    return Unit(play_effect=effect2, cardcode="06DE019")


def WraithofEchoesEffect(origin: CardArchetype):
    dead = PlayerStatisticList.ALLIES_DEAD_THIS_ROUND.resolve()
    return [
        BuffEverywhereEffect(
            filter_obj=BaseCardFilter(card_type=card_type), attack=1, health=1
        )
        for card_type in dead
    ]


# Round End: For each ally that died this round, grant all allied copies of it everywhere +1|+1.
def WraithofEchoes():
    return Unit(round_end_effects=WraithofEchoesEffect, cardcode="06SI034")


# Round Start: Flow: Refill 2 spell mana.
def ZaunBouncer():
    effect = RefillSpellMana(value=2)
    effect1 = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START,
        action=effect,
        condition=PlayerFlags.FLOW,
    )
    return Unit(effects=effect1, cardcode="06PZ019")


# Attack: Give Equipped allies +1|+1 this round.
def ZealousRangerKnight():
    effect = BuffEffect(
        target=CardFilter(flags=CardFlags.IS_EQUIPPED),
        attack=1,
        health=1,
        round_only=True,
    )
    return Unit(attack_commit_effect=effect, cardcode="06DE027")
