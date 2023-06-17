from attr import define
from actions.reactions.dynamic_attr_modifier import DynamicAttributeModifier

from actions.reactions.triggered_action import TriggeredAction
from custom_types.resolvables import ResolvableEntity


@define
class CreateDynamicValue:
    target: DynamicAttributeModifier
    bind_to: ResolvableEntity