from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from enums.entity_events import EntityEvents
from enums.location import LocEnum


from attr import define, field

from events.movement.MovementEvent import MovementEvent


@define
class DiscardEvent(MovementEvent):
    event: EntityEvents = field(init=False, default=EntityEvents.DISCARD)
    destination: LocEnum = field(init=False, default=LocEnum.SHADOWREALM)

    def resolve(self, gamestate: GameState, origin: CardArchetype, *args, **kwargs):
        return super().resolve(gamestate, origin, *args, **kwargs)