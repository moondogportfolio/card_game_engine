import Sets.SET6.Champions as Set6Champions
from actions.attachments.play_as_unit import PlayEquipAsUnit
from actions.attribute.buff import BuffEffect, BuffSupportEffect
from actions.create.create_card import CreateCardEffect
from actions.movement.discard import DiscardEffect
from actions.movement.draw import DrawEffect
from actions.movement.kill import KillAction
from actions.reactions.dynamic_attr_modifier import (
    DynamicAttackModifier,
    DynamicAttributeModifier,
    DynamicCostModifier,
    DynamicKeywordModifier,
)
from actions.reactions.triggered_action import (
    AllyOrigin_TA,
)
from actions.requisite.action_requisite import ActionRequisite
from card_classes.equipment import Equipment
from conditions.base_condition import Condition
from entity_selectors.base_card_filter import BaseCardFilter
from entity_selectors.card_filter import CardFilter
from enums.attribute import AttrEnum
from enums.entity_events import EntityEvents
from enums.keywords import KeywordEnum
from enums.location import LocEnum
from enums.operator import Ops_
from enums.subtypes import SubTypes_
from enums.types import Types_
from resolvable_enums.active_cards_selector import TargetShorthand
from resolvable_enums.auto_card_selector import AutoEntitySelector
from resolvable_enums.card_conditions import CardFlags
from resolvable_enums.player_conditions import PlayerFlags


def CorruptedForm():
    ...


def OrigamiSlicer():
    value = ...
    # value = PlayerStatistic(
    #     statistic=PlayerStatisticEnum.BOON_OR_TRAP_ACTIVATED_THIS_ROUND
    # )
    effect = DynamicAttackModifier(target=TargetShorthand.SELF, attack=value)


def DemacianSteel():
    return Equipment(cardcode = '06DE032')


def TheDarkinBallista():
    effect3 = PlayEquipAsUnit(unit=Set6Units.NaganekaofZuretta)


def TheLightofIcathia():
    effect = DynamicKeywordModifier(
        value=KeywordEnum.OVERWHELM,
        condition=Condition(
            condition=PlayerFlags.HAS_LEVELED_CHAMP_X_THIS_GAME,
            parameter=Set6Champions.Jax,
        ),
    )


def TheDarkinBloodletters():
    effect = CreateCardEffect(
        target=Set6Units.DarkinThrall,
        condition=Condition(
            target=TargetShorthand.THIS_EQUIPMENT_BEARER,
            condition=CardFlags.IS_CARD_def,
            parameter=Set6Units.DarkinThrall,
        ),
        triggering_effect=EntityEvents.LASTBREATH,
    )
    effect3 = PlayEquipAsUnit(cost=8, card=Set6Units.Xolaani)


def TheDarkinHalberd():
    effect3 = PlayEquipAsUnit(cost=8, card=Set6Units.Taarosh)
    effect1 = KillAction(target=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = ActionRequisite(requisite=effect1)
    return Equipment(cardcode = '06SI007T4')


def TheDarkinHarpoon():
    effect = DrawEffect(is_fleeting=True, triggering_effect=EntityEvents.ATTACK_COMMIT)
    effect1 = PlayEquipAsUnit(cost=9, card=Set6Units.Ibaaros)
    return Equipment(cardcode = '06BW014T3')


def TheDarkinAegis():
    effect1 = PlayEquipAsUnit(cost=5, card=Set6Units.Joraal)


def TheDarkinLodestone():
    effect = BuffSupportEffect(
        attack=1,
        health=1,
    )
    effect3 = PlayEquipAsUnit(cost=8, card=Set6Units.Horazi)


def GreatHammers():
    return Equipment(cardcode = '06NX026')


def TheDarkinHarp():
    effect1 = PlayEquipAsUnit(card=Set6Units.Styraatu)


def InspiredPlans():
    effect = CreateCardEffect(
        target=BaseCardFilter(type=Types_.SPELL, cost=2, flags=CardFlags.IS_NEW_CARD),
        is_fleeting=True,
    )
    return Equipment(bearer_attack_commit_effect=effect, cardcode = '06PZ030')


def TheDarkinScythe():
    effect1 = BuffEffect(target=AutoEntitySelector.SELF, attack=1, health=0)
    return Equipment(bearer_attack_commit_effect=effect1, cardcode = '06RU005T3')


def ShadowScythe():
    effect1 = BuffEffect(target=AutoEntitySelector.SELF, attack=2, health=0)
    return Equipment(bearer_attack_commit_effect=effect1, cardcode = '06RU005T10')


def CorruptedScythe():
    effect1 = BuffEffect(target=AutoEntitySelector.SELF, attack=1, health=1)
    return Equipment(bearer_attack_commit_effect=effect1, cardcode = '06RU005T11')


def TheDarkinBow():
    effect = BuffEffect(target=AutoEntitySelector.SELF, attack=1)
    ta1 = AllyOrigin_TA(event_filter=EntityEvents.PLAY_SPELL, action=effect)
    ta2 = AllyOrigin_TA(event_filter=EntityEvents.PLAY_SPELL, action=effect)
    # TODO max


def TheFixEm5000():
    return Equipment(cardcode = '06RU010')


def PotOPain():
    return Equipment(cardcode = '06RU012')


def SandwornAmulet():
    return Equipment(cardcode = '06RU028')


def Fishawhack():
    return Equipment(cardcode = '06RU029')


def UpcycledRake():
    return Equipment(cardcode = '06RU030')


def ShepherdsAuthority():
    return Equipment(cardcode = '06RU031')


def CombatReel():
    return Equipment(cardcode = '06RU033')


def PanOPain():
    return Equipment(cardcode = '06RU034')


def Mechapulverizer():
    effect1 = DiscardEffect(
        target=CardFilter(location=LocEnum.HAND, type=None), exclude_origin=True
    )
    effect = ActionRequisite(requisite=effect1)


def JaggedCutlass():
    effect = DynamicCostModifier(value=2, condition=PlayerFlags.PLUNDER)


def Gatalystv10():
    effect = DynamicAttributeModifier(
        attribute=AttrEnum.SPELL_DAMAGE, value=1, operator=Ops_.INCREMENT, target=...
    )


def TreasureoftheSands():
    return Equipment(cardcode = '06SH031')


def SwingingGlaive():
    effect = CreateCardEffect(
        target=BaseCardFilter(type=Types_.SPELL, cost=2), is_fleeting=True
    )


def MaleficSpear():
    effect = DynamicCostModifier(value=2, condition=PlayerFlags.ALLY_DIED_THIS_ROUND)


def SoulSword():
    effect = DynamicCostModifier(
        value=2,
        condition=PlayerFlags.FLOW,
    )
    return Equipment(cardcode = '06IO031')


def DraconicBands():
    return Equipment(subtype_modifier=SubTypes_.DRAGON, cardcode = '06MT033')


def BoneClub():
    return Equipment(cardcode = '06FR024')
