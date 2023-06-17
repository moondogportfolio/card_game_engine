from actions.activations.multiple_activations import MultipleActivationsEffect
from actions.activations.play_skill import PlaySkill
from actions.activations.recast_spell import RecastEventOfAction
from actions.attachments.autoequip import AutoEquipEffect
from actions.attachments.equip import EquipEffect
from actions.attachments.forge import ForgeEffect
from actions.attribute.buff import BuffCostEffect, BuffEffect
from actions.attribute.buff_everywhere import BuffEverywhereEffect
from actions.attribute.heal import HealEffect
from actions.branching.branching_action import BranchingAction
from actions.champ.level_up import LevelupEffect
from actions.common.strike import StrikeEffect
from actions.create.create_card import CreateCardEffect
from actions.create.summon_specific_cards import SpawnEffect, SummonHuskEffect
from actions.keywords.copy_keywords import CopyKeywords
from actions.movement.recall import RecallEffect
from actions.reactions.action_modifier import ActionModifier
from actions.reactions.dynamic_attr_modifier import DynamicAttackModifier
from actions.reactions.triggered_action import TriggeredAction
from actions.reactions.value_triggered_action import (
    EventCounterEnum,
    ValueTriggeredAction,
)
from actions.transform.transform import TransformEffect
from actions.traps.set_trap import PlantChimes, PlantMysteriousPortalEffect
from card_classes.champion import Champion
from card_classes.unit import Unit
from entity_selectors.base_card_filter import BaseCardFilter
from entity_selectors.card_filter import CardFilter
from entity_selectors.input import ChoiceBaseCard
from enums.attribute import AttrEnum
from enums.entity_events import EntityEvents
from enums.gamestate import GameStateEnums
from enums.location import LocEnum
from enums.operator import Ops_
from enums.origin_enum import OriginEnum
from enums.post_event_param import PostEventParam
from enums.types import Types_
from resolvable_enums.auto_card_selector import AutoEntitySelector
import Sets.SET6.Spells as SET6Spells
import Sets.SET6.Units as SET6Units
import Sets.SET6.Skills as SET6Skills
import Sets.SET6.Equipments as SET6Equipments
from resolvable_enums.player_conditions import PlayerFlags
from value.entity_attribute import EntityAttribute


def Norra():
    effect = PlantMysteriousPortalEffect()
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Norra2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.SUMMON,
        threshold=6,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        instance_bound=False,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
        location=None,
    )
    return Champion(nexus_strike_effect=effect, champion_spell=SET6Spells.Portalpalooza)


# Your Mysterious Portals now summon 4, 5, 6, or 7 cost followers instead.
# Nexus Strike: Plant a Mysterious Portal randomly in the top 4 cards of your deck.
def Norra2():
    effect = PlantMysteriousPortalEffect()
    # TODO
    return Champion(nexus_strike_effect=effect, champion_spell=SET6Spells.Portalpalooza)


def Illaoi():
    effect = SpawnEffect(quantity=1)
    value = EntityAttribute(
        target=AutoEntitySelector.ALLIED_STRONGEST_TENTACLE,
        attribute=AttrEnum.ATTACK,
    )
    effect1 = BuffEffect(target=AutoEntitySelector.SELF, attack=value, round_only=True)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Norra2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.DAMAGE,
        threshold=6,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_OPPO_O_ALLY,
        event_counter=EventCounterEnum.COUNT_VALUE,
        instance_bound=False,
        location=None,
        condition=...,
    )
    return Champion(effects=watcher, attack_commit_effect=[effect, effect1])


# When you Spawn, increase its value by 1.
# Attack: Spawn 1, then fully heal your strongest Tentacle and I gain stats equal to its stats this round.
def Illaoi2():
    effect = SpawnEffect(quantity=1)
    value = EntityAttribute(
        target=AutoEntitySelector.ALLIED_STRONGEST_TENTACLE,
        attribute=AttrEnum.ATTACK,
    )
    value2 = EntityAttribute(
        target=AutoEntitySelector.ALLIED_STRONGEST_TENTACLE,
        attribute=AttrEnum.HEALTH,
    )
    heal = HealEffect(
        target=AutoEntitySelector.ALLIED_STRONGEST_TENTACLE, value=Ops_.MAX
    )
    effect1 = BuffEffect(
        target=AutoEntitySelector.SELF, attack=value, health=value2, round_only=True
    )
    effect2 = ActionModifier(
        event_filter=EntityEvents.SPAWN,
        ally_enum=OriginEnum.O_ALLY,
        parameter=...,
        operator=Ops_.INCREMENT,
        value=1,
    )
    return Champion(attack_commit_effect=[effect, heal, effect1], effects=effect2)


