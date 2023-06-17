
from attr import define

from entity_selectors.card_filter import CardFilter


@define
class CardCounter:
    cards: CardFilter