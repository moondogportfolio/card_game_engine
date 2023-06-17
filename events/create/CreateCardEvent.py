from __future__ import annotations
from random import choice
from typing import TYPE_CHECKING, Any, List, Tuple, Type
from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from data.data_marshal import import_card
from entity_classes.player import Player
from entity_selectors.base_card_filter import BaseCardFilter
from enums.attribute import AttrEnum
from enums.entity_events import EntityEvents
from enums.keywords import KeywordEnum
from enums.location import LocEnum
from enums.operator import Ops_
from events.base_event import BaseEvent
from resolvable_enums.target_player import TargetPlayer

if TYPE_CHECKING:
    from actions.create.base_create import BaseCreateCardEffect

from attr import define, field


@define
class CreateCardEvent(BaseEvent):
    
    target: Type
    location: LocEnum
    owner: Player
    quantity: int = field(default=1)
    is_fleeting: bool = field(default=None)
    is_ephemeral: bool = field(default=None)
    index: int | Tuple[int, int] | None = field(default=None)
    with_my_stats_source: Any = field(default=None)
    with_my_stats_keywords_source: Any = field(default=None)
    attack: int | Tuple[Ops_, int] = field(default=None)
    cost: int | Tuple[Ops_, int] = field(default=None)
    health: int | Tuple[Ops_, int] = field(default=None)
    keywords: KeywordEnum | List[KeywordEnum] = field(default=None)
    created_card: CardArchetype | None = field(init=False, default=None)
    event: EntityEvents = field(default=EntityEvents.CREATE_CARD, init=False)

    def resolve(self, gamestate, origin, *args, **kwargs):
        cc = self.target
        if isinstance(cc, BaseCardFilter):
            cc = cc.resolve(origin)
            cc = choice(list(cc.values()))
            cc = import_card(cc)            
        cards = gamestate.entity_man.create_card(
            cc=cc,
            location=self.location,
            owner=self.owner,
            gamestate=gamestate,
            quantity=self.quantity,
            index=self.index
        )
        for new_card in cards:
            if self.attack:
                if isinstance(self.attack, tuple):
                    operator = self.attack[0]
                    value = self.attack[1]
                else:
                    operator = Ops_.SET
                    value = self.attack
                gamestate.entity_man.set_attribute(
                    target=new_card,
                    attribute=AttrEnum.ATTACK,
                    value=value,
                    operator=operator,
                )
            if self.health:
                if isinstance(self.health, tuple):
                    operator = self.health[0]
                    value = self.health[1]
                else:
                    operator = Ops_.SET
                    value = self.health
                gamestate.entity_man.set_attribute(
                    target=new_card,
                    attribute=AttrEnum.HEALTH,
                    value=value,
                    operator=operator,
                )
            if self.keywords:
                gamestate.entity_man.set_attribute(
                    target=new_card,
                    attribute=AttrEnum.KEYWORDS,
                    value=self.keywords,
                    operator=Ops_.PUSH,
                )
            if self.is_ephemeral:
                gamestate.entity_man.set_attribute(
                    target=new_card,
                    attribute=AttrEnum.KEYWORDS,
                    value=KeywordEnum.EPHEMERAL,
                    operator=Ops_.PUSH,
                )
            if self.is_fleeting:
                gamestate.entity_man.set_attribute(
                    target=new_card,
                    attribute=AttrEnum.KEYWORDS,
                    value=KeywordEnum.FLEETING,
                    operator=Ops_.PUSH,
                )
        self.created_card = cards

        print(f"created card event: created:{cards}")

@define
class SimpleCreateCardEvent(BaseEvent):
    card_type: CardArchetype
    location: LocEnum
    owner: Player
    event: EntityEvents = field(default=EntityEvents.CREATE_CARD, init=False)

    def resolve(self, gamestate: GameState, *args, **kwargs):
        cards = gamestate.entity_man.create_card(
            cc=self.card_type,
            location=self.location,
            owner=self.owner,
            gamestate=gamestate,
        )
        print(f"created card event: created:{cards}")