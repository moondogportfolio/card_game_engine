
from attr import define, field
from actions.create.base_create import BaseCreateCardEffect
from classes.gamestate import GameState
from entity_selectors.base_card_filter import BaseCardFilter, ManifestBaseCardFilter
from enums.location import LocEnum


@define
class ManifestEffect(BaseCreateCardEffect):
    target: ManifestBaseCardFilter = field(factory=ManifestBaseCardFilter)
    location: LocEnum = field(default=LocEnum.HAND, init=False)
    index: int = field(init=False)
    quantity: int = field(init=False)
    summon_chosen_card: bool = field(default=False, kw_only=True)

    """
    if choices have 4 or more elements, select 3 at random
    """
    def resolve(self, gamestate: GameState):
        return super().resolve(gamestate)
