from actions.activations.multiple_activations import MultipleActivationsEffect
from actions.activations.play_skill import PlaySkill
from actions.activations.recast_spell import RecastEventOfAction
from actions.attachments.autoequip import AutoEquipEffect
from actions.attachments.equip import EquipEffect
from actions.attachments.forge import ForgeEffect
from actions.attribute.buff import BuffCostEffect, BuffEffect
from actions.attribute.buff_everywhere import BuffEverywhereEffect
from actions.attribute.damage import DamageEffect
from actions.attribute.frostbite import FrostbiteEffect
from actions.attribute.heal import HealEffect
from actions.attribute.rally import RallyEffect
from actions.attribute.support import SupportEffect
from actions.branching.branching_action import BranchingAction
from actions.champ.level_up import LevelupEffect
from actions.common.strike import StrikeEffect
from actions.create.create_card import CreateCardEffect
from actions.create.summon_specific_cards import SpawnEffect, SummonHuskEffect
from actions.keywords.add_keyword import AddKeywordEffect, AddRandomKeywordEffect
from actions.keywords.copy_keywords import CopyKeywords
from actions.meta.create_dynamic_value import CreateDynamicValue
from actions.movement.draw import DrawEffect
from actions.movement.move import MoveEffect
from actions.movement.recall import RecallEffect
from actions.movement.revive import ReviveEffect
from actions.movement.summon import SummonEffect
from actions.movement.swap import SwapPositionsEffect
from actions.reactions.action_modifier import ActionModifier
from actions.reactions.action_negator import ActionNegator
from actions.reactions.action_replacement import ActionReplacement
from actions.reactions.dynamic_attr_modifier import (
    DynamicAttackModifier,
    DynamicKeywordModifier,
)
from actions.reactions.state_triggered_action import StateTriggeredAction
from actions.reactions.triggered_action import TriggeredAction
from actions.reactions.value_triggered_action import (
    EventCounterEnum,
    ValueTriggeredAction,
)
from actions.transform.transform import TransformEffect
from actions.traps.set_trap import (
    PlantChimes,
    PlantFlashBombTrap,
    PlantMysteriousPortalEffect,
    PlantPuffcaps,
    TrapMultiplier,
)
from actions.win.win_con import DeclareGameResult
from card_classes.champion import Champion
from card_classes.unit import Unit
from conditions.base_condition import Condition
from entity_selectors.base_card_filter import BaseCardFilter
from entity_selectors.card_filter import CardFilter
from entity_selectors.input import ChoiceBaseCard, ChoiceValue
from enums.attribute import AttrEnum
from enums.card_sorters import CardSorter
from enums.entity_events import EntityEvents
from enums.gamestate import GameStateEnums
from enums.keywords import KeywordEnum
from enums.location import LocEnum
from enums.operator import Ops_
from enums.origin_enum import OriginEnum
from enums.post_event_param import PostEventParam
from enums.subtypes import SubTypes_
from enums.types import Types_
from resolvable_enums.auto_card_selector import AutoEntitySelector
import Sets.SET1.Spells as Set1Spells
import Sets.SET1.Units as Set1Units
import Sets.SET1.Skills as Set1Skills
from resolvable_enums.card_conditions import CardFlags
from resolvable_enums.player_conditions import PlayerFlags
from resolvable_enums.target_player import TargetPlayer
from value.entity_attribute import EntityAttribute


def Thresh():
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Thresh2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.DIE,
        threshold=6,
        action_on_value=levelup,
        ally_enum=None,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(effects=watcher)


# The first time I attack this game, summon another attacking champion from your deck or hand.
def Thresh2():
    summon = SummonEffect(
        target=CardFilter(is_follower=False, location=(LocEnum.HAND, LocEnum.BOARD))
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.ATTACK_COMMIT,
        ally_enum=OriginEnum.SELF,
        action=summon,
        activate_once=True,
    )
    return Champion(effects=ta, cardcode="01SI052T1")


def Vladimir():
    effect = PlaySkill(target=Set1Skills.CrimsonPact)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Vladimir2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.DAMAGE_SURVIVE,
        threshold=5,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(effects=watcher, attack_commit_effect=effect)


