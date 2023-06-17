from enum import Enum, auto
from typing import Any, List, Tuple
from attr import define, field
from actions.base_action import BaseAction, BaseTargetAction
from events.movement.MovementEvent import MovementEvent

from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from entity_selectors.card_filter import DrawCardFilter
from enums.attribute import AttrEnum
from enums.entity_events import EntityEvents
from enums.location import LocEnum
from enums.operator import Ops_
from events.attribute.SetAttributeEvent import SetAttributeEvent
from events.base_event import BaseEvent, BaseTargetEvent
from resolvable_enums.target_player import TargetPlayer


@define
class TargetedDrawAction(BaseTargetAction):
    def resolve(self, target, *args, **kwargs):
        return MovementEvent(
            event=EntityEvents.DRAW, destination=LocEnum.HAND, target=target
        )


@define
class DrawEffect(BaseAction):
    """
    :param quantity - if passed value, will draw top x cards from deck
    :param target - if passed value, will draw specific cards from deck, and disregard quantity if any
    assumes drawing player draws from own deck
    """

    quantity: int = 1
    is_fleeting: bool = False
    player: TargetPlayer = field(default=TargetPlayer.ORIGIN_OWNER, kw_only=True)
    cost_reduction: int | None = None
    filter_obj: DrawCardFilter | None = field(default=None)
    # event: Enum = field(init=False, default=EntityEvents.DRAW)

    def resolve(self, gamestate: GameState, origin: Any, *args, **kwargs):
        player = self.player.resolve(gamestate, origin)
        if self.filter_obj:
            cards = self.filter_obj.resolve(gamestate, origin)
            cards = cards[0]
            #TODO
        else:
            cards = gamestate.loc_man.get_cards(LocEnum.DECK, player, self.quantity)
        event1 = MovementEvent(
            event=EntityEvents.DRAW, destination=LocEnum.HAND, target=cards
        )
        if self.cost_reduction:
            cards = [card.archetype for card in cards]
            event2 = SetAttributeEvent(
                target=cards,
                event=None,
                attribute=AttrEnum.COST,
                value=self.cost_reduction,
                operator=Ops_.DECREMENT,
            )
            return event1, event2
        return event1
    

        def execute(cards, player):
            for idx, card in enumerate(cards):
                if idx >= self.quantity:
                    break
                gamestate.loc_man.move_card(
                    card, new_location=LocEnum.HAND, player=player
                )
                if self.cost_reduction:
                    gamestate.entity_man.set_attribute(
                        target=card.archetype,
                        attribute=AttrEnum.COST,
                        value=self.cost_reduction,
                        operator=Ops_.DECREMENT,
                    )

        player = self.player
        location_getter = gamestate.loc_man.get_location_obj
        drawn_cards = []
        if isinstance(player, List):
            for p in player:
                execute(location_getter(LocEnum.DECK, p).cards, p)
        else:
            execute(location_getter(LocEnum.DECK, player).cards, player)


@define
class DrawSpecificReturnRestEffect(DrawEffect):
    top_x_cards: int | None = field(default=None)
