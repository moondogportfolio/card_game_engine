from typing import Any, Tuple
from attr import define
from actions.base_action import BaseAction, BaseTargetAction
from classes.gamestate import GameState

from entity_selectors.card_filter import StackSpellFilter
from enums.entity_events import EntityEvents
from enums.spell_speed import SpellSpeedEnum
from events.activations.negate_qd_spell import NegateQueuedSpellEvent


@define
class NegateSpell(BaseTargetAction):

    def resolve(self, target, gamestate: GameState, origin: Any):
        return NegateQueuedSpellEvent(target=target, event=EntityEvents.NEGATE_SPELL)