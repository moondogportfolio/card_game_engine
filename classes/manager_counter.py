from collections import defaultdict
from typing import Any, Dict, Tuple
from card_classes.cardslot import CardSlot

from enums.counters import TrapEnums
from enums.operator import Ops_


class CounterManager:
    
    def __init__(self) -> None:
        self.entities: Dict[Tuple[int, TrapEnums], int] = defaultdict(lambda: 0)

    
    def set_trap(self, entity: CardSlot, trap: TrapEnums, quantity: int, operator: Ops_):
        def execute(trap_enum):
            original_value = self.entities[(entity.id, trap_enum)]
            new_value = operator.compute(original_value, quantity)
            self.entities[(entity.id, trap_enum)] = new_value
        if trap is TrapEnums.BOON:
            for subtrap in (TrapEnums.CHIME, TrapEnums.MYSTERIOUS_PORTAL):
                execute(subtrap)
        else:
            execute(trap)

    def get_traps(self, entity: CardSlot, trap: TrapEnums) -> int:
        return self.entities[(entity.id, trap)]
