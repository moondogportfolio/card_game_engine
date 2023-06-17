from attr import define

from actions.base_action import BaseTargetValueAction
from events.attribute.damage_event import DamageEvent
from events.attribute.spell_overwhelm_event import SpellOverwhelmEvent


@define
class DamageEffect(BaseTargetValueAction):
    def resolve(self, target, *args, **kwargs):
        return DamageEvent(value=self.value, target=target)


@define
class SpellOverwhelmEffect(BaseTargetValueAction):
    def resolve(self, target, *args, **kwargs):
        return SpellOverwhelmEvent(value=self.value, target=target)
