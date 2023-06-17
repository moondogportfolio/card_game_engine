from __future__ import annotations
from collections import deque
from typing import TYPE_CHECKING, Deque, Dict, List, Tuple

from attr import Attribute, define, field, fields
from actions.branching.branching_action import BranchingAction
from decorators.multitarget import multitarget
from entity_classes.player import Player
from entity_selectors.input import Input

from enums.location import LocEnum
from actions.base_action import BaseTargetAction

if TYPE_CHECKING:
    from card_classes.spell import Spell
    from events.base_event import BaseEvent
    from classes.gamestate import GameState


@define
class TargetCoords:
    index: int
    location: LocEnum
    player: Player

    def get_card(self, gamestate: GameState):
        return gamestate.loc_man.get_card(
            self.location,
            self.player,
            self.index,
        ).archetype


@define
class QueuedSpell:
    spell: Spell
    effect_target_pair: Dict[int, List[TargetCoords]] | None
    negated: bool = field(default=False, init=False)


class SpellStackManager:
    def __init__(self) -> None:
        self.stack: Deque[QueuedSpell] = deque()

    @multitarget
    def remove_from_q(self, target: QueuedSpell):
        target.negated = True
        print(f"removed queued spell {target}")

    async def add_to_q(self, spell: Spell, gamestate: GameState):
        target_tuple_dict = {}
        qd_spell = QueuedSpell(spell=spell, effect_target_pair=None)
        for idx, action in enumerate(spell.activation_effect):
            if isinstance(action, BaseTargetAction):
                target_coords_list = []
                for target_obj in action.get_target_objects():
                    if isinstance(target_obj, Input):
                        resolved_choices = target_obj.choices.resolve(gamestate, spell)
                        target = await gamestate.input_manager.manual_input(
                            target_obj, resolved_choices
                        )
                        target_coords_list.append(target)
                    else:
                        target_coords_list.append(target_obj)
                target_tuple_dict[idx] = target_coords_list
        if target_tuple_dict:
            qd_spell.effect_target_pair = target_tuple_dict
        self.stack.appendleft(qd_spell)

    def resolve_stack(self, gamestate: GameState):
        for qd_spell in self.stack:
            if qd_spell.negated:
                continue
            effect_event_pair: Dict[int, BaseEvent] = {}
            for idx, action in enumerate(qd_spell.spell.activation_effect):
                coevent = None
                if action.coevent:
                    for subaction_index, subaction in enumerate(
                        qd_spell.spell.activation_effect
                    ):
                        if action.coevent == subaction:
                            coevent = effect_event_pair.get(subaction_index)
                            break
                if not action.resolve_condition(gamestate, qd_spell.spell, postevent=coevent):
                    continue
                # if action.fizz_if_fail and action.fizz_if_fail:
                #     ...
                #     #TODO
                if isinstance(action, BranchingAction):
                    action = action.resolve(gamestate, qd_spell.spell)
                if isinstance(action, BaseTargetAction):
                    target_coords_list = []
                    unresolved_target_coords = qd_spell.effect_target_pair.get(idx)
                    for target_obj in unresolved_target_coords:
                        if isinstance(target_obj, TargetCoords):
                            entity = target_obj.get_card(gamestate)
                        elif isinstance(target_obj, list):
                            entity = []
                            for subtarget in target_obj:
                                try:
                                    entity.append(subtarget.get_card(gamestate))
                                except AttributeError:  # target is player
                                    entity.append(subtarget)
                        elif (
                            isinstance(target_obj, (Player, QueuedSpell))
                            or target_obj == "pass"
                        ):
                            entity = target_obj
                        else:
                            entity = target_obj.resolve(
                                gamestate=gamestate,
                                origin=qd_spell.spell,
                                postevent=coevent,
                            )
                        target_coords_list.append(entity)

                    event = gamestate.event_man.resolve_action(
                        action, gamestate, qd_spell.spell, *target_coords_list
                    )

                else:
                    event = gamestate.event_man.resolve_action(
                        action, gamestate, qd_spell.spell
                    )
                effect_event_pair.update({idx: event})