# When I'm summoned or Round Start: Create a 0 cost Tumble in hand or if you have one, reduce its cost by 3.
def Vayne():
    effect = CreateCardEffect(target=SET6Spells.Tumble)
    effect1 = BuffCostEffect(target=CardFilter(card_class=SET6Spells.Tumble), value=1)
    effect2 = BranchingAction(
        condition=...,
        if_true=effect1,
        if_false=effect,
    )
    ta = TriggeredAction(event_filter=GameStateEnums.ROUND_START, action=effect2)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Vayne2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.PLAYER_ATTACK_COMMIT,
        threshold=4,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(effects=[watcher, ta], summon_effect=effect2)


def Vayne2():
    effect = CreateCardEffect(target=SET6Spells.Tumble, cost=0)
    effect1 = BuffCostEffect(
        target=CardFilter(card_class=SET6Spells.Tumble), value=0, operator=Ops_.SET
    )
    effect2 = BranchingAction(
        condition=...,
        if_true=effect1,
        if_false=effect,
    )
    ta = TriggeredAction(event_filter=GameStateEnums.ROUND_START, action=effect2)
    return Champion(effects=ta, summon_effect=effect2)


# Play: Equip me with an exact copy of an ally's equipment or the strongest equipment from hand.Attack: Forge me twice, then summon an attacking Spirit of the Ram with my stats.
def Ornn():
    effect2 = EquipEffect(
        target=AutoEntitySelector.SELF,
        equipment=...,
        triggering_effect=EntityEvents.PLAY,
    )
    effect = ForgeEffect(target=AutoEntitySelector.SELF)
    effect1 = MultipleActivationsEffect(effect=effect)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Ornn2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.STRIKE,
        threshold=True,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        event_counter=EventCounterEnum.BOOLEAN,
    )
    return Champion(attack_commit_effect=effect1, play_effect=effect2, effects=watcher)


def Ornn2():
    effect2 = EquipEffect(
        target=AutoEntitySelector.SELF,
        equipment=...,
        triggering_effect=EntityEvents.PLAY,
    )
    effect = ForgeEffect(target=AutoEntitySelector.SELF)
    effect1 = MultipleActivationsEffect(effect=effect)
    summon = CreateCardEffect(
        target=...,
        location=LocEnum.HOMEBASE,
        with_my_stats_source=AutoEntitySelector.SELF,
    )
    return Champion(attack_commit_effect=[effect1, summon], play_effect=effect2)


# Attack: I immediately strike the weakest enemy. Round Start: Reduce the cost of a spell in your hand by 1 and Flow: Grant all allied Master Yis everywhere +2|+0.
def MasterYi():
    effect = BuffCostEffect(
        target=CardFilter(type=Types_.SPELL, location=LocEnum.HAND),
        value=1,
    )
    effect1 = BuffEverywhereEffect(
        filter_obj=BaseCardFilter(card_class=MasterYi),
        attack=2,
    )
    trigger1 = TriggeredAction(event_filter=GameStateEnums.ROUND_START, action=effect)
    trigger2 = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START,
        action=effect1,
        condition=PlayerFlags.FLOW,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=MasterYi2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.DAMAGE,
        threshold=12,
        action_on_value=levelup,
        ally_enum=OriginEnum.O_ALLY,
        condition=...,
        instance_bound=False,
        event_counter=EventCounterEnum.COUNT_VALUE,
    )
    return Champion(effects=[watcher, trigger1, trigger2])


def MasterYi2():
    effect = BuffCostEffect(
        target=CardFilter(type=Types_.SPELL, location=LocEnum.HAND),
        value=1,
    )
    effect1 = BuffEverywhereEffect(
        filter_obj=BaseCardFilter(card_class=MasterYi),
        attack=2,
    )
    trigger1 = TriggeredAction(event_filter=GameStateEnums.ROUND_START, action=effect)
    trigger2 = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START,
        action=effect1,
        condition=PlayerFlags.FLOW,
    )
    attack = StrikeEffect(
        target=AutoEntitySelector.WEAKEST_OPPONENT_UNIT, striker=AutoEntitySelector.SELF
    )
    return Champion(effects=[trigger1, trigger2], attack_commit_effect=attack)


# Attack: I deal 3 to my blocker and Stun it. If it's dead or gone, I deal 3 to the enemy Nexus instead.
def Annie():
    effect = CreateCardEffect(target=SET6Units.Tibbers)
    create_tibbers = TriggeredAction(
        event_filter=EntityEvents.LEVEL_UP, action=effect, ally_enum=OriginEnum.T_SELF
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Annie2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.PLAY_FAST_OR_SLOW_OR_SKILL,
        threshold=6,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        event_counter=EventCounterEnum.COUNT_VALUE,
    )
    skill = PlaySkill(target=SET6Skills.MoltenShield)
    return Champion(effects=[watcher, create_tibbers], attack_commit_effect=skill)