# Attack: For each attacking ally on my right, deal 1 to it and drain 1 from the enemy Nexus.
def Vladimir2():
    effect = PlaySkill(target=Set1Spells.CrimsonPact2)
    return Champion(
        attack_commit_effect=effect,
        cardcode="01NX006T1",
        champion_spell=Set1Spells.Transfusion,
    )


def Eggnivia():
    effect1 = TransformEffect(target=AutoEntitySelector.SELF, new_form=Anivia)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Anivia2)
    watcher = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START,
        condition=PlayerFlags.ENLIGHTENED,
        action=[effect1, levelup],
    )
    return Unit(effects=watcher)


def Anivia():
    effect = PlaySkill(target=Set1Skills.GlacialStorm)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Anivia2)
    watcher = TriggeredAction(
        event_filter=EntityEvents.ACTIVATE_ENLIGHTENED,
        action=levelup,
        ally_enum=OriginEnum.T_ALLY,
    )
    effect1 = TransformEffect(target=AutoEntitySelector.SELF, new_form=Eggnivia)
    effect2 = ReviveEffect(target=AutoEntitySelector.SELF)
    return Champion(
        effects=watcher,
        attack_commit_effect=effect,
        last_breath_effect=[effect1, effect2],
    )


# Attack: Deal 2 to all enemies and the enemy Nexus.
# Last Breath: Revive me transformed into Eggnivia.
def Anivia2():
    effect = PlaySkill(target=Set1Skills.GlacialStorm)
    effect1 = TransformEffect(target=AutoEntitySelector.SELF, new_form=Eggnivia)
    effect2 = ReviveEffect(target=AutoEntitySelector.SELF)
    return Champion(
        attack_commit_effect=effect,
        last_breath_effect=[effect1, effect2],
        champion_spell=Set1Spells.HarshWinds,
        cardcode="01FR024T3",
    )


def Darius():
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Darius2)
    state = StateTriggeredAction(
        action=levelup,
        condition=lambda x, y: y.owner.health <= 10,
        # TODO init health
    )
    return Champion(effects=state)


def Darius2():
    return Champion(champion_spell=Set1Spells.Decimate, cardcode="01NX038T2")


def Hecarim():
    create = CreateCardEffect(
        Set1Units.SpectralRiders, location=LocEnum.BATTLEFIELD, quantity=2
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Hecarim2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.ATTACK_COMMIT,
        threshold=7,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        condition=...,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(attack_commit_effect=create, effects=watcher)


def Hecarim2():
    create = CreateCardEffect(
        Set1Units.SpectralRiders, location=LocEnum.BATTLEFIELD, quantity=2
    )
    dynamic = DynamicAttackModifier(
        value=3, target=CardFilter(keyword=KeywordEnum.EPHEMERAL)
    )
    effect = CreateDynamicValue(target=dynamic, bind_to=TargetPlayer.ORIGIN_OWNER)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.LEVEL_UP,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
        activate_once=True,
    )
    return Champion(
        attack_commit_effect=create,
        effects=ta1,
        cardcode="01SI042T1",
    )


def Tryndamere():
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Tryndamere2)
    ar = ActionReplacement(
        event_filter=EntityEvents.DIE,
        ally_enum=OriginEnum.T_SELF,
        replacement_action=levelup,
        activate_once=True,
    )
    return Champion(effects=ar)


def Tryndamere2():
    return Champion(cardcode="01FR039T2", champion_spell=Set1Spells.BattleFury)


def Teemo():
    trap = PlantPuffcaps(quantity=5)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Teemo2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.ADD_TRAP,
        threshold=15,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_OPPO_O_ALLY,
        condition=...,
        event_counter=EventCounterEnum.COUNT_VALUE,
    )
    return Champion(nexus_strike_effect=trap, effects=watcher)


# Nexus Strike: Double the Poison Puffcaps in the enemy deck.
def Teemo2():
    trap = TrapMultiplier()
    return Champion(
        nexus_strike_effect=trap,
        cardcode="01PZ008T2",
        champion_spell=Set1Spells.MushroomCloud,
    )


