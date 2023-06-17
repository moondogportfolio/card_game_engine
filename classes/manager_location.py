from collections import defaultdict
from enum import Enum
from typing import Dict, List, Tuple
from card_classes.cardslot import CardSlot
from card_classes.unit import Unit
from classes.location import Location
from decorators.multitarget import multitarget

from entity_classes.player import Player
from enums.location import LocEnum


class LocationManager:
    def __init__(self) -> None:
        #TODO setting for default locations
        self._locations = defaultdict(lambda: Location())


    def get_card(self, location: Enum, player: Player, index:int):
        return self._locations[(location, player.id)].get_card(index)

    def get_cards(self, location: Enum, player: Player, top_x_cards: int | None = None):
        cards = self._locations[(location, player.id)].cards
        if top_x_cards:
            return cards[:top_x_cards]
        else:
            return cards
        
    def get_board_units(self, player: Player) -> List[Unit]:
        ret_val = []
        for loc in (LocEnum.HOMEBASE, LocEnum.BATTLEFIELD):
            ret_val.extend(card.archetype for card in self._locations[(loc, player.id)].cards)
        return ret_val

    def get_location_obj(self, location: Enum, player: Player) -> Location:
        return self._locations[(location, player.id)]

    def create_location(self, location: Enum, player: Player, size: int = 0):
        location_tuple = (location, player.id)
        if location_tuple in self._locations:
            # raise LocationError
            ...
        else:
            self._locations[location_tuple] = Location(size)

    def swap_cards(self, card1: CardSlot, card2: CardSlot):
        try: #target is card archetype
            card1 = card1.cardslot
        except AttributeError:
            ...
        try: #target is card archetype
            card2 = card2.cardslot
        except AttributeError:
            ...
        #TODO index
        old_c1_data = card1.location
        old_c2_data = card2.location
        c1_lo = self._locations[(card1.location, card1.owner.id)]
        c2_lo = self._locations[(card2.location, card2.owner.id)]
        c1_lo.replace_card(card1, card2)
        c2_lo.replace_card(card2, card1)
        card1.location = old_c2_data
        card2.location = old_c1_data
        print(f'{card1}: {old_c1_data} > {old_c2_data}')
        print(f'{card2}: {old_c2_data} > {old_c1_data}')

    @multitarget
    def move_card(
        self,
        new_location: Enum,
        player: Player = None,
        *,
        target,
        index: int | None = None,
        random_index: bool = False,
        spawn: bool = False,
    ):
        """
        1.	Remove card from current location. (If not spawn.)
        2.	Recompute indices of cards on old location.
        3.	Add to new location, taking mind of index in relation to other cards.
        4.	Recompute indices of cards on new location.
        """
        # TODO Player
        try: #target is card archetype
            target = target.cardslot
        except AttributeError:
            ...
        if not player:
            player = target.owner
        new_location_obj = self._locations[(new_location, player.id)]
        if not spawn:
            old_location_obj = self._locations[(target.location, player.id)]
            old_index = old_location_obj.remove_card(target)
            old_location = target.location
            if index != None or random_index:
                index = new_location_obj.insert_card(
                    target, index=index, random_index=random_index
                )
            else:
                index = new_location_obj.add_card(target)
            print(f"{target} {old_location}:{old_index} > {new_location}:{index}")
        else:
            index = new_location_obj.add_card(target)
            target.index = index
        target.location = new_location
        # await card.execute_set_attribute(Attr_.LOCATION, new_location)
        # await card.execute_set_attribute(Attr_.INDEX, index)
        # # 4
        # # recompute indices
        # for card in self._locations[new_location].cards[index + 1 :]:
        #     await card.execute_set_attribute(Attr_.INDEX, card.index + 1)
        # await card.move_effects(old_location, new_location, spawn)
