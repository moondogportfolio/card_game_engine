from abc import abstractmethod
from typing import List

from attr import define, field

from classes.gamestate import GameState
from enums.card_sorters import CardSorter

class SelectorException(Exception):
    pass

@define
class EntitySelector:
    quantity: int | None = field(default=1, kw_only=True)
    minimum: int = field(default=1, kw_only=True)
    sorter: CardSorter | None = field(kw_only=True, default=None)
    
    def pare_return(self, entities) -> List | None:
        if self.quantity is None:
            return entities
        matches = len(entities)
        if matches >= self.quantity:
            return entities[:self.quantity]
        elif matches >= self.minimum:
            return entities
        else:
            return None

    @abstractmethod
    def resolve(self, gamestate: GameState):
        return
    
    @abstractmethod
    def validate(self, gamestate: GameState) -> bool:
        return