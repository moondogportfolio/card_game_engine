from actions.attribute.damage import DamageEffect
from actions.attribute.refill_mana import RefillSpellMana
from actions.keywords.stun_effect import StunEffect
from actions.movement.draw import DrawEffect
from actions.movement.obliterate import ObliterateEffect
from card_classes.skill import Skill
from entity_selectors.card_filter import CardFilter
from entity_selectors.target_game_card import TargetEntity
from enums.card_sorters import CardSorter
from enums.location import LocEnum
from resolvable_enums.active_cards_selector import TargetShorthand
from resolvable_enums.auto_card_selector import AutoEntitySelector
from resolvable_enums.target_player import TargetPlayer


# Deal 1 to an ally to deal 2 to the enemy Nexus.


def BlackPowderGrenade():
    effect = DamageEffect(value=1, target=TargetShorthand.ALLIED_BOARD_UNIT)
    effect1 = DamageEffect(value=2, target=TargetPlayer.OPPONENT, fizz_if_fail=effect)
    return Skill(activation_effect=[effect, effect1])


# Deal 1 to the enemy Nexus.
def Crackshot():
    effect = DamageEffect(value=1, target=TargetPlayer.OPPONENT)
    return Skill(activation_effect=effect)


# Obliterate an enemy with less Health than me.
def Devour():
    effect = ObliterateEffect(
        target=TargetEntity(
            choices=CardFilter(owner=TargetPlayer.OPPONENT, health=...)
        )
    )
    # TODO
    return Skill(activation_effect=effect)


def CannonBarrageEffect():
    ...

# Deal 2 to a unit.If it's dead or gone, deal 1 to the enemy Nexus instead.
def CannonBarrage():
    return Skill(activation_effect=CannonBarrageEffect)

# Deal 1 to all enemies and the enemy Nexus.
def PowderfulExplosion():
    effect = DamageEffect(
        value=1, target=AutoEntitySelector.OPPONENT_NEXUS_AND_BOARD_UNITS
    )
    return Skill(activation_effect=effect)


# Refill 1 spell mana.Draw 1.
def BlueCard():
    effect = RefillSpellMana(value=1)
    effect1 = DrawEffect()
    return Skill(activation_effect=[effect, effect1])


# Deal 1 to all enemies and the enemy Nexus.
def RedCard():
    # TODO include player
    effect = DamageEffect(
        value=1, target=AutoEntitySelector.OPPONENT_NEXUS_AND_BOARD_UNITS
    )
    return Skill(activation_effect=effect)


# Deal 2 and Stun the strongest enemy.
def GoldCard():
    target = CardFilter(owner=TargetPlayer.OPPONENT, sort_by=CardSorter.STRONGEST)
    effect = DamageEffect(value=2, target=target)
    effect1 = StunEffect(target=target)
    # TODO
    return Skill(activation_effect=[effect, effect1])


# Deal 1 to all battling enemies and the enemy Nexus.
def LoveTap():
    effect = DamageEffect(
        value=1,
        target=[
            CardFilter(owner=TargetPlayer.OPPONENT, location=LocEnum.BATTLEFIELD),
            TargetPlayer.OPPONENT,
        ],
    )
    return Skill(activation_effect=effect)


# Deal 1 three times to all battling enemies and the enemy Nexus.
def BulletTime():
    effect = DamageEffect(
        value=1,
        target=[
            CardFilter(owner=TargetPlayer.OPPONENT, location=LocEnum.BATTLEFIELD),
            TargetPlayer.OPPONENT,
        ],
    )
    return Skill(activation_effect=effect)
