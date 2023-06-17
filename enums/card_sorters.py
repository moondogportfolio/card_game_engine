from __future__ import annotations
from enum import Enum, auto
from typing import TYPE_CHECKING, Callable, Dict, List

if TYPE_CHECKING:
    from card_classes.cardarchetype import CardArchetype


class CardSorter(Enum):
    WEAKEST = auto()
    STRONGEST = auto()
    CHEAPEST = auto()
    EXPENSIVEST = auto()

    def resolve(self, cards: List[CardArchetype]):
        sorter_dict[self](cards)

def strongest(cards: List[CardArchetype], reverse: bool = False):
    cards.sort(key=lambda x: x, reverse=reverse)

def expensivest(cards: List[CardArchetype], reverse: bool = False):
    cards.sort(key=lambda x: x, reverse = reverse)

sorter_dict: Dict[CardSorter, Callable[[List[CardArchetype]], List[CardArchetype]]] = {
    CardSorter.STRONGEST: strongest,
    CardSorter.WEAKEST: lambda x: strongest(x, True),
    CardSorter.EXPENSIVEST: expensivest,
    CardSorter.CHEAPEST: lambda x: expensivest(x, True),
}