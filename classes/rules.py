from typing import Callable, Dict
from typing import List
from attr import define
from enums.gamestate import GameStateEnums


@define
class GamePhase:
    effects: List
    next_phase: GameStateEnums


class Rules:

    def __init__(self) -> None:
        self.phases: Dict[GameStateEnums, GamePhase] = {}

    def add_phase(self, phase, next_phase: GameStateEnums, events: List):
        self.phases[phase] = GamePhase(events, next_phase)

    def get_next_phase(self, state: GameStateEnums | None):
        if state is None:
            next_phase = GameStateEnums.GAME_START
        else:
            next_phase = self.phases[state].next_phase
        return next_phase, self.phases[next_phase]