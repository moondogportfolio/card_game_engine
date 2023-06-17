import Sets.SET3.Units as Set3Units
import Sets.SET3.Spells as Set3Spells
import Sets.SET3.Skills as Set3Skills



from actions.activations.play_skill import PlaySkill
from actions.attribute.buff import BuffEffect
from actions.attribute.heal import HealEffect
from actions.attribute.phase import PhaseMoonWeaponEffect
from actions.champ.level_up import LevelupEffect

from actions.create.create_card import CreateCardEffect
from actions.create.create_hand_cards import ReforgeEffect
from actions.create.invoke import InvokeEffect
from actions.keywords.add_keyword import AddKeywordEffect
from actions.keywords.copy_keywords import CopyKeywords
from actions.meta.create_ta import CreateTriggeredAction
from actions.movement.draw import (
    DrawEffect,
)
from actions.movement.move import MoveEffect
from actions.movement.obliterate import ObliterateEffect
from actions.reactions.action_modifier import ActionModifier
from actions.reactions.action_negator import ActionNegator
from actions.reactions.dynamic_attr_modifier import (
    DynamicCostModifier,
    DynamicKeywordModifier,
)
from actions.reactions.triggered_action import TriggeredAction
from actions.reactions.value_triggered_action import (
    EventCounterEnum,
    ValueTriggeredAction,
)
from card_classes.champion import Champion
from entity_selectors.base_card_filter import (
    InvokeBaseCardFilter,
)
from entity_selectors.card_filter import (
    BeholdingFilter,
    CardFilter,
)
from enums.entity_events import EntityEvents
from enums.keywords import KeywordEnum
from enums.gamestate import GameStateEnums
from enums.operator import Ops_
from enums.origin_enum import OriginEnum
from enums.post_event_param import PostEventParam
from enums.subtypes import SubTypes_
from resolvable_enums.active_cards_selector import TargetShorthand
from resolvable_enums.auto_card_selector import AutoEntitySelector
from resolvable_enums.card_conditions import CardFlags
from resolvable_enums.player_conditions import PlayerFlags
from resolvable_enums.target_player import TargetPlayer
from value.card_counter import CardCounter


def AurelionSol():
    effect = InvokeEffect(choices=InvokeBaseCardFilter(cost=(7, 0)))
    create = CreateCardEffect(target=InvokeBaseCardFilter(quantity=1))
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=AurelionSol2)
    ta = TriggeredAction(
        event_filter=GameStateEnums.ROUND_END, action=levelup, condition=...
    )
    return Champion(
        play_effect=effect,
        round_start_effects=create,
        effects=ta,
        cardcode="01NX006",
        champion_spell=Set3Spells.TheSkiesDescend,
    )


# Play: Invoke a Celestial card that costs 7 or more.
# Round Start: Create a random Celestial card in hand.
# Your Celestial cards cost 0.
def AurelionSol2():
    effect = InvokeEffect(choices=InvokeBaseCardFilter(cost=(7, 0)))
    create = CreateCardEffect(target=InvokeBaseCardFilter(quantity=1))
    val = DynamicCostModifier(value=0, target=CardFilter(), operator=Ops_.SET)
    return Champion(
        play_effect=effect,
        round_start_effects=create,
        effects=val,
        cardcode="01NX006T1",
        champion_spell=Set3Spells.TheSkiesDescend,
    )


def Trundle():
    effect = CreateCardEffect(Set3Units.IcePillar)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Trundle2)
    ta = TriggeredAction(
        event_filter=EntityEvents.PLAY,
        action=levelup,
        condition=...,
        ally_enum=OriginEnum.T_ALLY,
    )
    return Champion(
        summon_effect=effect,
        effects=ta,
        cardcode="03FR006",
        champion_spell=Set3Spells.Icequake,
    )


# When I'm summoned, create an Ice Pillar in hand.
# Attack: Grant me +1|+0 for each 8+ cost card you Behold.
def Trundle2():
    effect = CreateCardEffect(Set3Units.IcePillar)
    val = CardCounter(BeholdingFilter(cost=(8, 0)))
    # TODO foreach
    effect1 = BuffEffect(target=AutoEntitySelector.SELF, attack=val)
    return Champion(
        summon_effect=effect,
        effects=effect1,
        cardcode="03MT009",
        champion_spell=Set3Spells.Icequake,
    )


def Zoe():
    ta = TriggeredAction


