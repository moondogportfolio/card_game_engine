

from attr import define, field
from actions.base_action import BaseAction

from classes.gamestate import GameState
from enums.attribute import AttrEnum
from enums.operator import Ops_


@define
class SpendManaEffect(BaseAction):
    value: int = field(default=1)
    include_spell_mana: bool = field(default=False)

    
    def resolve(self, gamestate: GameState):
        gamestate.entity_man.set_attribute(
            target=self.target,
            attribute=AttrEnum.HEALTH,
            value=self.value,
            operator=Ops_.INCREMENT,
        )

