from json import load
import re
from typing import Dict, List

from data.JSONCard import JsonCard


pattern = re.compile("\W")
directory = "./data/datasets/set7.json"


with open(directory, "r", encoding="utf-8") as source:
    print(source)
    cards: List[JsonCard] = load(source)
    for card in cards:
        if card["type"] != 'Spell':
            continue
        print(f'\n\n#{card["descriptionRaw"]}')
        card_name = re.sub(pattern, "", card["name"])
        print(f'def {card_name}():')
        print('\teffect = ...')
        print('\treturn Spell(activation_effect = effect)')
