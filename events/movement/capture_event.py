from actions.meta.create_ta import CreateTriggeredAction
from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from enums.attribute import AttrEnum
from enums.entity_events import EntityEvents
from enums.location import LocEnum
from events.base_event import BaseTargetEvent


from attr import define, field


@define
class CaptureEvent(BaseTargetEvent):
    storage: CardArchetype
    event: EntityEvents = field(init=False, default=EntityEvents.CAPTURE)

    def resolve(self, gamestate: GameState, origin: CardArchetype, *args, **kwargs):
        gamestate.loc_man.move_card(
            target=self.target, new_location=LocEnum.SHADOWREALM
        )
        gamestate.attach_man.push_entity_attachment(
            entity=self.storage,
            attribute=AttrEnum.CAPTURED_UNITS,
            attachment=self.target,
        )