from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from enums.attribute import AttrEnum
from enums.entity_events import EntityEvents
from enums.keywords import KeywordEnum
from enums.operator import Ops_
from events.attribute.SetAttributeEvent import SetAttributeEvent


from attr import define, field

from events.base_event import BaseTargetEvent


@define
class BuffEvent(BaseTargetEvent):
    event: EntityEvents = field(default=None, init=False) 
    attack: int | None = field(default=None) 
    health: int | None = field(default=None)
    keywords: KeywordEnum | None = field(default=None)
    operator: Ops_ = field(default=Ops_.INCREMENT)
    round_only: bool = field(kw_only=True, default=False)

    def resolve(self, gamestate: GameState, *args, **kwargs):
        if self.attack:
            gamestate.entity_man.set_attribute(
                target=self.target,
                attribute=AttrEnum.HEALTH,
                value=self.attack,
                operator=self.operator,
            )
        if self.health:
            gamestate.entity_man.set_attribute(
                target=self.target,
                attribute=AttrEnum.HEALTH,
                value=self.health,
                operator=self.operator,
            )
        if self.keywords:
            gamestate.entity_man.set_attribute(
                target=self.target,
                attribute=AttrEnum.KEYWORDS,
                value=self.keywords,
                operator=Ops_.PUSH,
            )