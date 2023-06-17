from typing import Any, List
from attr import define, field
from custom_types.converters import shortcut_enum_converter
from custom_types.resolvables import ShortcutEnum
from entity_selectors.card_filter import CardFilter, StackSpellFilter

from entity_selectors.input import Input
from enums.card_sorters import CardSorter


@define
class TargetEntity(Input):
    choices: CardFilter | ShortcutEnum = field(
        factory=CardFilter,
        converter=shortcut_enum_converter,
    )
    entity_pool: List | None = field(default=None)
    exclusion: Any = field(default=None, kw_only=True)
    sorter: CardSorter | None = field(kw_only=True, default=None)
