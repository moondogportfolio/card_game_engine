from attr import define, field
from events.attribute.SetAttributeEvent import SetAttributeEvent
from actions.base_action import BaseAction

from classes.gamestate import GameState
from enums.attribute import AttrEnum
from enums.entity_events import EntityEvents
from enums.operator import Ops_


@define
class GainManaGemEffect(BaseAction):
    value: int = field(default=1)
    gain_mana: bool = field(default=False)
    round_only: bool = field(default=False)

    def resolve(self, gamestate: GameState):
        return SetAttributeEvent(
            event=EntityEvents.GAIN_MANA_GEM,
            target=...,
            attribute=AttrEnum.MANA_GEM,
            value=self.value,
            operator=Ops_.INCREMENT,
        )