# Attack: Summon an attacking Spiderling.
def Elise():
    create = CreateCardEffect(Set1Units.Spiderling, location=LocEnum.BATTLEFIELD)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Elise2)
    condition = Condition(target=TargetPlayer.ORIGIN_OWNER, condition=..., parameter=3)
    ta = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START,
        condition=condition,
        action=levelup,
    )
    return Champion(attack_commit_effect=create, effects=ta)


def Elise2():
    effect = DynamicKeywordModifier(
        value=[KeywordEnum.CHALLENGER, KeywordEnum.FEARSOME],
        target=CardFilter(subtype=SubTypes_.SPIDER),
        # TODO exclude origin
    )
    return Champion(
        effects=effect,
        cardcode="01SI053T2",
        champion_spell=Set1Spells.CrawlingSensation,
    )


def Lucian():
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Lucian2)
    watcher1 = ValueTriggeredAction(
        event_filter=EntityEvents.DIE,
        threshold=4,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    condition = Condition()
    watcher2 = TriggeredAction(
        event_filter=EntityEvents.DIE,
        condition=condition,
        ally_enum=OriginEnum.T_ALLY,
        action=levelup,
    )
    # TODO coNDITION
    return Champion(effects=[watcher1, watcher2])


# Each round, the first time an ally dies, Rally.
def Lucian2():
    effect = RallyEffect()
    ta = TriggeredAction(
        event_filter=EntityEvents.DIE,
        action=effect,
        ally_enum=OriginEnum.T_ALLY,
        activations_per_round=1,
    )
    return Champion(
        effects=effect,
        cardcode="01DE022T1",
        champion_spell=Set1Spells.RelentlessPursuit,
    )


def Draven():
    create = CreateCardEffect(Set1Spells.SpinningAxe)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Draven2)
    watcher1 = ValueTriggeredAction(
        event_filter=EntityEvents.STRIKE,
        threshold=2,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_SELF,
        condition=...,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(strike_effect=create, summon_effect=create, effects=watcher1)


# When I'm summoned or Strike: Create 2 Spinning Axes in hand.
def Draven2():
    create = CreateCardEffect(Set1Spells.SpinningAxe)
    return Champion(
        strike_effect=create,
        summon_effect=create,
        cardcode="01NX020T3",
        champion_spell=Set1Spells.WhirlingDeath,
    )


def Ezreal():
    create = CreateCardEffect(Set1Spells.MysticShot, is_fleeting=True)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Ezreal2)
    watcher1 = ValueTriggeredAction(
        event_filter=EntityEvents.TARGETED,
        threshold=8,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_OPPO,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(nexus_strike_effect=create, effects=watcher1)


# Nexus Strike: Create a Fleeting Mystic Shot in hand.When you cast a spell, deal 1 to the enemy Nexus. If it targeted an enemy, deal 2 to the enemy Nexus instead.


def Ezreal2():
    create = CreateCardEffect(Set1Spells.MysticShot, is_fleeting=True)
    action = DamageEffect(target=TargetPlayer.OPPONENT, value=1)
    watcher1 = TriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL,
        action=action,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
    )
    return Champion(
        nexus_strike_effect=create,
        effects=watcher1,
        cardcode="01PZ036T1",
        champion_spell=Set1Spells.MysticShot,
    )


