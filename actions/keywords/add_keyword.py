from enum import Enum
from random import choice
from typing import List
from attr import define, field
from events.attribute.SetAttributeEvent import SetAttributeEvent
from actions.base_action import BaseTargetAction
from classes.gamestate import GameState
from constants.positive_keywords import GENERATABLE_KEYWORDS, POSITIVE_KEYWORDS
from enums.attribute import AttrEnum
from enums.entity_events import EntityEvents
from enums.keywords import KeywordEnum
from enums.operator import Ops_


@define
class AddKeywordEffect(BaseTargetAction):
    keyword: KeywordEnum | List[KeywordEnum]
    round_only: bool = False
    event: Enum = field(init=False, default=EntityEvents.ADD_KEYWORD)
    quantity: int | None = field(default=None, kw_only=True)

    def resolve(self, target=None, *args, **kwargs):
        return SetAttributeEvent(
            event=EntityEvents.ADD_KEYWORD,
            attribute=AttrEnum.KEYWORDS,
            operator=Ops_.PUSH,
            value=self.keyword,
            target=target
        )


@define
class AddRandomKeywordEffect(BaseTargetAction):
    positive: bool = True
    count: int = 1
    round_only: bool = False
    event: Enum = field(init=False, default=EntityEvents.ADD_KEYWORD)

    def resolve(self):
        if self.positive:
            value = choice(POSITIVE_KEYWORDS)
        else:
            value = choice(GENERATABLE_KEYWORDS)
        return SetAttributeEvent(
            event=EntityEvents.ADD_KEYWORD,
            attribute=AttrEnum.KEYWORDS,
            operator=Ops_.PUSH,
            value=value
        )
