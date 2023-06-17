
from random import choice, shuffle
from typing import List

from card_classes.cardslot import CardSlot

class Card:
    ...


class Location:

    __slots__ = ("cards", "_size")

    def __init__(self, size: int = 0) -> None:
        self.cards: List[CardSlot] = []
        self._size = size

    def get_empty_spaces(self):
        if self._size == 0:
            return None
        return self._size - len(self.cards)

    def get_size(self):
        return self.cards.__len__()

    def add_card(self, card: Card) -> int:
        self.cards.append(card)
        return len(self.cards) - 1

    def replace_card(self, card, replacement):
        index = self.cards.index(card)
        self.cards.remove(card)
        self.cards.insert(index, replacement)

    def insert_card(self, card: Card, index: int, random_index: bool = None):
        loc = self.cards
        if random_index:
            index = choice(len(self.cards))
        if index >= len(self.cards):
            loc[len(loc) : index] = [None] * (index - len(loc))
            loc.append(card)
        else:
            self.cards.insert(index, card)
        return index

    def set_card_at_index(self, card: Card, index: int):
        self.cards[index] = card
        return card

    def remove_card(self, card):
        try:
            idx = self.cards.index(card)
            self.cards.pop(idx)
            return idx
            for idx, internal_card in enumerate(self.cards):
                if internal_card.id == card.id:
                    self.cards.pop(idx)
                    return idx
        except ValueError:
            # raise CardNotInLocationException("Owner does not have card in location.")
            ...

    def shuffle(self):
        shuffle(self.cards)

    def set_size(self, int):
        self._size = int

    def get_card(self, index):
        return self.cards[index]

    def get_index(self, card: Card):
        return self.cards.index(card)

    def is_full(self):
        """
        Size 0 is infinite size.
        """
        if self._size == 0:
            return False
        return True if self.cards.__len__() >= self._size else False
