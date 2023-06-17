from attr import define, field
from card_classes.cardarchetype import CardArchetype
from card_classes.unit import Unit
from classes.gamestate import GameState
from enums.attribute import AttrEnum
from enums.entity_events import EntityEvents
from enums.operator import Ops_

from events.base_event import BaseTargetEvent


@define
class StrikeEvent(BaseTargetEvent):
    striker: Unit
    event: EntityEvents = field(default=EntityEvents.STRIKE, init=False) 
    target_killed: bool = field(default=False, init=False)

    def resolve(self, gamestate: GameState, origin: CardArchetype):
        gamestate.entity_man.set_attribute(
            target=self.target,
            attribute=AttrEnum.HEALTH,
            value=self.striker.attack,
            operator=Ops_.DECREMENT,
        )
        if self.target.health <= 0:
            self.target_killed = True