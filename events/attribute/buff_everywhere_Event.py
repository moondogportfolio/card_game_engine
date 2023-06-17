from actions.base_action import BaseTargetAction
from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from entity_selectors.card_filter import CardFilter
from enums.entity_events import EntityEvents


from attr import define, field

from events.base_event import BaseEvent


@define
class BuffEverywhereEvent(BaseEvent):
    card_filter: CardFilter
    buff_obj: BaseTargetAction
    event: EntityEvents = field(default=None, init=False)

    def resolve(self, gamestate: GameState, origin: CardArchetype):
        #TODO
        gamestate.entity_man.set_attribute(
            target=self.target,
            attribute=self.attribute,
            value=self.value,
            operator=self.operator,
        )