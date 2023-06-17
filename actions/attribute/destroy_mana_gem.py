

from attr import define, field

from classes.gamestate import GameState
from enums.attribute import AttrEnum
from enums.operator import Ops_


@define
class DestroyManaGem:
    value: int = field(default=1)

    
    def resolve(self, gamestate: GameState):
        gamestate.entity_man.set_attribute(
            target=self.target,
            attribute=AttrEnum.HEALTH,
            value=self.value,
            operator=Ops_.INCREMENT,
        )

