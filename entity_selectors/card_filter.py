from functools import partial
from random import choices
from typing import Any, Callable, List, Tuple
from attr import define, field
from card_classes.cardarchetype import CardArchetype
from classes.entity_selectors import EntitySelector
from classes.gamestate import GameState
from entity_selectors.base_card_filter import BaseCardFilter, BaseCardFilter
from enums.location import LocEnum
from enums.subtypes import SubTypes_
from enums.types import Types_

from resolvable_enums.target_player import TargetPlayer
from resolvers.target_player import target_player_resolver


@define(slots=False)
class SimpleCardFilter:
    """
    Filters by location in space.
    """

    owner: TargetPlayer | None = field(default=TargetPlayer.ORIGIN_OWNER)
    # card: LORCard = None
    index: int | Tuple[int] = field(default=None)
    location: LocEnum | Tuple[LocEnum, ...] = field(default=LocEnum.HOMEBASE)
    exclude_origin: bool = field(default=False)

    def filter_by_location(self, gamestate: GameState, origin):
        # if self.location is LocEnum.BOARD or isinstance(self.location, tuple):
        #     self.location = LocEnum.HOMEBASE
        if self.owner:
            owner = self.owner.resolve(gamestate, origin)
            cards = gamestate.loc_man.get_cards(self.location, owner)
        else:
            cards = []
            for player in gamestate.entity_man.players:
                x = gamestate.loc_man.get_cards(self.location, player)
                cards.extend(x)
        return [card.archetype for card in cards]

    def resolve(self, gamestate: GameState, origin):
        cards = self.filter_by_location(gamestate, origin)
        if self.exclude_origin:
            try:
                cards.remove(origin)
            except ValueError:
                pass
        return cards


@define(slots=False)
class CardFilter(BaseCardFilter, SimpleCardFilter):
    """
    is_exclusion - except this filter
    attack/health - if tuple, inclusive of both limits
    index - randint vs. range
    """

    top_x_cards: int | None = field(default=None)
    unique_class: bool = field(default=None, kw_only=True)
    custom_filter: Callable[[CardArchetype], bool] | None = field(
        default=None, kw_only=True
    )
    exclude_origin: bool = field(default=False)

    def card_satisfies_filter(self, card: CardArchetype) -> bool:
        ...

    def get_attributes_filter(self) -> List[Callable[[CardArchetype, Any], bool]]:
        def keyword_check(entity: CardArchetype, keyword):
            return entity.has_keyword(keyword)

        def type_check(entity: CardArchetype, type: Types_):
            return entity.is_type_instance(type)

        def attribute_filter(entity, attribute):
            entity_attr = getattr(entity, attribute)
            self_attr = getattr(self, attribute)
            if type(self_attr) is tuple:
                if self_attr[1] == 0:
                    return entity_attr >= self_attr[1]
                else:
                    return entity_attr <= self_attr[1] and entity_attr >= self_attr[0]
            else:
                return entity_attr == self_attr

        filters: Tuple[Any | None, Callable[[CardArchetype, Any], bool]] = (
            (self.attack, partial(attribute_filter, attribute="attack")),
            (self.health, partial(attribute_filter, attribute="health")),
            (self.cost, partial(attribute_filter, attribute="cost")),
            (self.type, partial(type_check, type=self.type)),
            (self.keyword, partial(keyword_check, type=self.keyword)),
        )
        return [
            filter_tuple[1] for filter_tuple in filters if filter_tuple[0] is not None
        ]
        # return list(filter(lambda x: x[0] is not None, filters))
        # return [
        #     card for card in cards if all(filter_obj[1](card) for filter_obj in filters)
        # ]

    def check_validity(self, gamestate: GameState, origin):
        return len(self.filter_by_location(gamestate, origin)) >= self.minimum

    def resolve(self, gamestate: GameState, origin):
        cards = self.filter_by_location(gamestate, origin)
        if self.exclude_origin:
            try:
                cards.remove(origin)
            except ValueError:
                pass
        return [
            card
            for card in cards
            if all(filter_obj(card) for filter_obj in self.get_attributes_filter())
        ]
        # cards = self.pare_return(cards)
        return cards


@define
class CardFilterSelector(CardFilter, EntitySelector):
    def resolve(self, gamestate: GameState, origin):
        cards = super().resolve(gamestate, origin)
        if self.sorter:
            self.sorter.resolve(cards)
            return cards[: self.quantity]
        else:
            return choices(cards, k=self.quantity)


@define
class SpellFilter(CardFilter):
    attack: None = field(init=False, default=None)
    health: None = field(init=False, default=None)
    type: None = field(init=False, default=Types_.SPELL)
    is_follower: None = field(init=False, default=Types_.SPELL)


@define
class StackSpellFilter(SpellFilter):
    location: LocEnum = field(init=False, default=LocEnum.SPELL_STACK)

    def resolve(self, gamestate: GameState, origin):
        return [
            qd_spell
            for qd_spell in gamestate.spell_stack_man.stack
            if all(
                filter_obj(qd_spell.spell)
                for filter_obj in self.get_attributes_filter()
            )
        ]


@define
class DrawCardFilter(CardFilter):
    location: LocEnum = field(init=False, default=LocEnum.DECK)


@define
class EntityFilter(CardFilter):
    player: TargetPlayer = field(default=None)
    ensure_player: bool = field(default=False)

    def resolve(self, gamestate: GameState, origin):
        cards = super().resolve(gamestate, origin)
        player = self.player.resolve(gamestate, origin)
        try:
            cards.extend(player)
        except:
            cards.append(player)
        return cards


@define
class BeholdingFilter(CardFilter):
    location: LocEnum = field(init=False, default=(LocEnum.DECK, LocEnum.HAND))
    type: Types_ | None = field(default=None, kw_only=True)
