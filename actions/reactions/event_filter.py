
from enum import Enum
from attr import define, field

from actions.base_action import BaseAction
from enums.origin_enum import OriginEnum


@define
class EventFilter:
    """
    :param on_board_effect - will only trigger if source is on the board
    """
    event: Enum
    # action_filter: BaseAction
    origin: OriginEnum | None = field(default=None)
    target: OriginEnum | None = field(default=None)
    self_event: bool = field(default=False)
    on_board_only: bool = field(default=True)

    def check_if_satisfies_event(self, action: BaseAction) -> bool:
        return True