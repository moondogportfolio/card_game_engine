


from typing import Any, Callable
from attr import define, field
from actions.base_action import BaseTargetAction
from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from enums.entity_events import EntityEvents
from events.base_event import BaseTargetEvent


@define
class TransformEffect(BaseTargetAction):
    new_form: CardArchetype
    self_transform: bool = False
    change_identity: bool = True
    function: Callable[[CardArchetype], None] | None = None
    origin=None
    overwrite: bool = False
    revert_if_contains: bool = True
    apply_everywhere: bool= field(default=False)
    exact_copy: bool = False

    def resolve(self, gamestate: GameState, origin: Any):
        return TransformEvent(event=EntityEvents.TRANSFORM, new_form_card=...)
    
@define
class TransformEvent(BaseTargetEvent):
    new_form_card: CardArchetype