def Fiora():
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Fiora2)
    watcher1 = ValueTriggeredAction(
        event_filter=EntityEvents.KILL,
        threshold=2,
        action_on_value=levelup,
        condition=...,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(effects=watcher1)


# When I've killed 4 enemies and survived, you win the game.


def Fiora2():
    win = DeclareGameResult(winner=TargetPlayer.ORIGIN_OWNER)
    watcher1 = ValueTriggeredAction(
        event_filter=EntityEvents.KILL,
        threshold=4,
        action_on_value=win,
        condition=...,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(
        effects=watcher1,
        cardcode="01DE045T1",
        champion_spell=Set1Spells.Riposte,
    )


def Kalista():
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Kalista2)
    watcher1 = ValueTriggeredAction(
        event_filter=EntityEvents.DIE,
        threshold=3,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(effects=watcher1)


# Each round, the first time I attack revive an attacking Ephemeral copy of the strongest dead allied follower. This round, we're bonded and it takes damage for me.
def Kalista2():
    effect = ReviveEffect(target=..., destination=LocEnum.BATTLEFIELD)
    watcher1 = TriggeredAction(
        event_filter=EntityEvents.ATTACK_COMMIT,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
        activations_per_round=1,
    )
    return Champion(
        effects=watcher1,
        cardcode="01SI030T2",
        champion_spell=Set1Spells.BlackSpear,
    )


# When I'm summoned, Rally.Strike: Recall me.
def Katarina():
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Katarina2)
    rec = RecallEffect(target=AutoEntitySelector.SELF)
    create = CreateCardEffect(Set1Spells.BladesEdge, is_fleeting=True)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.LEVEL_UP,
        ally_enum=OriginEnum.T_SELF,
        action=rec,
        activate_once=True,
    )
    return Champion(strike_effect=levelup, summon_effect=create, effects=ta1)


def Katarina2():
    create = CreateCardEffect(Set1Spells.BladesEdge, is_fleeting=True, cost=0)
    rec = RecallEffect(target=AutoEntitySelector.SELF)
    rally = RallyEffect()
    return Champion(
        strike_effect=rec,
        summon_effect=[create, rally],
        cardcode="01NX042T2",
        champion_spell=Set1Spells.DeathLotus,
    )


def Zed():
    create = CreateCardEffect(
        Set1Units.LivingShadow,
        location=LocEnum.BATTLEFIELD,
        with_my_stats_source=AutoEntitySelector.SELF,
    )

    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Zed2)
    watcher1 = ValueTriggeredAction(
        event_filter=EntityEvents.NEXUS_STRIKE,
        threshold=2,
        action_on_value=levelup,
        condition=...,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(effects=watcher1, attack_commit_effect=create)


# Attack: Summon an attacking Living Shadow with my stats and positive keywords.


def Zed2():
    create = CreateCardEffect(
        Set1Units.LivingShadow,
        location=LocEnum.BATTLEFIELD,
        with_my_stats_keywords_source=AutoEntitySelector.SELF,
    )
    return Champion(
        attack_commit_effect=create,
        cardcode="01IO009T2",
        champion_spell=Set1Spells.Shadowshift,
    )


def Ashe():
    effect = FrostbiteEffect(target=AutoEntitySelector.STRONGEST_DEAD_ALLY)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Ashe2)
    effect1 = CreateCardEffect(
        target=Set1Spells.CrystalArrow, location=LocEnum.DECK, index=0
    )
    ta1 = TriggeredAction(
        event_filter=EntityEvents.LEVEL_UP,
        ally_enum=OriginEnum.T_SELF,
        action=effect1,
        activate_once=True,
    )
    watcher1 = ValueTriggeredAction(
        event_filter=EntityEvents.SET_ATTRIBUTE,
        threshold=4,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_OPPO_O_ALLY,
        condition=...,
        instance_bound=False,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(attack_commit_effect=effect, effects=[watcher1, ta1])


# Attack: Frostbite the strongest enemy.Enemies with 0 Power can't block.
def Ashe2():
    effect = FrostbiteEffect(target=AutoEntitySelector.STRONGEST_DEAD_ALLY)
    effect1 = ActionNegator(
        event_filter=EntityEvents.BLOCK, condition=..., ally_enum=...
    )
    return Champion(
        attack_commit_effect=effect,
        effects=effect1,
        cardcode="01FR038T2",
        champion_spell=Set1Spells.FlashFreeze,
    )


# Round Start: Rally.
def Garen():
    effect = BuffEffect(target=CardFilter(), exclude_origin=True, attack=1, health=1)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Garen2)
    watcher1 = ValueTriggeredAction(
        event_filter=EntityEvents.STRIKE,
        threshold=2,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_SELF,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(
        summon_effect=effect,
        effects=watcher1,
    )


def Garen2():
    effect = BuffEffect(target=CardFilter(), exclude_origin=True, attack=1, health=1)
    ta1 = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START,
        action=RallyEffect(),
    )
    return Champion(
        summon_effect=effect,
        effects=ta1,
        cardcode="01DE012T1",
        champion_spell=Set1Spells.Judgment,
    )


