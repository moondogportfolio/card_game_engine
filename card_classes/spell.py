from typing import List, Tuple
from attr import define, field
from actions.activations.alternative_effect import AlternativeActivationEffect
from actions.base_action import BaseAction, BaseTargetAction

from card_classes.cardarchetype import CardArchetype
from enums.spell_speed import SpellSpeedEnum


def activation_converter(value):
    if type(value) is tuple:
        return value
    else:
        return (value, )

@define(repr=False)
class Spell(CardArchetype):
    activation_effect: Tuple[BaseAction, ...] = field(kw_only=True, converter=activation_converter)
    activation_targets: List | None = field(default=None)
    spell_speed: SpellSpeedEnum = field(init=False)
    alternative_effect: AlternativeActivationEffect | None = field(kw_only=True, default=None)
    
    
    def __repr__(self) -> str:
        return f'SPELL {self.id} {self.name} {self.location} {self.owner}'
