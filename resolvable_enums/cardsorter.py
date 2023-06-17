
from enum import Enum, auto
from operator import attrgetter
from typing import List


class CardSorter(Enum):
    WEAKEST = (attrgetter('attack', 'health', 'cost'), True)
    STRONGEST = (attrgetter('attack', 'health', 'cost'), False)
    CHEAPEST = (attrgetter('cost'), True)
    EXPENSIVEST = (attrgetter('cost'), False)

    def resolve(self, entities: List):
        return entities.sort(key=self.value[0], reverse=self.value[1])