def Annie2():
    skill = PlaySkill(target=SET6Skills.MoltenShield)
    return Champion(attack_commit_effect=skill)


# When I'm summoned, create a random new 2 cost spell in hand.When you play a new spell that costs 2 or less, copy it with the same targets.
def Seraphine():
    effect = CreateCardEffect(
        target=BaseCardFilter(is_new=True, type=Types_.SPELL, cost=2),
        triggering_effect=EntityEvents.SUMMON,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Seraphine2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL,
        threshold=9,
        condition=...,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        instance_bound=False,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(summon_effect=effect, effects=watcher)


def Seraphine2():
    effect = CreateCardEffect(
        target=BaseCardFilter(is_new=True, type=Types_.SPELL, cost=2),
        triggering_effect=EntityEvents.SUMMON,
    )
    effect1 = RecastEventOfAction(target=PostEventParam.TARGET)
    effect = TriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL,
        action=effect1,
        condition=...,
        ally_enum=OriginEnum.T_ALLY,
    )
    return Champion(summon_effect=effect, effects=effect)


def TheWanderingCaretaker():
    effect = PlantChimes(quantity=..., entire_deck=True)
    ta = TriggeredAction(event_filter=GameStateEnums.ROUND_START, action=effect)
    # TODO


# Attack: Plant 6 Chimes on random cards in your deck.
# When you activate a Chime, grant +1|+1 to a random ally in play.
def Bard():
    effect = PlantChimes(
        quantity=3,
        entire_deck=True,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Bard2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.SET_ATTRIBUTE,
        threshold=20,
        condition=...,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        instance_bound=False,
        event_counter=EventCounterEnum.COUNT_VALUE,
    )
    return Champion(summon_effect=effect, effects=watcher)


def Bard2():
    effect = PlantChimes(
        quantity=6,
        entire_deck=True,
    )
    effect1 = BuffEffect(target=CardFilter(), attack=1, health=1)
    ta = TriggeredAction(
        event_filter=EntityEvents.ACTIVATE_CHIME,
        ally_enum=OriginEnum.T_ALLY,
        action=effect1,
    )
    return Champion(summon_effect=effect, effects=ta)


def TheVirtuoso():
    ...
    # TODO


# Attack: Deal 4 to all Stunned enemies and the enemy Nexus.
def Jhin():
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Jhin2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.PLAY_FAST_OR_SLOW_OR_SKILL,
        threshold=12,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        event_counter=EventCounterEnum.COUNT_VALUE,
    )
    skill = PlaySkill(target=SET6Skills.DeadlyFlourish)
    return Champion(effects=watcher, attack_commit_effect=skill)


def Jhin2():
    skill = PlaySkill(target=SET6Skills.CurtainCall)
    return Champion(attack_commit_effect=skill)


def TheShadowReaper():
    ...


# Play: Transform me and all copies of me into Rhaast or The Shadow Assassin.
def Kayn():
    heal = HealEffect(target=AutoEntitySelector.SELF, value=2)
    effect1 = TriggeredAction(
        event_filter=EntityEvents.SLAY, action=heal, ally_enum=OriginEnum.T_ALLY
    )
    effect = AutoEquipEffect(equipment=SET6Equipments.TheDarkinScythe)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Kayn2)

    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.STRIKE,
        threshold=2,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_SELF,
        event_counter=EventCounterEnum.COUNT_VALUE,
    )
    effect = RecallEffect(target=AutoEntitySelector.SELF)
    recall = TriggeredAction(
        event_filter=EntityEvents.LEVEL_UP, action=effect, ally_enum=OriginEnum.T_SELF
    )
    return Champion(summon_effect=effect, effects=[watcher, effect1, recall])


def TheShadowAssassin():
    effect = AutoEquipEffect(equipment=SET6Equipments.ShadowScythe)
    return Champion(summon_effect=effect)


def Rhaast():
    effect = AutoEquipEffect(equipment=SET6Equipments.CorruptedScythe)
    return Champion(summon_effect=effect)


def Kayn2():
    choice_form = ChoiceBaseCard(choices=[S])
    effect = TransformEffect(
        target=CardFilter(location=None, card_type=Kayn2),
        new_form=choice_form,
        apply_everywhere=True,
    )
    return Champion(play_effect=effect)


# Auto-Equip The Light of Icathia.Attack: Give me +1|+1 for each equipped ally this round.
def Jax():
    effect = AutoEquipEffect(equipment=SET6Equipments.TheLightofIcathia)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Jax2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.STRIKE,
        threshold=12,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        instance_bound=False,
        event_counter=EventCounterEnum.COUNT_VALUE,
    )
    return Champion(effects=watcher, summon_effect=effect)


