
from attr import define

from custom_types.resolvables import ResolvableEntity


@define
class DeclareGameResult:
    winner: ResolvableEntity | None

