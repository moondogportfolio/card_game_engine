from enum import Enum
from typing import List
from attr import define, field
from actions.attribute.support import SupportEffect
from actions.base_action import BaseAction
from card_classes.board_entity import BoardEntity

from card_classes.cardarchetype import CardArchetype
from enums.entity_events import EntityEvents
from enums.types import Types_


@define
class Unit(BoardEntity):
    attack: int = field(init=False, default=10)
    health: int = field(init=False, default=10)
    unit_spell: None | CardArchetype = field(default=None)
    strike_effect: List[BaseAction] | None = field(default=None)
    nexus_strike_effect: List[BaseAction] | None = field(default=None)
    attack_commit_effect: List[BaseAction] | None = field(default=None)
    support_effect: List[BaseAction] | None = field(default=None)
    support_effect: SupportEffect | None = field(default=None, kw_only=True)
    damage_survive_effect: BaseAction | None = field(default=None, kw_only=True)
    enlightened_effect: BaseAction | None = field(default=None, kw_only=True)
    name: str = field(kw_only=True, default=None)

    def is_type_instance(self, type: Types_):
        if type is Types_.UNIT:
            return True
        return False

    def get_internal_event(self, event: Enum):
        if event is EntityEvents.PLAY:
            return self.play_effect

    # def __attrs_post_init__(self):
    #     if not self.play_effect:
    #         return
    #     if not self.effects:
    #         self.effects = []
    #     effect = SelfTargetTriggeredAction(triggering_event=EntityEvents.PLAY, action=self.play_effect)
    #     self.effects.append(effect)
    #     super().__attrs_post_init__()

    def __repr__(self) -> str:
        return f'UNIT {self.id} {self.name} {self.attack}/{self.health} {self.location} {self.owner} '

@define
class StackableUnit(Unit):
    stack: int = field(init=False)