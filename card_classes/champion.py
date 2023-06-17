from typing import Any
from attr import define, field
from card_classes.cardarchetype import CardArchetype
from card_classes.unit import Unit

@define(repr=False)
class Champion(Unit):
    champion_spell: CardArchetype | None | Any = field(default=None)