from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from enums.attribute import AttrEnum
from enums.entity_events import EntityEvents
from enums.operator import Ops_
from events.attribute.SetAttributeEvent import SetAttributeEvent


from attr import define, field


@define
class DamageEvent(SetAttributeEvent):
    event: EntityEvents = field(default=EntityEvents.DAMAGE, init=False) 
    attribute: AttrEnum = field(default=AttrEnum.HEALTH, init=False)
    value: int
    operator: Ops_ = field(default=Ops_.DECREMENT, init=False)
    target_killed: bool = field(default=False, init=False)

    def resolve(self, gamestate: GameState, origin: CardArchetype):
        gamestate.entity_man.set_attribute(
            target=self.target,
            attribute=self.attribute,
            value=self.value,
            operator=self.operator,
        )
        if self.target.health <= 0:
            self.target_killed = True