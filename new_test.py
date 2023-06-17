import asyncio

from attr import evolve
import Sets.SET1.Units as SET1Units
import Sets.SET1.Spells as SET1Spells
import Sets.SET2.Spells as SET2Spells
import Sets.SET3.Spells as SET3Spells
import Sets.SET1.Champions as SET1Champions
from actions.create.base_create import BaseCreateCardEffect
from actions.create.create_player import CreatePlayerAction
from actions.keywords.add_keyword import AddKeywordEffect
from actions.movement.capture import RecreateCaptureEffect
from actions.movement.draw import DrawEffect
from actions.reactions.triggered_action import TriggeredAction
from actions_player.play_card import PlayCardEffect
from card_classes.unit import Unit
from classes.game import Game
from conditions.base_condition import Condition
from entity_selectors.card_filter import (
    CardFilter,
    CardFilterSelector,
    DrawCardFilter,
)
from entity_selectors.input import Input
from enums.card_sorters import CardSorter
from enums.entity_events import EntityEvents
from enums.keywords import KeywordEnum
from enums.location import LocEnum
from enums.post_event_param import PostEventParam
from enums.subtypes import SubTypes_
from enums.types import Types_
from events.attribute.damage_event import DamageEvent
from events.movement.MovementEvent import MovementEvent
from resolvable_enums.card_conditions import CardFlags
from resolvable_enums.target_player import TargetPlayer


async def a():
    game = Game()
    gs = game.gamestate
    CC = SET1Units.Battlesmith
    p1 = gs.entity_man.create_player(10, 10, 10, 10)
    p2 = gs.entity_man.create_player(10, 10, 10, 10)
    card = gs.entity_man.create_card(CC, LocEnum.HOMEBASE, p1, gs)
    card2 = gs.entity_man.create_card(
        SET1Units.AcademyProdigy, LocEnum.HOMEBASE, p1, gs
    )[0]
    card3 = gs.entity_man.create_card(
        SET1Units.AcademyProdigy, LocEnum.HOMEBASE, p1, gs
    )
    gs.entity_man.create_card(SET1Units.AcademyProdigy, LocEnum.DECK, p1, gs, 4)
    oppo_board_card = gs.entity_man.create_card(
        SET1Units.AcademyProdigy, LocEnum.HOMEBASE, p2, gs
    )[0]
    deck_cards = gs.entity_man.create_card(CC, LocEnum.DECK, p2, gs, 10)
    card: Unit = card[0]
    hand_card = gs.entity_man.create_card(CC, LocEnum.HAND, p1, gs)[0]
    card4 = gs.entity_man.create_card(SET1Units.AcademyProdigy, LocEnum.HAND, p2, gs)


    sc = gs.entity_man.create_card(SET3Spells.ForTheFallen, LocEnum.DECK, p2, gs)[0]
    sc1 = gs.entity_man.create_card(SET1Spells.FinalSpark, LocEnum.HAND, p2, gs)[0]
    sc2 = gs.entity_man.create_card(SET2Spells.SuitUp, LocEnum.DECK, p2, gs)[0]
    champ_card = gs.entity_man.create_card(SET1Champions.Shen, LocEnum.HOMEBASE, p1, gs)

    # TEST SPELLSTACK
    # TODO
    await gs.spell_stack_man.add_to_q(sc, gs)
    gs.spell_stack_man.resolve_stack(gs)

    # TEST NEGATORS
    # spell_card = gs.entity_man.create_card(
    #     SET2Spells.UnyieldingSpirit, LocEnum.DECK, p2, gs
    # )[0]
    # event = DamageEvent(target=card, value=5)
    # gs.event_man.resolve_event(event=event, gamestate=gs, origin=card)

    # TEST COEVENT
    # spell_card = gs.entity_man.create_card(SET2Spells.TrailofEvidence, LocEnum.HAND, p2, gs)[0]

    # TEST POST EVENT
    # effect = TriggeredAction(
    #     event_filter=EntityEvents.MOVED_OUT_OF_PLAY, action=RecreateCaptureEffect()
    # )
    # gs.event_man.events[EntityEvents.MOVED_OUT_OF_PLAY] = [effect]
    # kill_event = MovementEvent(
    #     event=EntityEvents.KILL, target=oppo_board_card, destination=LocEnum.GRAVEYARD
    # )
    # gs.event_man.resolve_event(event=kill_event, gamestate=gs, origin=card)

    # TEST EVENT MAN
    # event = AddKeywordEffect(
    #     target=Input(choices=CardFilter(location=LocEnum.HOMEBASE)),
    #     keyword=KeywordEnum.BARRIER,
    # )
    # gs.event_man.resolve_action(event, gs, card, target=card)
    # TEST PLAY CARD
    # play_card_event = PlayCardEffect().resolve()
    # play_unit_event = play_card_event.resolve(gs, card, hand_card)
    # summon_event = play_unit_event.resolve(gs, card, play_unit_event.target)
    # effect = summon_event.resolve(gs, card, summon_event.target)

    # TEST COPY CARD
    # y = evolve(card)
    # # y.effects.event_filter = None
    # print(id(card.effects), id(y.effects))
    # print(y)

    # TEST EFFECTS
    # effect = AddKeywordEffect(target=card, keyword=KeywordEnum.ATTACH)
    # effect.resolve().resolve(gs, card, card)
    # TEST POSTEVENT/TRIGGERED ACTION

    # postevent = SummonEvent(target=card)
    # event = card.effects.resolve(gs, card, postevent)

    # TEST SELECTOR

    # cards = CardFilterSelector(
    #     type=None,
    #     owner=TargetPlayer.OPPONENT,
    #     location=LocEnum.HAND,
    # )
    # print(cards.resolve(gs, card))

    # cards = SimpleCardFilterSelector(
    #         location=LocEnum.HAND,
    #         sorter=CardSorter.CHEAPEST,
    #     ).resolve(gs, card)
    # print(cards)

    # TEST CONDITION
    # print(event)
    # condition=Condition(
    #         target=PostEventParam.TARGET,
    #         condition=CardFlags.IS_SUBTYPE_X,
    #         parameter=SubTypes_.ELITE,
    #     ).resolve(gs, card, postevent=postevent)


asyncio.run(a())
