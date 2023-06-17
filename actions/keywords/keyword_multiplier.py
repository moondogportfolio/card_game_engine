from attr import define

from actions.base_action import BaseTargetAction
from enums.keywords import KeywordEnum


@define
class MultiplyKeywordValue(BaseTargetAction):
    keyword: KeywordEnum
    multiplier: int