def Braum():
    effect = CreateCardEffect(Set1Units.MightyPoro, LocEnum.HOMEBASE)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Braum2)
    watcher1 = ValueTriggeredAction(
        event_filter=EntityEvents.DAMAGE_SURVIVE,
        threshold=10,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_SELF,
        event_counter=EventCounterEnum.COUNT_VALUE,
        # TODO
    )
    ta1 = TriggeredAction(
        event_filter=EntityEvents.DAMAGE_SURVIVE,
        action=effect,
        activate_once=True,
        ally_enum=OriginEnum.T_SELF,
    )
    return Champion(effects=[watcher1, ta1])


# When I survive damage, summon a Mighty Poro.


def Braum2():
    effect = CreateCardEffect(Set1Units.MightyPoro, LocEnum.HOMEBASE)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.DAMAGE_SURVIVE,
        action=effect,
        activate_once=True,
        ally_enum=OriginEnum.T_SELF,
    )
    return Champion(
        effects=ta1,
        cardcode="01FR009T1",
        champion_spell=Set1Spells.TakeHeart,
    )


def Yasuo():
    effect = DamageEffect(target=PostEventParam.TARGET, value=2)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.STUN,
        action=effect,
        ally_enum=OriginEnum.T_OPPO_O_ALLY,
    )
    ta2 = TriggeredAction(
        event_filter=EntityEvents.RECALL,
        action=effect,
        ally_enum=OriginEnum.T_OPPO_O_ALLY,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Yasuo2)
    # TODO multiple trigger
    watcher1 = ValueTriggeredAction(
        event_filter=EntityEvents.STUN,
        threshold=5,
        action_on_value=levelup,
        instance_bound=False,
        ally_enum=OriginEnum.T_OPPO_O_ALLY,
        event_counter=EventCounterEnum.COUNT_VALUE,
        # TODO
    )
    return Champion(effects=[ta1, ta2, watcher1])


# When you Stun or Recall an enemy, I strike it.


def Yasuo2():
    effect = StrikeEffect(target=PostEventParam.TARGET, striker=AutoEntitySelector.SELF)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.STUN,
        action=effect,
        ally_enum=OriginEnum.T_OPPO_O_ALLY,
    )
    ta2 = TriggeredAction(
        event_filter=EntityEvents.RECALL,
        action=effect,
        ally_enum=OriginEnum.T_OPPO_O_ALLY,
    )
    return Champion(
        effects=[ta1, ta2],
        cardcode="01IO015T1",
        champion_spell=Set1Spells.SteelTempest,
    )


def Karma():
    effect = CreateCardEffect(
        target=BaseCardFilter(type=Types_.SPELL, owner_same_regions=True)
    )
    ta = TriggeredAction(event_filter=GameStateEnums.ROUND_END, action=effect)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Karma2)
    watcher = TriggeredAction(
        event_filter=EntityEvents.ACTIVATE_ENLIGHTENED,
        action=levelup,
        ally_enum=OriginEnum.T_ALLY,
    )
    return Champion(effects=[ta, watcher])


# When you play a spell, cast it again on the same targets.
def Karma2():
    effect = RecastEventOfAction(target=PostEventParam.TARGET)
    ta = TriggeredAction(
        event_filter=GameStateEnums.ROUND_END,
        action=effect,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
    )
    return Champion(
        effects=ta,
        cardcode="01IO041T1",
        champion_spell=Set1Spells.InsightofAges,
    )


def Lux():
    create = CreateCardEffect(Set1Spells.FinalSpark)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.LEVEL_UP,
        ally_enum=OriginEnum.T_SELF,
        action=create,
        activate_once=True,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Lux2)
    watcher1 = ValueTriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL,
        threshold=6,
        action_on_value=levelup,
        instance_bound=False,
        ally_enum=OriginEnum.T_ALLY,
        event_counter=...,
        # TODO
    )
    return Champion(effects=[ta1, watcher1])


