
from Sets.SET7.Units2new import ElegantEdge
from actions.attribute.damage import DamageEffect
from actions.attribute.heal import HealEffect
from actions.base_action import BaseAction
from actions.movement.predict import PredictEffect
from classes.game import Game


class TestActionsMovement:
    game = Game()
    gs = game.gamestate
    p1 = gs.entity_man.create_player(10, 10, 10, 10)
    p2 = gs.entity_man.create_player(10, 10, 10, 10)
    gs.entity_man.create_deck("", p1, gs, ElegantEdge)
    gs.entity_man.create_deck("", p2, gs, ElegantEdge)
    card = gs.entity_man.cards[0]

    def _tester(self, effect: BaseAction):
        new_act = effect()
        new_act.resolve_params(self.gs, self.card)
        new_act.resolve(self.gs, self.card)

    def test_predict(self):
        self._tester(PredictEffect())

