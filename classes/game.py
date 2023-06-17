import time
from classes.gamestate import GameState
from classes.rules import Rules


from inspect import getmembers, isfunction

from rules_init import LORRules


class Game:
    def __init__(self, rules: Rules | None = None) -> None:
        self.gamestate = GameState()
        self.rules = rules or LORRules

    # def game_start(self):
    #     gs = self.gamestate
    #     player = gs.entity_man.players[0]
    #     cardclass = DragonMaster
    #     unit = gs.entity_man.create_card(cardclass, LocEnum.HOMEBASE, player, gs)[0]
    #     buff = BuffEffect(target=unit, origin=None)
    # frozen = jsonpickle.encode(gs)
    # print(frozen)
    # buff.resolve(gs)
    # target = CardFilter(maximum=3, minimum=3, owner=None)
    # recall = RecallAction(target=target, origin=None)
    # print(recall.validate_targets(self.states))

    # def test_environment(self):
    #     gs = self.gamestate
    #     p1 = gs.entity_man.create_player(10, 10, 10, 10)
    #     p2 = gs.entity_man.create_player(10, 10, 10, 10)
    #     gs.entity_man.create_deck("", p1, gs, unitmod.ElegantEdge)
    #     gs.entity_man.create_deck("", p2, gs, unitmod.ElegantEdge)
    #     card = gs.entity_man.cards[0]
    #     print(card.archetype.attack)
        # functions_list = getmembers(unitmod, isfunction)
        # for name, func in functions_list:
        #     print(func())
        

    # def test_environment2(self):
    #     gs = self.gamestate
    #     p1 = gs.entity_man.create_player(10, 10, 10, 10)
    #     p2 = gs.entity_man.create_player(10, 10, 10, 10)
    #     gs.entity_man.create_deck("", p1, gs, DragonMaster)
    #     gs.entity_man.create_deck("", p2, gs, DragonMaster)
    #     card = gs.entity_man.cards[0]
    #     quant = 10000000
    #     tic = time.perf_counter()
    #     card = gs.entity_man.create_card(
    #         card_class=DragonMaster,
    #         location=None,
    #         owner=p1,
    #         gamestate=gs,
    #         quantity=quant,
    #     )
    #     print(len(card))
    #     toc = time.perf_counter()
    #     print(toc-tic)
    #     print(card[0].archetype)
    #     print(p1.deckcode)
        # print(asizeof.asized(card))
        # damage = DamageEffect(target=card, value=2)
        # trigger = TriggeringEvent(event=EntityEvents.DAMAGE)
        # am = ActionModifier(
        #     trigger, parameter="value", operator=OpEnum.MULTIPLY, value=5
        # )
        # gs.listener_man.tampers[EntityEvents.DAMAGE].append(am)
        # gs.listener_man.modifier_check(damage)
        # damage(gs)

    async def game_looper_test(self):
        while True:
            await self.gamestate.input_manager.manual_input()
            await self.gamestate.step()

    async def game_looper(self):
        while True:
            await self.gamestate.input_manager.manual_input()
            if not await self.gamestate.step():
                next_ph_enum, next_ph_obj = self.rules.get_next_phase(
                    self.gamestate.game_phase
                )
                self.gamestate.set_phase(next_ph_enum, next_ph_obj.effects)
