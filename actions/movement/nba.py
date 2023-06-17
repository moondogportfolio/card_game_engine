
from enum import Enum
from attr import define, field
from actions.base_action import BaseAction

from classes.gamestate import GameState
from enums.entity_events import EntityEvents
from enums.location import LocEnum


@define
class NabEffect(BaseAction):
    quantity: int = field(default=1)

    def resolve(self, gamestate: GameState):
        self.relocate(gamestate)
