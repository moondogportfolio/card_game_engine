from card_classes.cardarchetype import CardArchetype
from classes.gamestate import GameState
from enums.attribute import AttrEnum
from enums.entity_events import EntityEvents
from enums.keywords import KeywordEnum
from enums.operator import Ops_
from events.attribute.SetAttributeEvent import SetAttributeEvent


from attr import define, field


@define
class AddKeywordEvent(SetAttributeEvent):
    event: EntityEvents = field(init=False, default=EntityEvents.ADD_KEYWORD)
    attribute: AttrEnum = field(init=False, default=AttrEnum.KEYWORDS)
    value: KeywordEnum
    operator: Ops_ = field(init=False, default=Ops_.PUSH)

    def resolve(self, gamestate: GameState, origin: CardArchetype):
        gamestate.entity_man.set_attribute(
            target=self.target,
            attribute=self.attribute,
            value=self.value,
            operator=self.operator,
        )