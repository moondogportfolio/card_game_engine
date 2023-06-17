import asyncio
from actions.attribute.damage import DamageEffect
from actions.base_action import BaseAction
from actions.movement.predict import PredictEffect
from actions.reactions.triggered_action import TriggeredAction
from actions.traps.set_trap import PlantFlashBombTrap
from actions_player.play_card import PlayCardEffect, PlayEquip
from classes.game import Game
import Sets.SET7.Units as unitmod
import Sets.SET6.Units as SET6Units
import Sets.SET1.Spells as SET1Spells

import Sets.SET6.Equipments as SET6Equipments
from enums.counters import TrapEnums
from enums.entity_events import EntityEvents
from enums.location import LocEnum


class TestTrap:
    game = Game()
    gs = game.gamestate
    p1 = gs.entity_man.create_player(10, 10, 10, 10)
    p2 = gs.entity_man.create_player(10, 10, 10, 10)
    gs.entity_man.create_deck("", p1, gs, unitmod.AugmentedClockling)
    gs.entity_man.create_deck("", p2, gs, unitmod.ElegantEdge)
    gs.entity_man.create_card(SET6Units.WidowedHuntress, LocEnum.HAND, p1, gs)
    gs.entity_man.create_card(SET6Units.WidowedHuntress, LocEnum.HOMEBASE, p2, gs)
    gs.entity_man.create_card(SET6Equipments.DemacianSteel, LocEnum.HAND, p1, gs)
    gs.entity_man.create_card(unitmod.AugmentedClockling, LocEnum.HAND, p1, gs, 5)
    spell = gs.entity_man.create_card(SET1Spells.WitheringWail, LocEnum.HAND, p1, gs)[0]

    def damage_test(self):
        self.gs.spell_stack_man.add_to_queue(self.spell, self.gs)
        self.gs.stack_manager.resolve_stack(self.gs)
        print(self.gs.spell_stack_man.params)

    def _tester(self, effect: BaseAction, origin):
        new_act = effect()
        new_act.action_origin = origin
        new_act.resolve_params(self.gs)
        new_act.resolve(self.gs)

    def test(self):
        self._tester(PlantFlashBombTrap())
        opponent = self.gs.entity_man.get_opponent(self.card.owner)
        for index, card in enumerate(
            self.gs.loc_man.get_cards(LocEnum.DECK, opponent, 10)
        ):
            traps = self.gs.counter_man.get_traps(card, TrapEnums.FLASHBOMB_TRAP)
            print(traps)

    def test_validity(self, action):
        action.action_origin = self.p1
        print(action.target, action)
        # print(action.check_validity(self.gs))

    def test_play_unit(self):
        play_card = PlayCardEffect()
        self.test_looper(play_card)



    def test_looper(self, effect):
        self.gs.stack_manager.add_to_queue(effect, self.p1)

    def test_play(self):
        play_card = PlayCardEffect()
        self.test_looper(play_card)
        # self.test_validity(play_card)

    def test_triggered_action(self):
        ta = TriggeredAction(event_filter=EntityEvents.PLAY, action=...)

    def test_play_equip(self):
        pe = PlayEquip()
        self.test_validity(pe)



# async def main():
#     x = TestTrap()
#     x.test_play()
#     await x.game.game_looper_test()


# asyncio.run(main())

x = TestTrap()
x.damage_test()