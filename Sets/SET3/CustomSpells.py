from typing import Any, Tuple
from attr import define
from actions.attribute.buff import BuffEffect
import Sets.SET1.Units as Set1Units
from actions.base_action import BaseAction
from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from enums.location import LocEnum
from events.base_event import BaseEvent
from events.create.CreateCardEvent import CreateCardEvent
from value.player_statistic import PlayerStatistic


@define
class ForTheFallenEffect(BaseAction):
    def resolve(
        self, gamestate: GameState, origin: CardArchetype, *args, **kwargs
    ) -> BaseEvent | Tuple[BaseEvent]:
        val = origin
        #todo playerstatistic
        return CreateCardEvent(
            target=Set1Units.DauntlessVanguard,
            owner=origin.owner,
            location=LocEnum.HOMEBASE,
            quantity=PlayerStatistic.ALLY_DIED_THIS_GAME.resolve(),
        )


# Grow all allies' Power and Health to the highest Power or Health among allies.
# Grant all allies allied keywords.
@define
class GiveItAllEffect(BaseAction):
    def resolve(
        self, gamestate: GameState, origin: CardArchetype, *args, **kwargs
    ) -> BaseEvent | Tuple[BaseEvent]:
        board_units = gamestate.loc_man.get_board_units(origin.owner)
        max_val = 0
        keyword = set()
        for card in board_units:
            keyword.update(card.keywords)
            if card.health > max_val:
                max_val = card.health
            if card.attack > max_val:
                max_val = card.attack
        return BuffEffect(target=board_units, attack=max_val, health=max_val)