def Jax2():
    effect = AutoEquipEffect(equipment=SET6Equipments.TheLightofIcathia)
    val = ...
    # TODO
    effect1 = BuffEffect(
        target=AutoEntitySelector.SELF, attack=val, health=val, round_only=True
    )
    return Champion(summon_effect=effect, attack_commit_effect=effect1)


# Auto-Equip The Darkin Bow. The Darkin Bow activates twice and has max +10|+0.
def Varus():
    effect = AutoEquipEffect(equipment=SET6Equipments.TheDarkinBow)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Varus2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.TARGETED,
        threshold=7,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        instance_bound=False,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(effects=watcher, summon_effect=effect)


def Varus2():
    effect = AutoEquipEffect(equipment=SET6Equipments.TheDarkinBow)
    effect1 = DynamicAttackModifier(value=10)
    # TODO
    recast = RecastEventOfAction(target=...)
    ta = TriggeredAction(
        event_filter=EntityEvents.SET_ATTRIBUTE,
        action=recast,
        ally_enum=OriginEnum.O_ALLY,
        condition=...,
    )
    return Champion(effects=[effect1, ta], summon_effect=effect)


# When you or an ally kill an allied Husk, give me its positive keywords this round.Round End: Summon a random Husk. If fewer than 6 allies have died this game, transform me back into Evelynn.
def Evelynn():
    effect2 = SummonHuskEffect()
    effect1 = CopyKeywords(
        target=AutoEntitySelector.SELF, source=PostEventParam.TARGET, round_only=True
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Evelynn2)

    ta = TriggeredAction(
        event_filter=EntityEvents.KILL,
        action=[effect1, levelup],
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        condition=...,
    )
    return Champion(effects=ta, summon_effect=effect2)


def Evelynn2():
    effect1 = SummonHuskEffect()
    ta1 = TriggeredAction(
        event_filter=GameStateEnums.ROUND_END,
        action=effect1,
    )
    effect2 = CopyKeywords(
        target=AutoEntitySelector.SELF, source=PostEventParam.TARGET, round_only=True
    )
    ta2 = TriggeredAction(
        event_filter=EntityEvents.KILL,
        action=effect2,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        condition=...,
    )
    #TODO
    transform = TransformEffect(target=CardFilter())
    ta3 = TriggeredAction(
        event_filter=GameStateEnums.ROUND_END,
        action=transform,
        condition=...
    )
    return Champion(effects=[ta1, ta2, ta3])


# When I'm summoned or Round Start: If you have the attack token, create a Second Skin in hand.Attack: Deal 1 for each positive keyword I have to enemies or the enemy Nexus (lowest health first).
def KaiSa():
    effect1 = CreateCardEffect(
        target=SET6Spells.SecondSkin,
        triggering_effect=EntityEvents.SUMMON,
    )
    ta1 = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START,
        action=effect1,
        condition=PlayerFlags.HAS_ATTACK_TOKEN
    )
    #TODO
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=KaiSa2)
    return Champion(summon_effect=effect1, effects=[ta1, ...])

def KaiSa2():
    effect1 = CreateCardEffect(
        target=SET6Spells.SecondSkin,
        triggering_effect=EntityEvents.SUMMON,
    )
    ta1 = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START,
        action=effect1,
        condition=PlayerFlags.HAS_ATTACK_TOKEN
    )
    effect2 = PlaySkill(target=SET6Skills.IcathianRain)
    return Champion(summon_effect=effect1, effects=ta1, attack_commit_effect=effect2)


# Attack:  When another ally gains Power from Hallowed, so do I. 
# Drain 1 from the enemy Nexus one time for every 2 Power I have.
def Gwen():
    effect2 = PlaySkill(target=SET6Skills.SnipSnip)
    buff = BuffEffect(target=AutoEntitySelector.SELF, attack=...)
    ta = TriggeredAction(
        event_filter=EntityEvents.BUFFED_BY_HALLOW,
        ally_enum=OriginEnum.T_ALLY,
        action=buff
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Gwen2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.DAMAGE,
        threshold=10,
        action_on_value=levelup,
        ally_enum=OriginEnum.O_SELF,
        event_counter=EventCounterEnum.COUNT_VALUE
    )
    return Champion(attack_commit_effect=effect2, effects=[watcher, ta])

def Gwen2():
    effect2 = PlaySkill(target=SET6Skills.SnipSnipSnip)
    buff = BuffEffect(target=AutoEntitySelector.SELF, attack=...)
    ta = TriggeredAction(
        event_filter=EntityEvents.BUFFED_BY_HALLOW,
        ally_enum=OriginEnum.T_ALLY,
        action=buff
    )
    return Champion(attack_commit_effect=effect2, effects=ta)
