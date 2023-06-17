from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Protocol, Tuple, Type
from card_classes.cardslot import CardSlot

from decorators.multitarget import multitarget
from entity_classes.player import Player
from enums.attribute import AttrEnum
from enums.keywords import KeywordEnum
from enums.location import LocEnum
from enums.operator import Ops_

if TYPE_CHECKING:
    from card_classes.cardarchetype import CardArchetype

card_cc_pair = {}

class CreateCardModifier(Protocol):
    is_fleeting: bool
    is_ephemeral: bool
    with_my_stats_source: Any
    with_my_stats_keywords_source: Any
    attack: int | Tuple[Ops_, int]
    cost: int | Tuple[Ops_, int]
    health: int | Tuple[Ops_, int]
    keywords: KeywordEnum | List[KeywordEnum]

class EntityManager:
    def __init__(self) -> None:
        self.players = []
        self.cards: List[CardArchetype] = []
        self.card_slots = []
        self.arche_slot: Dict[int, CardSlot] = {}

    def get_opponent(self, player):
        for x in self.players:
            if x.id != player.id:
                return x

    def create_player(
        self,
        health: int,
        mana: int,
        mana_gem: int,
        spell_mana: int,
        is_ai: bool = False,
    ) -> Player:
        player_id = len(self.players)
        player = Player(
            id=player_id,
            health=health,
            mana=mana,
            mana_gem=mana_gem,
            spell_mana=spell_mana,
            rally=False,
            deckcode="",
        )
        self.players.append(player)
        return player

    @multitarget
    def set_attribute(
        self,
        target,
        attribute: AttrEnum,
        value,
        operator: Ops_,
        broadcast: bool = True # CREATE CARD CAN SET ATTRIBUTE WITHOUT BROADCASTING CHANGES
    ):
        attribute = attribute.name.lower()
        if operator is Ops_.PULL:
            ...
        if operator is Ops_.PUSH:
            container: List = getattr(target, attribute)
            try:
                container.extend(value)
            except TypeError:
                container.append(value)
            print(target, attribute, container, value)  
        else:  
            old_value = getattr(target, attribute)
            new_value = operator.compute(old_value, value)
            setattr(target, attribute, new_value)
            print(target, attribute, old_value, new_value)
            return old_value, new_value

    def create_deck(self, deckcode: str, player, gamestate, cc=None):
        for _ in range(40):
            self.create_card(cc, LocEnum.DECK, player, gamestate)

    def create_card(
        self,
        cc: Callable[[None], CardArchetype] | CardArchetype,
        location,
        owner,
        gamestate,
        quantity: int = 1,
        index: int | None = None
    ) -> List:
        created = []
        for _ in range(quantity):
            try:
                new_card = cc()
                name = cc.__name__
                card_cc_pair.update({name:cc})
                new_card.name = name
            except TypeError: #new_card not callable
                cc = card_cc_pair.get(cc.name)
                new_card = cc()
                new_card.name = cc.__name__
            new_card.id = len(self.cards)
            slot = CardSlot(id=len(self.card_slots), archetype=new_card, owner=owner)
            new_card.cardslot = slot
            self.cards.append(new_card)
            self.card_slots.append(slot)
            gamestate.loc_man.move_card(
                new_location=location, player=owner, target=slot, spawn=True
            )
            created.append(new_card)
            self.arche_slot[new_card.id] = slot               

        return created

    def get_slot_for_arche(self, archetype: CardArchetype):
        return self.arche_slot[archetype.id]
