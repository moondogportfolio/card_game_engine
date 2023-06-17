
from typing import List, Set, Tuple
from attr import define, field

from enums.region import RegionEnum


@define(repr=False)
class Player:
    id: int
    health: int
    mana_gem: int
    spell_mana: int
    mana: int
    rally: bool
    deckcode: str
    regions: Set[RegionEnum] = field(init=False, default={RegionEnum.DEMACIA, RegionEnum.NOXUS})

    @property
    def owner(self):
        return self
    
    def __attrs_post_init__(self):
        print(f'{self} created')

    def __repr__(self) -> str:
        return f"Player{self.id} [H:{self.health}/M:{self.mana}]"
    
    def watched_list_values(self, value) -> List:
        return