from attr import define
from actions.base_action import BaseTargetAction
from card_classes.cardarchetype import CardArchetype
from enums.operator import Ops_


@define
class GainStatsAndKeywords(BaseTargetAction):
    operator: Ops_
    source: CardArchetype