from card_classes.cardarchetype import CardArchetype
from card_classes.cardslot import CardSlot
from classes.gamestate import GameState
from enums.entity_events import EntityEvents
from enums.location import LocEnum
from events.base_event import BaseTargetEvent


from attr import define


@define
class MovementEvent(BaseTargetEvent):
    target: CardSlot
    destination: LocEnum

    def resolve(self, gamestate: GameState, origin: CardArchetype, *args, **kwargs):
        gamestate.loc_man.move_card(target=self.target, new_location=self.destination)

    def append_extra_signals(self, signals_list) -> EntityEvents:
        if self.target.location in (
            LocEnum.HOMEBASE,
            LocEnum.BATTLEFIELD,
        ) and self.destination not in (LocEnum.HOMEBASE, LocEnum.BATTLEFIELD):
            signals_list.append(EntityEvents.MOVED_OUT_OF_PLAY)
