from typing import Any, Tuple
from attr import define, field
from actions.base_action import BaseAction, BaseTargetAction
from card_classes.unit import Unit
from classes.gamestate import GameState
from entity_selectors.card_filter import EntityFilter

from entity_selectors.target_game_card import TargetEntity
from enums.keywords import KeywordEnum
from enums.location import LocEnum
from events.attribute.add_keyword_event import AddKeywordEvent
from events.attribute.damage_event import DamageEvent
from events.attribute.frostbite import FrostbiteEvent
from events.base_event import BaseEvent
from events.movement.discard_event import DiscardEvent
from events.movement.draw_event import DrawEvent
from events.movement.swap_event import SwapPositionsEvent
from resolvable_enums.target_player import TargetPlayer


# Swap 2 allies. Give them Barrier this round.
@define
class StandUnitedEffect(BaseTargetAction):
    def resolve(self, target, *args, **kwargs):
        target, target2 = target[0], target[1]
        event1 = SwapPositionsEvent(target=target, destination=target2)
        event2 = AddKeywordEvent(target=(target, target2), value=KeywordEnum.BARRIER)
        return (event1, event2)


# Deal 4 to an enemy if it has 0 Power. Otherwise, Frostbite it.
@define
class ShatterEffect(BaseTargetAction):
    def resolve(
        self, target: Unit, gamestate: GameState, origin: Any, *args, **kwargs
    ) -> BaseEvent:
        if target.attack == 0:
            return DamageEvent(value=4, target=target)
        else:
            return FrostbiteEvent(target=target)


@define
class RummageEffect(BaseTargetAction):
    def resolve(
        self, target, gamestate: GameState, origin, *args, **kwargs
    ) -> BaseEvent | Tuple[BaseEvent]:
        event1 = DiscardEvent(target=target)
        cards = gamestate.loc_man.get_cards(
            LocEnum.DECK,
            player=origin.owner,
            top_x_cards=event1.get_target_len(),
        )
        event2 = DrawEvent(target=cards)
        return (event1, event2)


@define
class TrueshotBarrageEffect(BaseTargetAction):
    target: TargetEntity = field(
        init=False,
        default=TargetEntity(
            quantity=3,
            minimum=1,
            choices=EntityFilter(
                owner=TargetPlayer.OPPONENT, player=TargetPlayer.OPPONENT
            ),
        ),
    )

    def resolve(self, target, *args, **kwargs):
        if isinstance(target, tuple):
            return [
                DamageEvent(value=3 - idx, target=subtarget)
                for idx, subtarget in enumerate(target)
            ]
        else:
            return DamageEvent(value=3, target=target)


@define
class HeartoftheFluftEffect(BaseAction):
    def resolve(self, gamestate: GameState, origin: Any):
        return super().resolve(gamestate, origin)
