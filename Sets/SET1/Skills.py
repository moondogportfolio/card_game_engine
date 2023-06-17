from actions.attribute.damage import DamageEffect
from actions.attribute.drain import DrainEffect
from actions.keywords.stun_effect import StunEffect
from actions.movement.discard import DiscardEffect
from actions.movement.draw import DrawEffect
from actions.movement.kill import KillAction
from actions.movement.obliterate import ObliterateEffect
from actions.movement.recall import RecallEffect
from actions.transform.transform import TransformEffect
from card_classes.spell import Spell
from entity_selectors.card_filter import CardFilter
from entity_selectors.target_game_card import TargetEntity
from enums.card_sorters import CardSorter
from enums.location import LocEnum
from resolvable_enums.active_cards_selector import TargetShorthand
from resolvable_enums.auto_card_selector import AutoEntitySelector
from resolvable_enums.target_player import TargetPlayer


def Sabotage():
    effect = DamageEffect(target=TargetPlayer.OPPONENT, value=1)
    return Spell(activation_effect=effect)


def Undermine():
    effect = DamageEffect(target=TargetPlayer.OPPONENT, value=2)
    return Spell(activation_effect=effect)


def ParalyzingBite():
    effect = StunEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT)
    return Spell(activation_effect=effect)


def Bullseye():
    effect = DamageEffect(value=1, target=TargetShorthand.OPPONENT_BOARD_UNIT)
    return Spell(activation_effect=effect)


def Impersonate(Skill):
    effect = TransformEffect(target=..., new_form=TargetShorthand.ANY_BOARD_UNIT)
    return Spell(activation_effect=effect)


def FaceMelter():
    effect = DamageEffect(value=1, target=CardFilter(owner=TargetPlayer.OPPONENT))
    return Spell(activation_effect=effect)


def Balesight():
    effect = ObliterateEffect(
        target=CardFilter(
            owner=None,
            attack=(0, 4),
            location=(LocEnum.HAND, LocEnum.BOARD),
        )
    )
    return Spell(activation_effect=effect)


def SkywardStrikes():
    effect = RecallEffect(
        target=TargetEntity(
            quantity=3,
            minimum=1,
            choices=CardFilter(owner=TargetPlayer.OPPONENT, quantity=None),
        )
    )
    return Spell(activation_effect=effect)


def MagnumOpus():
    effect = ObliterateEffect(
        target=CardFilter(location=LocEnum.DECK, type=None, top_x_cards=5),
    )
    # TODO
    value = ...
    effect1 = DamageEffect(
        target=AutoEntitySelector.OPPONENT_NEXUS_AND_BOARD_UNITS, value=value
    )
    return Spell(activation_effect=(effect, effect1))


def BladeofLedros():
    effect = DamageEffect(
        value=...,
        target=TargetPlayer.OPPONENT,
    )
    return Spell(activation_effect=effect)

    # def value_getter(self):
    #     return -(-self.opponent.health // 2)


def NightHarvest():
    # TODO
    effect = KillAction(
        target=CardFilter(
            owner=TargetPlayer.OPPONENT, quantity=2, sorter=CardSorter.WEAKEST
        )
    )
    return Spell(activation_effect=effect)


def StaggeringStrikes():
    effect = RecallEffect(
        target=TargetEntity(
            quantity=2,
            minimum=1,
            choices=CardFilter(owner=TargetPlayer.OPPONENT, quantity=None),
        )
    )
    return Spell(activation_effect=effect)


def RecklessResearch():
    #TODO discard
    effect = DiscardEffect(target=CardFilter(location=LocEnum.HAND, type=None))
    effect1 = DrawEffect(quantity=3)
    effect2 = DamageEffect(value=3, target=TargetShorthand.OPPONENT_BOARD_UNIT)
    return Spell(activation_effect=(effect, effect1, effect2))


def TarkazsFury(Skill):
    effect = DamageEffect(
        value=1, target=CardFilter(location=LocEnum.BATTLEFIELD, owner=None)
    )
    return Spell(activation_effect=effect)


def GlacialStorm2():
    _cardcode = "01FR024T5"

    effect = DamageEffect(
        value=2,
        target=AutoEntitySelector.OPPONENT_NEXUS_AND_BOARD_UNITS,
    )
    return Spell(activation_effect=effect)


def GlacialStorm():
    _cardcode = "01FR024T2"

    effect = DamageEffect(
        value=1,
        target=AutoEntitySelector.OPPONENT_NEXUS_AND_BOARD_UNITS,
    )
    return Spell(activation_effect=effect)


def CrimsonPact():
    effect = DamageEffect()
    # TODO for each
    effect = DamageEffect(value=1, target=TargetPlayer.OPPONENT)
    effect1 = DamageEffect(value=1)
    return Spell(activation_effect=effect)


def CrimsonPact2():
    _cardcode = "01NX006T4"

    effect = DrainEffect(value=1, target=TargetPlayer.OPPONENT)
    effect1 = DamageEffect(target=..., value=1)
    return Spell(activation_effect=(effect, effect1))