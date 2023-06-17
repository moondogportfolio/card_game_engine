
from dataclasses import dataclass
from typing import Any

from enums.attribute import AttrEnum



@dataclass
class EntityAttribute:
    target: Any
    attribute: AttrEnum