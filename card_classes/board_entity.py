from typing import List
from attr import define, field
from actions.base_action import BaseAction
from card_classes.cardarchetype import CardArchetype


@define
class BoardEntity(CardArchetype):
    summon_effect: List[BaseAction] | None = field(default=None) 
    last_breath_effect: List[BaseAction] | None = field(default=None)
    play_plunder: BaseAction | None = field(default=None, kw_only=True)
    play_daybreak: BaseAction | None = field(default=None, kw_only=True)
    play_nightfall: BaseAction | None = field(default=None, kw_only=True)
    summon_allegiance_effect: BaseAction | None = field(default=None, kw_only=True)
