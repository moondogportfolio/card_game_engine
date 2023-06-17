from typing import Any, Tuple
from attr import define
import Sets.SET4.Units as Set4Units
import Sets.SET6.Champions as Set6Champions
from actions.base_action import BaseAction, BaseTargetAction
from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from entity_selectors.base_card_filter import BaseCardFilter
from enums.attribute import AttrEnum
from enums.location import LocEnum
from enums.operator import Ops_
from events.attachments.transfer_attachments import TransferAttachmentsEvent
from events.attribute.buff_event import BuffEvent
from events.attribute.buff_everywhere_Event import BuffEverywhereEvent
from events.attribute.damage_event import DamageEvent
from events.attribute.frostbite import FrostbiteEvent
from events.base_event import BaseEvent
from events.create.CreateCardEvent import CreateCardEvent
from value.player_statistic import PlayerStatistic


@define
class SneezyBiggledustEffect(BaseAction):
    def resolve(
        self, gamestate: GameState, origin: Any, *args, **kwargs
    ) -> BaseEvent | Tuple[BaseEvent]:
        cards = gamestate.loc_man.get_board_units(origin.owner)
        events = []
        for card in cards:
            if card.created:
                events.append(BuffEvent(target=card, attack=2, health=2))
            else:
                events.append(BuffEvent(target=card, attack=1, health=1))
        return events


# Frostbite an enemy.
# Summon a Rimefang Pack.
# Grant it +1|+1 for each time you've Frostbitten enemies this game.
@define
class FrozeninFearEffect(BaseTargetAction):
    def resolve(
        self, target, gamestate: GameState, origin: Any, *args, **kwargs
    ) -> BaseEvent | Tuple[BaseEvent]:
        event1 = FrostbiteEvent(target=target)
        val = PlayerStatistic.FROSTBITTEN_ENEMIES
        event2 = CreateCardEvent(
            target=Set4Units.RimefangPack,
            location=LocEnum.HOMEBASE,
            owner=origin.owner,
            attack=val,
            health=val,
        )
        return (event1, event2)


@define
class SecondSkinEffect(BaseTargetAction):
    def resolve(
        self, target: CardArchetype, *args, **kwargs
    ) -> BaseEvent | Tuple[BaseEvent]:
        buff = BuffEvent(keywords=target.positive_keywords)
        event = BuffEverywhereEvent(
            card_filter=BaseCardFilter(card_class=Set6Champions.KaiSa), buff_obj=buff
        )
        return event


# Deal 1 to a unit. If one of your traps or boons activated this round, deal 3 to it instead.
@define
class ProximityPuffcapEffect(BaseTargetAction):
    def resolve(
        self, target: CardArchetype, *args, **kwargs
    ) -> BaseEvent | Tuple[BaseEvent]:
        if ...:
            # TODO
            val = 3
        else:
            val = 1
        return DamageEvent(value=val, target=target)


# Give an ally with an attachment the stats and keywords of its attachment this round
# and move the attachment to another ally.
@define
class Sharesies(BaseTargetAction):
    equipment_destination: Any

    def get_target_objects(self) -> Tuple:
        return (self.target, self.equipment_destination)

    def resolve(
        self,
        target: CardArchetype,
        equipment_destination: CardArchetype,
        gamestate: GameState,
        *args,
        **kwargs
    ) -> BaseEvent | Tuple[BaseEvent]:
        entity = gamestate.attach_man.get_entity_attachment(target, AttrEnum.ATTACHMENT)
        event1 = BuffEvent(
            attack=entity.attack,
            health=entity.health,
            keywords=entity.keywords,
            round_only=True,
        )
        event2 = TransferAttachmentsEvent(
            target=target, destination=equipment_destination
        )
        return (event1, event2)
