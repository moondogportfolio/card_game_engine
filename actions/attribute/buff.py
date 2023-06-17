from typing import Any, Callable
from attr import define, field
from actions.base_action import BaseAction, BaseTargetAction
from enums.entity_events import EntityEvents
from events.attribute.SetAttributeEvent import SetAttributeEvent
from events.attribute.add_keyword_event import AddKeywordEvent
from events.base_event import BaseEvent
from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from enums.attribute import AttrEnum
from enums.keywords import KeywordEnum
from enums.operator import Ops_


@define
class BuffEffect(BaseTargetAction):
    attack: int | None | Callable[[CardArchetype, GameState], int] = field(default=None)
    health: int | None = field(default=None)
    keyword: KeywordEnum | None = field(default=None)
    round_only: bool = field(default=False)
    operator: Ops_ = field(default=Ops_.INCREMENT, kw_only=True)
    set_init: bool = field(default=False, kw_only=True)
    max_attack: int | None = field(default=None, kw_only=True)
    max_health: int | None = field(default=None, kw_only=True)
    send_to_attachment: bool | None = field(default=None, kw_only=True)

    def resolve(self, target, *args, **kwargs):
        events = []
        if self.attack:
            events.append(
                SetAttributeEvent(
                    event=None,
                    attribute=AttrEnum.ATTACK,
                    value=self.attack,
                    target=target,
                    operator=Ops_.INCREMENT,
                )
            )
        if self.health:
            events.append(
                SetAttributeEvent(
                    event=None,
                    attribute=AttrEnum.HEALTH,
                    value=self.health,
                    target=target,
                    operator=Ops_.INCREMENT,
                )
            )
        if self.attack:
            events.append(
                AddKeywordEvent(
                    value=self.keyword,
                    target=target,
                )
            )
        return events
        # self.target = self.target.resolve(gamestate, origin, postevent)
        # gamestate.entity_man.set_attribute(
        #     target=self.target,
        #     attribute=AttrEnum.ATTACK,
        #     value=self.attack,
        #     operator=self.operator,
        # )
        # if (self.operator is not Ops_.SET and self.health != 0) and self.health is not None:
        #         gamestate.entity_man.set_attribute(
        #             target=self.target,
        #             attribute=AttrEnum.HEALTH,
        #             value=self.health,
        #             operator=self.operator,
        #         )


@define
class BuffSupportEffect(BaseAction):
    buff_action: BuffEffect


class BuffSupportEvent:
    target: CardArchetype
    supporter: CardArchetype

    def resolve(self, gamestate: GameState):
        ...


@define
class BuffCostEffect(BaseTargetAction):
    value: int = field(default=1)
    round_only: bool = field(default=False)
    operator: Ops_ = field(default=Ops_.DECREMENT)

    def resolve(self, target, *args, **kwargs):
        print(target, self.value)
        return SetAttributeEvent(
            event=EntityEvents.DAMAGE,
            attribute=AttrEnum.COST,
            value=self.value,
            target=target,
            operator=self.operator,
        )
