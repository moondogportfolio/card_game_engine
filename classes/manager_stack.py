from __future__ import annotations
from collections import deque
from typing import Any, Deque, List, TYPE_CHECKING

from attr import define


from enums.location import LocEnum


if TYPE_CHECKING:
    from card_classes.spell import Spell
    from classes.gamestate import GameState
    from actions.base_action import BaseAction


@define
class TargetCoordinates:
    player: Any
    location: LocEnum
    index: int


class StackManager:
    def __init__(self) -> None:
        self.stack: Deque[Spell] = deque()
        self.params: List = []

    def add_to_queue(
        self,
        effect: BaseAction,
        action_origin,
        tail: bool = True,
        coords: bool = False,
    ):
        # new_act = effect()
        # new_act.action_origin = action_origin
        if tail:
            self.stack.append((effect, action_origin, coords))
        else:
            self.stack.appendleft(effect)

    def resolve_stack(self, gamestate: GameState):
        while len(self.stack) > 0:
            action, origin, coords = self.stack[0]
            try:
                # if event.resolve_condition(self.game_obj):
                # event.resolve_params(gamestate)
                print(f"activating {action.__class__}")
                # action.resolve_params(gamestate)
                if coords:
                    result = action.resolve(gamestate, origin)
                    print(result)
                    gamestate.spell_stack_man.set_target(result, origin)
                self.stack.popleft()
                # ADD TO STACK POSTEVENTS
                # gamestate.event_man.post_event(action)
            except InputError:
                return
