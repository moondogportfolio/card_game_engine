from attr import define
from actions.base_action import BaseAction

from resolvable_enums.player_conditions import PlayerFlags


@define
class OnceYouve:
    state: PlayerFlags
    action: BaseAction