# When you cast 6+ mana of spells, create a Final Spark in hand.


def Lux2():
    create = CreateCardEffect(Set1Spells.FinalSpark)
    watcher1 = ValueTriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL,
        threshold=6,
        action_on_value=create,
        instance_bound=False,
        ally_enum=OriginEnum.T_ALLY,
        event_counter=...,
        # TODO
    )
    return Champion(
        effects=watcher1,
        cardcode="01DE042T2",
        champion_spell=Set1Spells.PrismaticBarrier,
    )


def Jinx():
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Jinx2)
    condition = Condition(
        target=TargetPlayer.ORIGIN_OWNER,
        condition=PlayerFlags.HAS_X_CARDS_ON_Y_LOC,
        parameter=[0, LocEnum.HAND],
    )
    state = StateTriggeredAction(
        action=levelup,
        condition=condition,
    )
    return Champion(effects=state)


# Round Start: Draw 1.Each round, the first time you empty your hand, create a Super Mega Death Rocket! in hand.
def Jinx2():
    create = CreateCardEffect(Set1Spells.SuperMegaDeathRocket)
    draw = DrawEffect()
    watcher = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START,
        action=draw,
    )
    # TODO levelup
    condition = Condition(
        target=TargetPlayer.ORIGIN_OWNER,
        condition=PlayerFlags.HAS_X_CARDS_ON_Y_LOC,
        parameter=[0, LocEnum.HAND],
    )
    state = StateTriggeredAction(
        action=create,
        condition=condition,
    )
    return Champion(
        effects=[watcher, state],
        cardcode="01PZ040T1",
        champion_spell=Set1Spells.GetExcited,
    )


# Support: Give my supported ally Barrier this round.
# When an ally gets Barrier, give it +3|+0 this round.
def Shen():
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Shen2)
    watcher1 = ValueTriggeredAction(
        event_filter=EntityEvents.ADD_KEYWORD,
        threshold=5,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
        
    )
    support = SupportEffect(
        keyword=KeywordEnum.BARRIER
    )
    return Champion(
        effects=watcher1,
        support_effect=support,
        cardcode="01IO032",
        champion_spell=Set1Spells.StandUnited,
    )



def Shen2():
    effect = BuffEffect(target=PostEventParam.TARGET, attack=3, round_only=True)
    watcher1 = TriggeredAction(
        event_filter=EntityEvents.ADD_KEYWORD,
        action=effect,
        condition=...,
        ally_enum=OriginEnum.T_ALLY,
    )
    return Champion(
        effects=watcher1,
        cardcode="01IO032T1",
        champion_spell=Set1Spells.StandUnited,
    )


def Heimerdinger():
    effect = CreateCardEffect(target=PostEventParam.TARGET, cost=0)
    ta = TriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL, ally_enum=OriginEnum.T_ALLY, action=effect
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Heimerdinger2)
    watcher1 = ValueTriggeredAction(
        event_filter=EntityEvents.SUMMON,
        threshold=12,
        action_on_value=levelup,
        instance_bound=False,
        ally_enum=OriginEnum.T_ALLY,
        event_counter=...,
    )
    # TODO value counter
    return Champion(
        effects=[ta, watcher1],
        cardcode="01PZ056T10",
        champion_spell=Set1Spells.ProgressDay,
    )


# When you cast a spell, create a Fleeting Turret in hand with equal cost. Grant it +1|+1 and it costs 0.
def Heimerdinger2():
    effect = CreateCardEffect(
        target=PostEventParam.TARGET,
        cost=0,
        attack=(Ops_.INCREMENT, 1),
        health=(Ops_.DECREMENT, 1),
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL, ally_enum=OriginEnum.T_ALLY, action=effect
    )
    return Champion(
        effects=ta,
        cardcode="01PZ056T10",
        champion_spell=Set1Spells.ProgressDay,
    )
