from typing import Literal
from attr import define, field
from events.attribute.SetAttributeEvent import SetAttributeEvent
from actions.base_action import BaseAction

from classes.gamestate import GameState
from enums.attribute import AttrEnum
from enums.entity_events import EntityEvents
from enums.operator import Ops_


@define
class RefillSpellMana(BaseAction):
    value: int | Literal[Ops_.MAX] = field(default=1)

    
    def resolve(self, gamestate: GameState):
        
        return SetAttributeEvent(
            event=EntityEvents.REFILL_SPELL_MANA,
            attribute=AttrEnum.SPELL_MANA,
            value=self.value,
            operator=Ops_.INCREMENT,
        )



@define
class RefillManaEffect(BaseAction):
    value: int | Literal[Ops_.MAX] = field(default=1)
    
    def resolve(self, gamestate: GameState):
        
        return SetAttributeEvent(
            event=EntityEvents.REFILL_MANA,
            attribute=AttrEnum.MANA,
            value=self.value,
            operator=Ops_.INCREMENT,
        )