# When I level up, grant your Nexus "When you summon an ally, grant its keywords to all allies."
# Nexus Strike: Create a Behold the Infinite that costs 0 in hand.
def Zoe2():
    create = CreateCardEffect(target=Set3Spells.BeholdtheInfinite, cost=0)
    keyword = CopyKeywords()
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=keyword,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
    )
    create_ta = CreateTriggeredAction(
        triggered_action=ta, target=TargetPlayer.ORIGIN_OWNER
    )
    ta1 = TriggeredAction(
        event_filter=EntityEvents.LEVEL_UP,
        action=create_ta,
        activate_once=True,
        ally_enum=OriginEnum.T_SELF,
    )
    return Champion(
        nexus_strike_effect=create,
        effects=ta1,
        cardcode="03MT009T1",
        champion_spell=Set3Spells.SleepyTroubleBubble,
    )
    #TODO


# Nightfall or when you activate another Nightfall: Give me +2|+0 and Challenger this round.
def Diana():
    add_keyword = AddKeywordEffect(
        AutoEntitySelector.SELF, KeywordEnum.CHALLENGER, True
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Diana2)
    levelwatcher = ValueTriggeredAction(
        event_filter=EntityEvents.ACTIVATE_NIGHTFALL,
        threshold=4,
        action_on_value=levelup,
        ally_enum=OriginEnum.O_ALLY,
        instance_bound=False,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    ta1 = TriggeredAction(
        event_filter=EntityEvents.ACTIVATE_NIGHTFALL,
        action=add_keyword,
        ally_enum=OriginEnum.T_ALLY,
    )
    # TODO nightfall
    return Champion(
        effects=[ta1, levelwatcher],
        cardcode="03MT056",
        champion_spell=Set3Spells.PaleCascade,
    )


def Diana2():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=2,
        keyword=KeywordEnum.CHALLENGER,
        round_only=True,
    )
    ta1 = TriggeredAction(
        event_filter=EntityEvents.ACTIVATE_NIGHTFALL,
        action=effect,
        ally_enum=OriginEnum.T_ALLY,
    )
    # TODO
    return Champion(
        effects=ta1,
        cardcode="03MT056T1",
        champion_spell=Set3Spells.PaleCascade,
    )


def Lulu():
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Lulu2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.SUPPORT,
        threshold=4,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        instance_bound=False,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    effect = BuffEffect(PostEventParam.TARGET, 4, 4, True, Ops_.GROW)
    return Champion(
        support_effect=effect,
        effects=watcher,
        cardcode="03IO002T1",
        champion_spell=Set3Spells.Whimsy,
    )


# Round Start: Create a Fleeting Help, Pix! in hand.
# Support: My supported ally grows up to 5|5 this round.
def Lulu2():
    effect = BuffEffect(
        PostEventParam.TARGET, 5, 5, round_only=True, operator=Ops_.GROW
    )
    effect1 = CreateCardEffect(Set3Spells.HelpPix, is_fleeting=True)
    return Champion(
        round_start_effects=effect1,
        cardcode="03IO002T1",
        champion_spell=Set3Spells.Whimsy,
    )


def Riven():
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Riven2)
    levelup_ta = TriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL,
        action=levelup,
        condition=...,
        ally_enum=OriginEnum.T_ALLY,
    )
    effect = ReforgeEffect()
    ta1 = TriggeredAction(
        event_filter=EntityEvents.GAIN_ATTACK_TOKEN,
        action=effect,
        ally_enum=OriginEnum.T_ALLY,
    )
    ta2 = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
        condition=...,
    )
    return Champion(
        effects=[levelup_ta, ta1, ta2],
        cardcode="03NX007",
        champion_spell=Set3Spells.WeaponHilt,
    )


# When I'm summoned, if you have the attack token, or when you gain the attack token, Reforge.
# Each round, the first time you increase my Power, increase it by twice the amount.
def Riven2():
    effect = ReforgeEffect()
    ta1 = TriggeredAction(
        event_filter=EntityEvents.GAIN_ATTACK_TOKEN,
        action=effect,
        ally_enum=OriginEnum.T_ALLY,
    )
    ta2 = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
        condition=...,
    )
    ta3 = ActionModifier(
        event_filter=EntityEvents.SET_ATTRIBUTE,
        operator=Ops_.MULTIPLY,
        value=2,
        parameter=...,
        ally_enum=OriginEnum.T_SELF,
        condition=...,
    )
    return Champion(
        effects=[ta3, ta1, ta2],
        cardcode="03NX007T1",
        champion_spell=Set3Spells.WeaponHilt,
    )


def Soraka():
    effect = HealEffect()
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Soraka2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.HEAL,
        threshold=4,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        instance_bound=False,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    # TODO supp
    return Champion(
        effects=watcher,
        cardcode="03MT055",
        champion_spell=Set3Spells.Wish,
    )


