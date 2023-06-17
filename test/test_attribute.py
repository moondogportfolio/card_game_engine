
from Sets.SET7.Units2new import ElegantEdge
from actions.attribute.damage import DamageEffect
from actions.attribute.heal import HealEffect
from classes.game import Game


class TestAttribute:
    game = Game()
    gs = game.gamestate
    p1 = gs.entity_man.create_player(10, 10, 10, 10)
    p2 = gs.entity_man.create_player(10, 10, 10, 10)
    gs.entity_man.create_deck("", p1, gs, ElegantEdge)
    gs.entity_man.create_deck("", p2, gs, ElegantEdge)
    card = gs.entity_man.cards[0]

    def test_damage(self):
        health = self.card.health
        effect = DamageEffect(target=self.card, value=2)
        effect.resolve(self.gs)
        assert self.card.health == health -2

    def test_heal(self):
        health = self.card.health
        effect = HealEffect(target=self.card, value=2)
        effect.resolve(self.gs)
        assert self.card.health == health + 2
