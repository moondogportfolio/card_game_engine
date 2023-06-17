

from random import choices
from typing import Any
from attr import define, field

from actions.base_action import BaseAction, BaseTargetAction
from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from enums.counters import TrapEnums
from enums.location import LocEnum
from enums.operator import Ops_
from resolvable_enums.target_player import TargetPlayer




@define
class TrapMultiplier(BaseTargetAction):
    multiplier: int = 2
    trap: TrapEnums = TrapEnums.POISON_PUFFCAP
    entire_deck: bool = True
    target: TargetPlayer = field(default=TargetPlayer.ORIGIN_OWNER, kw_only=True)

    def resolve(self, gamestate: GameState, origin):
        cards = gamestate.loc_man.get_cards(LocEnum.DECK, origin.owner)
        for card in cards:
            gamestate.counter_man.set_trap(
                entity=card,
                trap=self.trap,
                quantity=self.multiplier,
                operator=Ops_.MULTIPLY,
            )


@define
class SetTrapEffect(BaseTargetAction):
    quantity: int = 1
    trap: TrapEnums = TrapEnums.POISON_PUFFCAP
    operator: Ops_ = field(default=Ops_.INCREMENT, kw_only=True)
    each: bool = False
    top_x_cards: int = field(default=False, kw_only=True)
    entire_deck: bool = field(default=True, kw_only=True)
    target: TargetPlayer | None = field(default=TargetPlayer.OPPONENT, kw_only=True)
    target_cards: Any = field(default=None, kw_only=True)
    
    def resolve(self, gamestate: GameState, origin: CardArchetype):
        player = gamestate.entity_man.get_opponent(origin.owner)
        targets = gamestate.loc_man.get_cards(LocEnum.DECK, player, self.top_x_cards or None)
        targets = choices(targets, k=self.quantity)
        for target in targets:
            gamestate.counter_man.set_trap(
                entity=target,
                trap=self.trap,
                quantity=self.quantity,
                operator=self.operator,
            )

@define
class PlantPuffcaps(SetTrapEffect):
    # target_cards: Any = field(default=None, kw_only=False)
    trap: TrapEnums = field(default=TrapEnums.POISON_PUFFCAP, init=False)

@define
class PlantFlashBombTrap(SetTrapEffect):
    trap: TrapEnums = field(default=TrapEnums.FLASHBOMB_TRAP, init=False)
    top_x_cards: int = field(default=8, kw_only=True)
    entire_deck: bool = field(default=False, kw_only=True)

    
@define
class PlantMysteriousPortalEffect(SetTrapEffect):
    trap: TrapEnums = field(init=False, default=TrapEnums.MYSTERIOUS_PORTAL)
    top_x_cards: int = field(default=4)
    entire_deck: bool = field(default=False, kw_only=True)
    target: TargetPlayer = field(kw_only=True, default=TargetPlayer.ORIGIN_OWNER)


@define
class PlantChimes(SetTrapEffect):
    trap: TrapEnums = field(init=False, default=TrapEnums.CHIME)
    top_x_cards: int = field(default=1)
    entire_deck: bool = field(default=False, kw_only=True)
    target: TargetPlayer = field(kw_only=True, default=TargetPlayer.ORIGIN_OWNER)


@define
class ActivateBoons:
    top_x_cards: int