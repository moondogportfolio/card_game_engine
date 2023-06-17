
from typing import Tuple
from attr import define, field
from actions.base_action import BaseAction
from card_classes.board_entity import BoardEntity


@define
class Landmark(BoardEntity):
    countdown_effect: Tuple[BaseAction] | None = field(default=None)  
