from typing import Any
from attr import define, field
from actions.base_action import BaseAction, BaseTargetAction
from actions.movement.summon import SummonEffect, SummonEvent

from card_classes.cardarchetype import CardArchetype
from card_classes.equipment import Equipment
from card_classes.landmark import Landmark
from card_classes.spell import Spell
from card_classes.unit import Unit
from classes.gamestate import GameState
from entity_selectors.card_filter import CardFilter
from entity_selectors.input import Input
from enums.entity_events import EntityEvents
from enums.location import LocEnum
from events.base_event import BaseTargetEvent
from resolvable_enums.active_cards_selector import TargetShorthand


play_card_target = Input(choices=CardFilter(location=LocEnum.HAND, card_type=None))


@define
class PayCost(BaseAction):
    card: CardArchetype


move_effect = SummonEffect(target=...)


@define
class PlayCardEffect(BaseTargetAction):
    target: Input = field(init=False, default=play_card_target)

    # def resolve_params(self, gamestate: GameState):
    #     super().resolve_params(gamestate)
    #     target: CardArchetype
    #     for target in self.target:

    #         ...

    def resolve(self):
        '''
        get event
        '''
        return PlayCardEvent(event=EntityEvents.PLAY)

    # def resolve(self, gamestate: GameState):
    #     # PAY COST
    #     # REQUIREMENTS
    #     if isinstance(self.target, (Unit, Landmark)):
    #         summon = SummonEffect(target=self.target)
    #         gamestate.stack_manager.add_to_queue(summon, self.action_origin)
    #         gamestate.stack_manager.add_to_queue(
    #             self.target.play_effect, self.action_origin
    #         )

    # for effect in self.target.get_internal_event(EntityEvents.PLAY):
    #     gamestate.stack_manager.add_to_tail(effect, self.target)


@define
class PlayEquip(BaseTargetAction):
    bearer: CardFilter = field(init=False, default=TargetShorthand.ALLIED_BOARD_UNIT)
    target: CardFilter = field(init=False, default=TargetShorthand.HAND_EQUIPMENT)

    def check_target_validity(self, gamestate: GameState):
        bearer_val = self.bearer.check_validity(gamestate, self.action_origin)
        return super().check_target_validity(gamestate) and bearer_val

    def resolve(self, gamestate: GameState, origin: Any):
        return super().resolve(gamestate, origin)


@define
class PlayCardEvent(BaseTargetEvent):
    def resolve(self, gamestate: GameState, origin: CardArchetype, target):
        if isinstance(target, Spell):
            return PlaySpellEvent(event=EntityEvents.PLAY_UNIT)
        elif isinstance(target, Unit):
            return PlayUnitEvent(event=EntityEvents.PLAY_UNIT, target=target)
        else:
            return PlayLandmarkEvent(event=EntityEvents.PLAY_LANDMARK)


@define
class PlaySpellEvent(BaseTargetEvent):
    def resolve(self, gamestate: GameState, origin: CardArchetype, target):
        print('OK')
        return super().resolve(gamestate, origin, target)


@define
class PlayUnitEvent(BaseTargetEvent):
    def resolve(self, gamestate: GameState, origin: CardArchetype, target):
        return SummonEvent(destination=LocEnum.HOMEBASE, target=target)




@define
class PlayLandmarkEvent(BaseTargetEvent):
    def resolve(self, gamestate: GameState, origin: CardArchetype, target):
        return SummonEvent(destination=LocEnum.HOMEBASE)
