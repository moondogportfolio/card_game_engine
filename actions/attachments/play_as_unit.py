
from attr import define

from card_classes.cardarchetype import CardArchetype


@define
class PlayEquipAsUnit:
    unit: CardArchetype