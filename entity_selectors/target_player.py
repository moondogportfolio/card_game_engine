
from typing import Any, List
from attr import define, field
from entity_selectors.card_filter import CardFilter

from entity_selectors.input import Input
from resolvable_enums.target_player import TargetPlayer


@define
class TargetPlayerInput(Input):
    choices: TargetPlayer
    entity_pool: List | None = field(default=None, init=False)
    exclusion: Any = field(default=None, init=False)
