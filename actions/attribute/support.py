from attr import define, field

from enums.keywords import KeywordEnum


@define
class SupportEffect:
    attack: int | None = field(default=None)
    health: int | None = field(default=None)
    keyword: KeywordEnum | None = field(default=None)
    round_ony: bool = field(default=False)