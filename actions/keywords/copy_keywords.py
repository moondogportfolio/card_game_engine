from attr import define, field
from actions.base_action import BaseTargetAction
from custom_types.resolvables import ResolvableEntity


@define
class CopyKeywords(BaseTargetAction):
    source: ResolvableEntity
    positive_only: bool = field(default=True, kw_only=True)
    round_only: bool = field(default=False, kw_only=True)