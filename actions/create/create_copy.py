from typing import Any, Callable, List, Tuple, Type

from attr import define, field
from actions.base_action import BaseTargetAction
from enums.attribute import AttrEnum
from events.create.CreateCardEvent import CreateCardEvent
from classes.gamestate import GameState
from enums.entity_events import EntityEvents
from enums.keywords import KeywordEnum
from enums.location import LocEnum
from enums.operator import Ops_
from resolvable_enums.target_player import TargetPlayer


@define
class CreateCopyEffect(BaseTargetAction):
    """
    target:
        ManifestEffect - will get selected card
        AcquireChoice - will get selected card
    cost/attack/health - when given int, will set to that value
    index - if tuple, will select randomly. to select from bottom of deck, use (-X, 0)
    :param cost - if int, will set cost to that value
    """
    location: LocEnum = field(default=LocEnum.HAND)
    owner: TargetPlayer | None = field(default=TargetPlayer.ORIGIN_OWNER)
    quantity: int = field(default=1)
    is_fleeting: bool = field(default=None)
    is_ephemeral: bool = False
    index: int | Tuple[int, int] | None = field(default=None)
    with_my_stats_source: Any = field(default=None)
    with_my_stats_keywords_source: Any = field(default=None)
    attack: int | Tuple[Ops_, int] = field(default=None)
    cost: int | Tuple[Ops_, int] = field(default=None)
    health: int | Tuple[Ops_, int] = field(default=None)
    keywords: KeywordEnum | List[KeywordEnum] = field(default=None)

    def resolve(self, target, *args, **kwargs):
        return CreateCardEvent(
            target=target,
            location=self.location,
            owner=self.owner,
            quantity=self.quantity,
            is_fleeting=self.is_fleeting,
            is_ephemeral=self.is_ephemeral,
            index=self,
            with_my_stats_keywords_source=self.with_my_stats_keywords_source,
            with_my_stats_source=self.with_my_stats_source,
            attack=self.attack,
            cost=self.cost,
            health=self.health,
            keywords=self.keywords
        )



@define
class CreateExactCopyEffect(CreateCopyEffect):
    ...

