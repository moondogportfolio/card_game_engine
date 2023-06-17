from Sets.SET7.Units2new import AugmentedClockling, ElegantEdge
from actions.attribute.damage import DamageEffect
from actions.attribute.heal import HealEffect
from classes.game import Game
from enums.location import LocEnum


class TestAttribute:
    game = Game()
    gs = game.gamestate
    p1 = gs.entity_man.create_player(10, 10, 10, 10)
    p2 = gs.entity_man.create_player(10, 10, 10, 10)
    gs.entity_man.create_deck("", p1, gs, ElegantEdge)
    gs.entity_man.create_deck("", p2, gs, ElegantEdge)
    card = gs.entity_man.cards[0]

    def create_card(self, card):
        return self.gs.entity_man.create_card(
            card, LocEnum.BATTLEFIELD, self.p1, self.gs
        )[0]

    def test_a(self):
        unit = self.create_card(AugmentedClockling)
        assert unit.health == 10
