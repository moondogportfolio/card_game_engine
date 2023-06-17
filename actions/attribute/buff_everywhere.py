from typing import Any, Tuple
from attr import define, field
from actions.attribute.buff import BuffCostEffect, BuffEffect

from actions.base_action import BaseAction, BaseTargetAction
from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from entity_classes.player import Player
from entity_selectors.base_card_filter import BaseCardFilter
from enums.keywords import KeywordEnum
from events.attribute.buff_everywhere_Event import BuffEverywhereEvent
from events.base_event import BaseEvent


@define
class BuffEverywhereEffect(BaseAction):
    filter_obj: BaseCardFilter = None
    attack: int | None = field(default=None)
    health: int | None = field(default=None)
    cost: int | None = field(default=None)
    keyword: KeywordEnum | None = field(default=None)
    buff_obj: BuffEffect = None

    def resolve(self, *args, **kwargs) -> BaseEvent | Tuple[BaseEvent]:
        effects = []
        if self.attack or self.health or self.keyword:
            effects.append(
                BuffEffect(
                    target=None,
                    attack=self.attack,
                    health=self.health,
                    keyword=self.keyword,
                )
            )
        if self.cost:
            effects.append(BuffCostEffect(target=None, value=self.cost))
        if self.buff_obj:
            effects.append(self.buff_obj)
        return BuffEverywhereEvent(card_filter=self.filter_obj, buff_obj=effects)


@define
class TargetedBuffEverywhereEffect(BaseTargetAction):
    attack: int | None = field(default=None)
    health: int | None = field(default=None)
    cost: int | None = field(default=None)
    keyword: KeywordEnum | None = field(default=None)
    buff_obj: BuffEffect = None

    def resolve(
        self, target: CardArchetype, *args, **kwargs
    ) -> BaseEvent | Tuple[BaseEvent]:
        effects = []
        if self.attack or self.health or self.keyword:
            effects.append(
                BuffEffect(
                    target=None,
                    attack=self.attack,
                    health=self.health,
                    keyword=self.keyword,
                )
            )
        if self.cost:
            effects.append(BuffCostEffect(target=None, value=self.cost))
        if self.buff_obj:
            effects.append(self.buff_obj)
        return BuffEverywhereEvent(
            card_filter=BaseCardFilter(card_type=target.cardcode), buff_obj=effects
        )
