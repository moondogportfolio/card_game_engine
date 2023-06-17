from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from enums.attribute import AttrEnum
from enums.operator import Ops_
from events.base_event import BaseTargetEvent


from attr import define, field


@define
class SetAttributeEvent(BaseTargetEvent):
    attribute: AttrEnum
    value: int
    operator: Ops_ = field(default=Ops_.SET, kw_only=True)

    def resolve(self, gamestate: GameState, origin: CardArchetype):
        gamestate.entity_man.set_attribute(
            target=self.target,
            attribute=self.attribute,
            value=self.value,
            operator=self.operator,
        )