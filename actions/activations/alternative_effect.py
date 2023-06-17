from attr import define, field

from actions.base_action import BaseAction


@define
class AlternativeActivationEffect:
    activation_effects: BaseAction
    spell_cost: int
    mana_cost: int | None = field(kw_only=True, default=None)