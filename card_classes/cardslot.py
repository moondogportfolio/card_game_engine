from __future__ import annotations
from typing import TYPE_CHECKING, Any
from attr import define, field
from entity_classes.player import Player

from enums.location import LocEnum

if TYPE_CHECKING:
    from card_classes.cardarchetype import CardArchetype

@define(repr=False, eq=False)
class CardSlot:
    id: int
    archetype: CardArchetype
    owner: Player
    index: int = field(init=False)
    location: LocEnum = field(init=False)
    attributes: dict = field(init=False, factory=dict)

    def __eq__(self, __value: object) -> bool:
        try:
            return self.id == __value.id
        except:
            return False

    def set_attribute(self, __name: str, __value: Any) -> None:
        self.attributes[__name] = __value

    def get_attribute(self, attribute):
        try:
            return self.attributes[attribute]
        except:
            return getattr(self.archetype, attribute)

    def get_base_attribute(self, attribute):
        return getattr(self.archetype, attribute)

    def __repr__(self) -> str:
        return f'{self.id} {self.location} {self.owner}'