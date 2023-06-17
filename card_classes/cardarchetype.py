
from enum import Enum
from typing import Any, List, Tuple
from attr import define, field
from actions.base_action import BaseAction
from actions.reactions.continuous_action import ContinuousAction
from actions.reactions.triggered_action import TriggeredAction
from card_classes.cardslot import CardSlot
from data.data_marshal import cardcode2jsoncard
from enums.keywords import KeywordEnum
from enums.types import Types_


@define(repr=False)
class CardArchetype:
    cardcode: str = field(default=None)
    cardslot: CardSlot = field(default=None)
    continuous_effects: List[ContinuousAction] | None = field(
        kw_only=True, default=None
    )
    effects: Tuple[ContinuousAction] | ContinuousAction |None = field(kw_only=True, default=None)
    cost: int = field(init=False, default=1)
    id: int = field(init=False, default=None)
    TA_ally_target: List | None = field(default=None)
    name: str = field(init=False)
    play_requisite: BaseAction | None = field(default=None, kw_only=True)
    round_start_effects: BaseAction | None = field(default=None, kw_only=True)
    round_end_effects: BaseAction | None = field(default=None, kw_only=True)
    play_effect: List[BaseAction] | None = field(default=None)  
    keywords: List = field(factory=list)
    created: bool = field(kw_only=True, default=False)



    def __attrs_post_init__(self):
        return
        json_card = cardcode2jsoncard(self.cardcode)
        self.name = json_card['name']

    def get_internal_event(self, event: Enum) -> List[BaseAction]:
        ...

    def has_keyword(self, keyword: KeywordEnum):
        return False
    
    @property
    def positive_keywords(self):
        return self.keywords

    @property
    def index(self):
        return self.cardslot.index

    @property
    def owner(self):
        return self.cardslot.owner
    
    @property
    def opponent(self):
        return self.cardslot.owner

    @property
    def location(self):
        return self.cardslot.location
    
    
    def is_type_instance(self, type: Types_):
        return True
    

    # def test_trigger(self, event, gamestate):
    #     for effect in self.effects:
    #         if effect.is_triggered(event):
    #             try:
    #                 effect.action()
    #             except TypeError:
    #                 [subeffect.test_resolve(gamestate, self) for subeffect in effect.action]