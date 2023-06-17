from typing import Any, List, Tuple
from attr import define
from actions.base_action import BaseTargetAction

from actions.reactions.triggered_action import TriggeredAction
from classes.gamestate import GameState
from events.actions_modifier.grant_reaction_actions import GrantReactionActions
from events.base_event import BaseEvent


@define
class CreateTriggeredAction(BaseTargetAction):
    triggered_action: TriggeredAction | List[TriggeredAction]

    def resolve(self, target, *args, **kwargs) -> BaseEvent | Tuple[BaseEvent]:
        return GrantReactionActions(
            triggered_action=self.triggered_action, target=target, event=None
        )
