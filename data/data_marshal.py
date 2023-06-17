from __future__ import annotations
from importlib import import_module
import pickle
import re
from typing import TYPE_CHECKING, Dict, List, Type

from attr import define
from json import load

from data.JSONCard import JsonCard

dataset_location = './data/datasets'

class NotImplementedError(Exception):
    def __init__(self, card_data: JsonCard, *args: object) -> None:
        self.card_data = card_data
        super().__init__(*args)

    def msg(self):
        print(self.card_data["name"], self.card_data["cardCode"])


pattern = re.compile("\W")
cardcode_json_dict: Dict[str, JsonCard] = {}
name2cardcode: Dict[str, str] = {}


def _re_init_cards():
    for set_number in range(1, 8):
        for card in _load_cards(set_number):
            card_name = card["name"]
            card_name = re.sub(pattern, "", card_name)
            cardcode_json_dict[card["cardCode"]] = card
            name2cardcode[card_name] = card["cardCode"]
    with open(f'{dataset_location}/cc', "wb+") as file:
        pickle.dump(cardcode_json_dict, file)
    with open(f'{dataset_location}/n2cc', "wb+") as file:
        pickle.dump(name2cardcode, file)


def _load_cards(set_number: int) -> List:
    """
    Returns JSON file.
    """
    with open(f"{dataset_location}/set{set_number}.json", encoding="utf8") as json_file:
        return load(json_file)


def init(reinit=False):
    if reinit:
        _re_init_cards()
        return
    with open(f'{dataset_location}/cc', "rb") as file:
        cardcode_json_dict.update(pickle.load(file))
    with open(f'{dataset_location}/n2cc', "rb") as file:
        name2cardcode.update(pickle.load(file))


def cardcode2jsoncard(card_code: str) -> JsonCard:
    return cardcode_json_dict[card_code]


# def get_card_database():
#     return _cards


# def check_implementation(set_number: int):
#     for card in _load_cards(set_number):
#         x = import_card(card)
#         # try:
#         # except Exception as e:
#         #     print(e.msg)


def import_card(card: JsonCard = None):
    card_name = card["name"]
    card_name = re.sub(pattern, "", card_name)
    if card["rarity"] == "Champion":
        card_type = "Champions"
    elif card["type"] == "Ability":
        card_type = "Skills"
    else:
        card_type = card["type"] + "s"
    card_set = card["set"].upper()
    module_name = f"Sets.{card_set}.{card_type}"
    module_pkg = f"{card_name}"
    try:
        return getattr(import_module(module_name), module_pkg)
    except AttributeError:
        print(card["name"], card["cardCode"])
        # raise NotImplementedError(card)


# def class2jsondata(class_obj: type):
#     cardname = re.sub(pattern, "", class_obj.__name__)
#     try:
#         cardcode = _name2cardcode[cardname]
#         data = _cards[cardcode]
#         return data
#     except KeyError:
#         raise NotImplementedError(f"Check name of class {class_obj.__name__}.")

init(reinit=True)