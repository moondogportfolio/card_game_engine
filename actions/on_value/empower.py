from typing import Any
from attr import define, field

from enums.keywords import KeywordEnum


@define
class EmpowerEffect:
    value: int
    keywords: KeywordEnum | None
    effect: Any = field(kw_only=True, default=None)
    