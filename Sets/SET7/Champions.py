from actions.attribute.buff import BuffEffect
from actions.attribute.rally import RallyEffect
from actions.champ.level_up import LevelupEffect
from actions.create.create_card import CreateCardEffect
from actions.create.create_hand_cards import GenerateCoinEffect
from actions.keywords.add_keyword import AddKeywordEffect
from actions.meta.reset_event_counter import ResetEventCounter
from actions.reactions.action_negator import ActionNegator
from actions.reactions.action_replacement import ActionReplacement
from actions.reactions.triggered_action import TriggeredAction
from actions.reactions.value_triggered_action import (
    EventCounterEnum,
    ValueTriggeredAction,
)
from card_classes.unit import Unit
from conditions.base_condition import Condition
from enums.entity_events import EntityEvents
from enums.keywords import KeywordEnum
from enums.origin_enum import OriginEnum
from resolvable_enums.auto_card_selector import AutoEntitySelector
from resolvable_enums.player_conditions import PlayerFlags
from resolvable_enums.target_player import TargetPlayer


def Jack():
    effect = GenerateCoinEffect()
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Jack2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.USE_MANA_FOR_PLAY,
        threshold=12,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_SELF,
        instance_bound=False,
        location=None,
    )
    return Unit(strike_effect=effect)


def Jack2():
    effect = GenerateCoinEffect(value=2)
    effect1 = BuffEffect(target=AutoEntitySelector.SELF, attack=...)
    effect2 = TriggeredAction(
        event_filter=EntityEvents.REFILL_MANA,
        action=effect1,
        ally_enum=OriginEnum.T_ALLY,
    )
    return Unit(strike_effect=effect, effects=effect2)


def Samira():
    effect = CreateCardEffect(target=...)
    condition = Condition(
        target=TargetPlayer.ORIGIN_OWNER,
        condition=PlayerFlags.HAS_NO_X_HAND_CARD,
        parameter=...,
    )
    effect1 = TriggeredAction(
        event_filter=EntityEvents.STRIKE,
        action=effect,
        condition=condition,
        ally_enum=OriginEnum.T_SELF,
    )
    effect2 = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        condition=condition,
        ally_enum=OriginEnum.T_SELF,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Samira2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.PLAY,
        threshold=6,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_SELF,
    )
    reset = ResetEventCounter(target=watcher)
    ta = TriggeredAction(
        event_filter=EntityEvents.GAIN_ATTACK_TOKEN,
        ally_enum=OriginEnum.T_ALLY,
        action=reset,
    )
    return Unit(effects=[effect1, effect2, watcher, ta])


def Samira2():
    effect = CreateCardEffect(target=..., cost=0)
    effect1 = TriggeredAction(
        event_filter=EntityEvents.STRIKE,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
    )
    effect2 = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
    )
    effect3 = RallyEffect()
    effect4 = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
    )
    # TODO watcher
    return Unit(effects=[effect1, effect2, effect4])


def Sett():
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Samira2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.USE_MANA_FOR_PLAY,
        threshold=40,
        event_counter=EventCounterEnum.COUNT_VALUE,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_SELF,
        instance_bound=False,
    )
    action = AddKeywordEffect(
        target=AutoEntitySelector.SELF, keyword=KeywordEnum.BARRIER
    )
    ta = ActionReplacement(
        event_filter=EntityEvents.DAMAGE,
        ally_enum=OriginEnum.SELF,
        replacement_action=action,
        activate_once=True,
        condition=...
    )
    return Unit(effects=[watcher, ta])


def Sett2():
    negate_damage = ActionNegator(
        event_filter=EntityEvents.DAMAGE,
        ally_enum=OriginEnum.T_SELF,
        condition=...
    )
    negate_death = ActionNegator(
        event_filter=EntityEvents.DIE,
        ally_enum=OriginEnum.T_SELF,
        condition=...
    )
    create = CreateCardEffect(target=...)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.USE_MANA_FOR_PLAY,
        threshold=12,
        event_counter=EventCounterEnum.COUNT_VALUE,
        action_on_value=create,
        ally_enum=OriginEnum.T_SELF,
        
    )
    return Unit(effects=[watcher, negate_damage, negate_death])

