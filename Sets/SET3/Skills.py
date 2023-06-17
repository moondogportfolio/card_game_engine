from actions.activations.multiple_activations import MultipleActivationsEffect
from actions.attribute.buff import BuffEffect
from actions.attribute.damage import DamageEffect
from actions.attribute.drain import DrainEffect
from actions.common.strike import StrikeEffect
from actions.keywords.add_keyword import AddKeywordEffect, AddRandomKeywordEffect
from actions.keywords.stun_effect import StunEffect
from actions.meta.create_ta import CreateTriggeredAction
from actions.movement.capture import CaptureEffect
from actions.movement.kill import DestroyLandmarkEffect
from actions.reactions.triggered_action import TriggeredAction
from card_classes.spell import Spell
from entity_selectors.card_filter import CardFilter
from entity_selectors.input import ChoiceAction
from entity_selectors.target_game_card import TargetEntity
from enums.gamestate import GameStateEnums
from enums.keywords import KeywordEnum
from enums.types import Types_
from resolvable_enums.active_cards_selector import TargetShorthand
from resolvable_enums.auto_card_selector import AutoEntitySelector
from resolvable_enums.target_player import TargetPlayer
import Sets.SET3.Champions as Set3Champions


# Stun enemies with 2 or less Power.
def Mischief():
    effect = StunEffect(target=CardFilter(owner=TargetPlayer.OPPONENT, attack=(0, 2)))
    return Spell(activation_effect=effect)



# Drain 2 from the enemy Nexus.
def Torment():
    effect = DrainEffect(value=2, target=TargetPlayer.OPPONENT)
    return Spell(activation_effect=effect)


# Capture a unit or landmark.
def Claim():
    effect = CaptureEffect(
        target=TargetShorthand.ANY_BOARD_UNIT_OR_LANDMARK, storage=...
    )
    return Spell(activation_effect=effect)


# Deal 1 to an ally and an enemy 4 times.
def Gouge():
    effect1 = DamageEffect(target=TargetShorthand.ALLIED_BOARD_UNIT, value=1)
    effect2 = DamageEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT, value=1)
    effect4 = MultipleActivationsEffect(target=(effect1, effect2), multiplier=4)
    # TODO
    return Spell(activation_effect=effect4)


# Grant Viktor a random keyword.
def HexCoreUpgrade():
    effect = AddRandomKeywordEffect(
        target=CardFilter(card_class=Set3Champions.Viktor)
    )
    return Spell(activation_effect=effect)



# Stun the strongest enemy.
def SolarFlare():
    effect = StunEffect(target=AutoEntitySelector.STRONGEST_OPPONENT_BOARD_UNIT)
    return Spell(activation_effect=effect)


# Grant an ally +2|+0, Overwhelm, and Quick Attack.
def BladeoftheExile():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=2,
        keyword=[KeywordEnum.OVERWHELM, KeywordEnum.QUICKSTRIKE],
    )
    return Spell(activation_effect=effect)


# Tahm Kench swallows an enemy unit. It strikes him, then he Captures it.
def AnAcquiredTaste():
    target = TargetEntity(choices=TargetShorthand.OPPONENT_BOARD_UNIT)
    tahm = CardFilter(card_class=Set3Champions.TahmKench, quantity=1)
    effect = StrikeEffect(striker=target, target=tahm)
    effect1 = CaptureEffect(storage=tahm, target=target)
    return Spell(activation_effect=(effect, effect1))


# Give an ally Barrier or an enemy Vulnerable this round.
def HelpPix():
    effect = AddKeywordEffect(
        keyword=KeywordEnum.VULNERABLE, target=TargetShorthand.OPPONENT_BOARD_UNIT
    )
    effect1 = AddKeywordEffect(
        keyword=KeywordEnum.BARRIER, target=TargetShorthand.ALLIED_BOARD_UNIT
    )
    effect2 = ChoiceAction(choices=[effect, effect1])
    return Spell(activation_effect=effect2)


# Stun an enemy. If it's a follower, Stun it again at the next Round Start.
def SkyCharge():
    target_obj = TargetEntity(choices=TargetShorthand.OPPONENT_BOARD_UNIT)
    effect = StunEffect(target=target_obj)
    effect1 = StunEffect(
        target=target_obj,
    )
    # TODO
    ta = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START, action=effect1, condition=...
    )
    effect2 = CreateTriggeredAction(triggered_action=ta)

    return Spell(activation_effect=(effect, effect2))


# Deal 3 to ALL other units.
def ExtinguishingRay():
    # TODO
    effect = DamageEffect(target=CardFilter(owner=None), value=3)
    return Spell(activation_effect=effect)


# Obliterate ALL landmarks.
def DestructiveRay():
    effect = DestroyLandmarkEffect(target=CardFilter(type=Types_.LANDMARK, owner=None))
    return Spell(activation_effect=effect)
