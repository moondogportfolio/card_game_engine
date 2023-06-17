from __future__ import annotations
from collections import defaultdict

from enum import Enum
from typing import Dict, List, TYPE_CHECKING



if TYPE_CHECKING:         
    from actions.reactions.action_negator import ActionNegator
    from actions.reactions.action_modifier import ActionModifier
    from actions.base_action import BaseAction

class ListenerManager:

    def __init__(self) -> None:
        self.tampers: Dict[Enum, List[ActionModifier]] = defaultdict(list)
        self.negators: Dict[Enum, List[ActionNegator]] = defaultdict(list)

    def modifier_check(self, action: BaseAction):
        try:
            tamperlist = self.tampers[action.event_enum]
        except KeyError:
            return action
        tampers = [x for x in tamperlist if x.event_filter.check_if_satisfies_event(action)]
        for tamper in tampers:
            tamper.modify_event(event=action)
        return action

    