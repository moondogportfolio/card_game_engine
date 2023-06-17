from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState


from attr import define, field

from events.attribute.damage_event import DamageEvent


@define
class SpellOverwhelmEvent(DamageEvent):

    def resolve(self, gamestate: GameState, origin: CardArchetype):
        print(self.target)
        if self.target == 'pass':
            self.target = origin.opponent
        gamestate.entity_man.set_attribute(
            target=self.target,
            attribute=self.attribute,
            value=self.value,
            operator=self.operator,
        )