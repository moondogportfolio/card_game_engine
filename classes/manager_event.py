from __future__ import annotations
from collections import defaultdict
from enum import Enum
from typing import Dict, List, TYPE_CHECKING, Tuple
from actions.base_action import BaseTargetAction
from actions.reactions.action_modifier import ActionModifier
from actions.reactions.action_negator import ActionNegator
from actions.reactions.action_replacement import ActionReplacement
from actions.reactions.triggered_action import TriggeredAction
from card_classes.cardarchetype import CardArchetype
from enums.entity_events import EntityEvents

from events.event_exceptions import FailEvent


if TYPE_CHECKING:
    from events.base_event import BaseEvent
    from actions.base_action import BaseAction
    from classes.gamestate import GameState


class ActionNegatedException(Exception):
    ...


class EventManager:
    def __init__(self) -> None:
        self.post_events_dict: Dict[
            EntityEvents, List[Tuple[TriggeredAction, CardArchetype]]
        ] = defaultdict(list)
        self.pre_events_dict: Dict[
            EntityEvents, List[Tuple[ActionModifier, CardArchetype]]
        ] = defaultdict(list)
        self.hard_coded_rules: Dict[Enum, List] = None

    def add_action(self, action, bound_entity):
        if isinstance(action, (ActionNegator, ActionModifier, ActionReplacement)):
            self.pre_events_dict[action.event_filter].append((action, bound_entity))
        else:
            self.post_events_dict.update({action.event_filter: (action, bound_entity)})

    def pre_event(self, event: BaseEvent, gamestate: GameState, event_origin):
        # TODO exit fnc once replaced, negated
        print("Entering PRE event triggers")
        if event.event is None:
            return event
        for action, bound_origin in self.pre_events_dict[event.event]:
            if isinstance(action, ActionNegator):
                if not action.is_triggered(gamestate, bound_origin, event):
                    continue
                raise ActionNegatedException
        return event
        # def trigger(card, action):
        #     if isinstance(action, ActionNegator):
        #         raise ImportError
        #     elif isinstance(action, ActionModifier):
        #         if not action.is_triggered(gamestate, card, event):
        #             return event
        #         return action.modify_event(event)
        #     elif isinstance(action, ActionReplacement):
        #         if not action.is_triggered(gamestate, card, event):
        #             return event
        #         replacement_action = action.replacement_action
        #         print('event replaced')
        #         if isinstance(replacement_action, BaseTargetAction):
        #             targets = []
        #             for target_obj in replacement_action.get_target_objects():
        #                 entity = target_obj.resolve(
        #                         gamestate=gamestate,
        #                         origin=card,
        #                     )
        #                 targets.append(entity)
        #             return replacement_action.resolve(gamestate=gamestate, origin=card, *targets)
        #         return replacement_action.resolve(gamestate=gamestate, origin=card)
        #     return event
        # cards = gamestate.entity_man.cards
        # for card in cards:
        #     actions = card.effects
        #     if actions is None:
        #         continue
        #     try:
        #         for subaction in actions:
        #             event = trigger(card, subaction)

        #     except TypeError:  # actions is nontuple
        #         event = trigger(card, actions)
        # return event

    def post_event(self, event: BaseEvent, gamestate: GameState):
        print("Entering post event triggers")
        # try:
        #     for action, origin in self.post_events_dict[event.event]:
        #         if not action.is_triggered(gamestate, origin, event):
        #             continue
        #         action = action.action
        #         #TODO registered listeners origin
        #         self.resolve_action(
        #             action=action,
        #             gamestate=gamestate,
        #             origin=None,
        #             postevent=event,
        #         )
        # except KeyError:
        #     ...
        # def trigger(card, action):
        #     if not action.is_triggered(gamestate, card, event):
        #         return
        #     if not isinstance(action, TriggeredAction):
        #         return
        #     action = action.action
        #     self.resolve_action(
        #         action=action,
        #         gamestate=gamestate,
        #         origin=card,
        #         postevent=event,
        #     )
        # cards = gamestate.entity_man.cards
        # for card in cards:
        #     actions = card.effects
        #     if actions is None:
        #         continue
        #     try:
        #         for subaction in actions:
        #             trigger(card, subaction)

        #     except TypeError:  # actions is nontuple
        #         trigger(card, actions)

    def resolve_event(self, event: BaseEvent, gamestate, origin, *args, **kwargs):
        try:
            event = self.pre_event(event, gamestate, origin)
        except ActionNegatedException:
            print(f'event {event.event} negated')
            event.negated = True
            return event
        # signals = [event.event]
        # event.append_extra_signals(signals)
        try:
            event.resolve(gamestate, origin)
            self.post_event(event, gamestate)
            # for signal in signals:
            #     self.post_event(signal, event, gamestate)
        except FailEvent:
            event.success = False
        return event

    def resolve_action(self, action: BaseAction, gamestate, origin, *args, **kwargs):
        event = action.resolve(gamestate=gamestate, origin=origin, *args, **kwargs)
        if isinstance(event, (tuple, list)):
            for subevent in event:
                self.resolve_event(subevent, gamestate, origin, *args, **kwargs)
        else:
            return self.resolve_event(event, gamestate, origin, *args, **kwargs)

    def create_triggered_event(self, event):
        ...
