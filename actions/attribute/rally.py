from attr import define
from events.attribute.SetAttributeEvent import SetAttributeEvent
from actions.base_action import BaseAction
from classes.gamestate import GameState
from enums.attribute import AttrEnum
from enums.entity_events import EntityEvents
from enums.operator import Ops_

@define
class RallyEffect(BaseAction):

    def resolve(self, gamestate: GameState):
        gamestate.entity_man.set_attribute(
            target=self.target,
            attribute=AttrEnum.RALLY,
            value=True,
            operator=Ops_.SET,
        )
        return SetAttributeEvent(
            event=EntityEvents.GAIN_ATTACK_TOKEN,
            target=...,
            attribute=AttrEnum.RALLY,
            value=True,
            operator=Ops_.SET,
        )