# The first time you heal a damaged ally each round, draw 1.
# Support: Fully heal me and my supported ally.
def Soraka2():
    effect = DrawEffect()
    ta2 = TriggeredAction(
        event_filter=EntityEvents.HEAL,
        action=effect,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        activations_per_round=1,
        condition=...,
    )
    # TODO
    return Champion(
        effects=ta2,
        cardcode="03MT055T1",
        champion_spell=Set3Spells.Wish,
    )


# Your created cards cost 1 less.
# When I'm summoned or Round Start: Create a Hex Core Upgrade in hand.
def Viktor():
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Viktor2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.PLAY,
        threshold=7,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        condition=...,
        instance_bound=False,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    effect = CreateCardEffect(Set3Spells.HexCoreUpgrade)
    return Champion(
        effects=watcher,
        summon_effect=effect,
        round_start_effects=effect,
        cardcode="03PZ003",
        champion_spell=Set3Spells,
    )


def Viktor2():
    effect = CreateCardEffect(Set3Spells.HexCoreUpgrade)
    effect1 = DynamicCostModifier(
        value=1, target=CardFilter(flags=CardFlags.IS_CREATED)
    )
    return Champion(
        effects=effect1,
        summon_effect=effect,
        round_start_effects=effect,
        cardcode="03PZ003T1",
        champion_spell=Set3Spells,
    )


def Shyvana():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF, attack=1, health=1, round_only=True
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Shyvana2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.DAMAGE,
        threshold=16,
        action_on_value=levelup,
        ally_enum=OriginEnum.O_ALLY,
        condition=...,
        event_counter=EventCounterEnum.COUNT_VALUE,
    )
    return Champion(
        effects=watcher,
        attack_commit_effect=effect,
        cardcode="02FR002T3",
        champion_spell=Set3Spells.Confront,
    )


# Attack: Give me +1|+1 this round.
def Shyvana2():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF, attack=2, health=2, round_only=True
    )
    create = CreateCardEffect(target=Set3Spells.StrafingStrike, is_fleeting=True)
    return Champion(
        attack_commit_effect=[effect, create],
        cardcode="02FR002T3",
        champion_spell=Set3Spells.StrafingStrike,
    )


