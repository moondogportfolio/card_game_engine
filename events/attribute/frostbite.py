from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from enums.attribute import AttrEnum
from enums.entity_events import EntityEvents
from enums.operator import Ops_
from events.attribute.SetAttributeEvent import SetAttributeEvent


from attr import define, field


@define
class FrostbiteEvent(SetAttributeEvent):
    event: EntityEvents = field(default=EntityEvents.FROSTBITE, init=False) 
    attribute: AttrEnum = field(default=AttrEnum.ATTACK, init=False)
    value: int = field(default=0, init=False)
    operator: Ops_ = field(default=Ops_.SET, init=False)

    def resolve(self, gamestate: GameState, origin: CardArchetype):
        gamestate.entity_man.set_attribute(
            target=self.target,
            attribute=self.attribute,
            value=self.value,
            operator=self.operator,
        )