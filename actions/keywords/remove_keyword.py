from enum import Enum
from typing import List
from attr import define, field
from events.attribute.SetAttributeEvent import SetAttributeEvent
from actions.base_action import BaseTargetAction
from classes.gamestate import GameState
from enums.attribute import AttrEnum
from enums.entity_events import EntityEvents
from enums.keywords import KeywordEnum
from enums.operator import Ops_


@define
class RemoveKeywordEffect(BaseTargetAction):
    keyword: KeywordEnum | List[KeywordEnum]
    round_only: bool = False
    event: Enum = field(init=False, default=EntityEvents.ADD_KEYWORD)

    def resolve(self, gamestate: GameState):
        return SetAttributeEvent(
            event=EntityEvents.REMOVE_KEYWORD,
            attribute=AttrEnum.KEYWORDS,
            value=self.keyword,
            operator=Ops_.PULL
        )
        # if type(self.keyword) is list:
        #     for keyword in self.keyword:
        #         gamestate.entity_man.set_attribute(
        #             target=self.target,
        #             attribute=AttrEnum.KEYWORDS,
        #             operator=Ops_.PUSH,
        #             value=self.keyword,
        #         )
        # else:
        #     gamestate.entity_man.set_attribute(
        #             target=self.target,
        #             attribute=AttrEnum.KEYWORDS,
        #             operator=Ops_.PUSH,
        #             value=self.keyword,
        #         )


@define
class PurgeKeywordsEffect(BaseTargetAction):
    purge_negative: bool = False
    purge_positive: bool = False
    purge_all: bool = False
    event: Enum = field(init=False, default=EntityEvents.REMOVE_KEYWORD)

    def resolve(self, gamestate: GameState):
        ...