# Support: My supported ally and I can't take damage or die this round.
# Copy the last spell you cast on only me this round onto that ally (It can't be copied again).
def Taric():
    effect = AddKeywordEffect(
        target=[PostEventParam.TARGET, AutoEntitySelector.SELF],
        keyword=KeywordEnum.TOUGH,
        round_only=True,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Taric2)
    watcher = ValueTriggeredAction(
        event_filter=[EntityEvents.TARGETED, EntityEvents.SUPPORT],
        threshold=7,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    # TODO multi filter
    return Champion(
        effects=watcher,
        support_effect=effect,
        cardcode="03MT058T1",
        champion_spell=Set3Spells.StrafingStrike,
    )


def Taric2():
    effect2 = ActionNegator(
        event_filter=EntityEvents.DIE, round_only=True, ally_enum=OriginEnum.T_SELF
    )
    effect = CreateTriggeredAction(
        triggered_action=effect2, target=AutoEntitySelector.SELF
    )
    effect1 = CreateTriggeredAction(
        triggered_action=effect2, target=PostEventParam.TARGET
    )
    # TODO
    return Champion(
        support_effect=[effect, effect1],
        cardcode="03MT058",
        champion_spell=Set3Spells.BlessingofTargon,
    )


TahmEffect1 = ObliterateEffect(target=...)
TahmEffect2 = MoveEffect(target=..., destination=...,)
TahmTA = TriggeredAction(
    event_filter=EntityEvents.LEVEL_UP,
    ally_enum=OriginEnum.T_SELF,
    action=[TahmEffect1, TahmEffect2],
)


def TahmKench():
    effect = CreateCardEffect(Set3Spells.AnAcquiredTaste)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=TahmKench2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.CAPTURE,
        threshold=3,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_OPPO,
        condition=...,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(
        effects=(watcher, TahmTA),
        round_start_effects=effect,
        summon_effect=effect,
        cardcode="03MT058",
        champion_spell=Set3Spells.BayouBrunch,
    )


# Round Start: Create an An Acquired Taste in hand.
# Attack: Obliterate my Captured enemies and release my allies.
def TahmKench2():
    effect = CreateCardEffect(Set3Spells.AnAcquiredTaste)
    return Champion(
        round_start_effects=effect,
        summon_effect=effect,
        attack_commit_effect=(TahmEffect1, TahmEffect2),
        cardcode="03MT058",
        champion_spell=Set3Spells.BayouBrunch,
    )


def Leona():
    play = PlaySkill(target=Set3Skills.SolarFlare, condition=PlayerFlags.DAYBREAK)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Leona2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.ACTIVATE_DAYBREAK,
        threshold=4,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(
        play_effect=play,
        effects=watcher,
        cardcode="03MT054",
        champion_spell=Set3Spells.MorningLight,
    )


# Daybreak or when you activate another Daybreak: Stun the strongest enemy.
def Leona2():
    play = PlaySkill(target=Set3Skills.SolarFlare, condition=PlayerFlags.DAYBREAK)
    effect = AddKeywordEffect(
        target=AutoEntitySelector.SELF, keyword=KeywordEnum.BARRIER
    )
    watcher = TriggeredAction(
        event_filter=EntityEvents.ACTIVATE_DAYBREAK,
        action=(play, effect),
        ally_enum=OriginEnum.T_ALLY,
    )
    return Champion(
        play_effect=play,
        effects=watcher,
        cardcode="03MT054T1",
        champion_spell=Set3Spells.MorningLight,
    )


# Nightfall: Grant an enemy Vulnerable and give enemies -1|-0 this round.
# Other allies have Fearsome.
# When you play a unit, give enemies -1|-0 this round.
def Nocturne():
    effect = AddKeywordEffect(
        TargetShorthand.OPPONENT_BOARD_UNIT,
        KeywordEnum.VULNERABLE,
        round_only=True,
        condition=PlayerFlags.NIGHTFALL,
    )
    effect2 = BuffEffect(
        AutoEntitySelector.ALL_OPPONENT_UNITS,
        -1,
        0,
        round_only=True,
        condition=PlayerFlags.NIGHTFALL,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Nocturne2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.PLAYER_ATTACK_COMMIT,
        threshold=5,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        event_counter=...,
    )
    return Champion(
        play_effect=[effect, effect2],
        effects=watcher,
        cardcode="03MT054",
        champion_spell=Set3Spells.UnspeakableHorror,
    )


def Nocturne2():
    effect = AddKeywordEffect(
        TargetShorthand.OPPONENT_BOARD_UNIT,
        KeywordEnum.VULNERABLE,
        round_only=True,
        condition=PlayerFlags.NIGHTFALL,
    )
    effect2 = BuffEffect(
        AutoEntitySelector.ALL_OPPONENT_UNITS,
        -1,
        0,
        round_only=True,
        condition=PlayerFlags.NIGHTFALL,
    )
    # TODO exclude this instance
    effect3 = BuffEffect(
        AutoEntitySelector.ALL_OPPONENT_UNITS,
        -1,
        0,
        round_only=True,
    )
    dynamic = DynamicKeywordModifier(value=KeywordEnum.FEARSOME, target=CardFilter())
    watcher = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect3,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
    )
    return Champion(
        play_effect=[effect, effect2],
        effects=[watcher, dynamic],
        cardcode="03MT054T1",
        champion_spell=Set3Spells.UnspeakableHorror,
    )


# Nightfall: Pick a Moon Weapon to create in hand.
# Each round, the first time you play 2 other cards or Round Start:
# Create the Phased Moon Weapon in hand if you don't already have one.
# Your Moon Weapons cost 1 less.
def Aphelios():
    effect = PhaseMoonWeaponEffect(target=..., condition=PlayerFlags.NIGHTFALL)
    create = CreateCardEffect(
        target=...,
    )
    effect1 = ValueTriggeredAction(
        event_filter=EntityEvents.PLAY,
        activations_per_round=1,
        action_on_value=create,
        condition=...,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        round_end_reset=True
    )
    effect2 = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START, action=create, condition=...
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Aphelios2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL,
        threshold=4,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        condition=...,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
        instance_bound=False,
    )
    return Champion(
        play_effect=effect,
        effects=[watcher, effect1, effect2],
        cardcode="03MT217",
        champion_spell=Set3Spells.GiftsFromBeyond,
    )


def Aphelios2():
    effect = PhaseMoonWeaponEffect(target=..., condition=PlayerFlags.NIGHTFALL)
    create = CreateCardEffect(
        target=...,
    )
    effect1 = TriggeredAction(
        event_filter=create, activations_per_round=1, action=..., condition=...
    )
    effect2 = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START, action=create, condition=...
    )
    dynamic = DynamicCostModifier(
        value=1, target=CardFilter(location=None, type=SubTypes_.MOONCARD)
    )
    return Champion(
        play_effect=effect,
        effects=[dynamic, effect1, effect2],
        cardcode="03MT217T13",
        champion_spell=Set3Spells.GiftsFromBeyond,
    )
