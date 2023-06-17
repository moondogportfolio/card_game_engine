from attr import define
from events.attribute.SetAttributeEvent import SetAttributeEvent

from actions.base_action import BaseTargetAction
from classes.gamestate import GameState
from enums.attribute import AttrEnum
from enums.entity_events import EntityEvents
from enums.operator import Ops_


@define
class FrostbiteEffect(BaseTargetAction):
    
    def resolve(self, gamestate: GameState):
        return SetAttributeEvent(
            event=EntityEvents.FROSTBITE,
            attribute=AttrEnum.ATTACK,
            value=0,
        )
