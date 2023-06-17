

from typing import Any, Callable, List, Tuple, Type
from attr import define, field
from actions.create.base_create import BaseCreateCardEffect


@define
class CreateCardEffect(BaseCreateCardEffect):
    attachment: Any | None = field(kw_only=True, default=None)
    """
    target:
        ManifestEffect - will get selected card
        AcquireChoice - will get selected card
    cost/attack/health - when given int, will set to that value
    index - if tuple, will select randomly. to select from bottom of deck, use (-X, 0)
    :param cost - if int, will set cost to that value
    """

    