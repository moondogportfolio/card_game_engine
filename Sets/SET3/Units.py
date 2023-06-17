from Sets.SET3.CustomEffects import MechanizedMimicEffect, MountainSojournersEffect
import Sets.SET3.Skills as Set3Skills
import Sets.SET3.Spells as Set3Spells
from actions.activations.play_skill import PlaySkill
from actions.attachments.destroy import DestroyAttachmentsEffect, DestroyEquipEffect
from actions.attachments.equip import EquipEffect
from actions.attachments.forge import ForgeEffect
from actions.attachments.improvise import ImproviseEffect
from actions.attachments.transfer_equip import TransferEquipmentEffect
from actions.attack.challenge import ChallengeEffect
from actions.attack.free_attack import FreeAttackEffect
from actions.attack.overwhelm_effect import OverwhelmEffect
from actions.attribute.buff import BuffCostEffect, BuffEffect
from actions.attribute.buff_everywhere import BuffEverywhereEffect
from actions.attribute.damage import DamageEffect
from actions.attribute.gain_mana_gem import GainManaGemEffect
from actions.attribute.heal import HealEffect
from actions.attribute.rally import RallyEffect
from actions.attribute.refill_mana import RefillManaEffect, RefillSpellMana
from actions.attribute.set_attribute import SetAttribute
from actions.attribute.support import SupportEffect
from actions.common.strike import StrikeEffect

from actions.create.create_card import CreateCardEffect
from actions.create.create_hand_cards import ReforgeEffect
from actions.create.invoke import InvokeEffect
from actions.keywords.add_keyword import AddKeywordEffect
from actions.keywords.stun_effect import StunEffect
from actions.movement.discard import DiscardEffect
from actions.movement.draw import (
    DrawEffect,
)
from actions.movement.move import MoveEffect
from actions.reactions.action_replacement import ActionReplacement
from actions.reactions.dynamic_attr_modifier import (
    DynamicAttributeModifier,
    DynamicCostModifier,
)
from actions.reactions.triggered_action import TriggeredAction
from card_classes.unit import Unit
from conditions.base_condition import Condition
from entity_selectors.base_card_filter import (
    BaseCardFilter,
    BaseCardRandomSelector,
    InvokeBaseCardFilter,
)
from entity_selectors.card_filter import (
    BeholdingFilter,
    CardFilter,
    EntityFilter,
)
from entity_selectors.input import ChoiceAction
from entity_selectors.target_game_card import TargetEntity
from enums.attribute import AttrEnum
from enums.entity_events import EntityEvents
from enums.keywords import KeywordEnum
from enums.gamestate import GameStateEnums
from enums.location import LocEnum
from enums.operator import Ops_
from enums.origin_enum import OriginEnum
from enums.post_event_param import PostEventParam
from enums.subtypes import SubTypes_
from enums.types import Types_
from resolvable_enums.active_cards_selector import TargetShorthand
from resolvable_enums.auto_card_selector import AutoEntitySelector
from resolvable_enums.card_conditions import CardFlags
from resolvable_enums.player_conditions import PlayerFlags
from resolvable_enums.target_player import TargetPlayer
from value.entity_attribute import EntityAttribute
from value.player_statistic import PlayerStatistic


# Last Breath: Reforge.
def BladeSquire():
    effect = ReforgeEffect()
    return Unit(last_breath_effect=effect)


#
def Squirrel():
    return Unit()


# Play: Deal 2 to me.
def CrustyCodger():
    effect = DamageEffect(target=AutoEntitySelector.SELF, value=2)
    return Unit(play_effect=effect)


# When I'm supported, grant me +2|+0.
def FlowerChild():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=2,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUPPORT,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
    )
    return Unit(effects=ta)


# When I'm summoned, create a Gem in hand.
def GiftGiver():
    effect = CreateCardEffect(
        Set3Spells.Gem,
    )
    return Unit(summon_effect=effect)


# When I'm summoned, create a Duskpetal Dust in hand.
def LunariDuskbringer():
    effect = CreateCardEffect(
        Set3Spells.DuskpetalDust,
    )
    return Unit(summon_effect=effect)


# Support: Give my supported ally +2|+1 this round.
def Pix():
    effect = SupportEffect(
        attack=2,
        health=1,
        round_only=True,
    )
    return Unit(support_effect=effect)


#
def Porofly():
    return Unit()


# Daybreak: Give me +1|+1 this round.
def SolariSoldier():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=1,
        health=1,
        round_only=True,
    )
    return Unit(play_daybreak=effect)


# Nightfall: Give me +2|+0 and Fearsome this round.
def StygianOnlooker():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=2,
        keyword=KeywordEnum.FEARSOME,
        round_only=True,
    )
    return Unit(play_nightfall=effect)


#
def TheCharger():
    return Unit()


# Round Start: Create an Ignition in hand.
def BallisticBot():
    effect = CreateCardEffect(
        Set3Spells.Ignition,
    )
    return Unit(round_start_effects=effect)


# Play: Deal 3 to me.
def Boxtopus():
    effect = DamageEffect(target=AutoEntitySelector.SELF, value=3)
    return Unit(play_effect=effect)


# When I'm summoned, if you Behold a Dragon, grant me Challenger.
def DragonguardLieutenant():
    effect = AddKeywordEffect(
        target=AutoEntitySelector.SELF,
        keyword=KeywordEnum.CHALLENGER,
    )
    effect1 = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
        condition=Condition(
            target=TargetPlayer.ORIGIN_OWNER,
            condition=PlayerFlags.IS_BEHOLDING_X_CARD,
            parameter=BeholdingFilter(subtype=SubTypes_.DRAGON),
        ),
    )
    return Unit(effects=effect1)


# When I'm summoned, create a random Dragon in hand.
def EggheadResearcher():
    effect1 = CreateCardEffect(
        target=BaseCardRandomSelector(subtype=SubTypes_.DRAGON),
    )
    return Unit(summon_effect=effect1)


# Round Start: If you Behold an 8+ cost card, get an extra mana gem this round.
def FacesoftheOldOnes():
    effect = GainManaGemEffect(
        gain_mana=True,
        round_only=True,
    )
    effect1 = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START,
        action=effect,
        condition=PlayerFlags.IS_BEHOLDING_8_COST_CARD,
    )
    return Unit(round_start_effects=effect1)


# Play: Deal 1 to me and an ally to draw 1.
def FortuneCroaker():
    effect = DamageEffect(target=AutoEntitySelector.SELF, value=2)
    effect1 = DamageEffect(target=TargetShorthand.ALLIED_BOARD_UNIT, value=2)
    effect2 = DrawEffect(fizz_if_fail=(effect, effect1))
    return Unit(play_effect=(effect, effect1, effect2))


# Daybreak: Give me +0|+4 this round.
def SolariShieldbearer():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        health=4,
        round_only=True,
    )
    return Unit(play_daybreak=effect)


# Nightfall: Grant me Elusive.
def LunariShadestalker():
    effect = AddKeywordEffect(
        target=AutoEntitySelector.SELF,
        keyword=KeywordEnum.ELUSIVE,
    )
    return Unit(play_nightfall=effect)


# When I'm summoned, Reforge.
def Runeweaver():
    effect = ReforgeEffect()
    return Unit(summon_effect=effect)


# I cost 2 less if you Behold a Celestial.
def StarryScamp():
    effect1 = DynamicCostModifier(
        value=2,
        condition=PlayerFlags.IS_BEHOLDING_CELESTIAL,
    )
    return Unit(effects=effect1)


#
def StartledStomper():
    return Unit()


# Nightfall: Create a copy of me in hand.
def EvershadeStalker():
    effect1 = CreateCardEffect(
        target=EvershadeStalker,
    )
    return Unit(play_nightfall=effect1)


# Support: Grant my supported ally +2|+2.Last Breath: Create 3 Gems in hand.
def MentoroftheStones():
    effect = SupportEffect(
        attack=2,
        health=2,
        round_only=True,
    )
    effect2 = CreateCardEffect(Set3Spells.Gem, quantity=3)
    return Unit(last_breath_effect=effect2, support_effect=effect)


#
def Mumblesprite():
    return Unit()


# Support: Create an attacking Mumblesprite with my supported ally's stats.
def TrevorSnoozebottom():
    effect = CreateCardEffect(
        Mumblesprite,
        LocEnum.BATTLEFIELD,
        with_my_stats_source=PostEventParam.TARGET
    )
    effect1 = TriggeredAction(
        event_filter=EntityEvents.SUPPORT,
        ally_enum=OriginEnum.SUPPORTER_SELF,
        action=effect
    )
    return Unit(effects=effect1)


# Round Start: Heal your Nexus 3. Deal damage to me equal to the amount healed.
def BroadbackedProtector():
    effect = HealEffect(target=TargetPlayer.ORIGIN_OWNER, value=3)
    effect1 = DamageEffect(
        target=AutoEntitySelector.SELF,
        value=PostEffectParamGetter(
            effect=effect, parameter=EventParameter.HEALED_AMOUNT
        ),
    )
    return Unit(round_start_effects=(effect, effect1))


# Play: Invoke a Celestial card that costs 3 or less.
def TheFangs():
    effect = InvokeEffect(
        target=InvokeBaseCardFilter(cost=(0, 3)),
    )
    return Unit(play_effect=effect)


# Round Start: Create a Sleep with the Fishes in hand.
def JacktheWinner():
    effect = CreateCardEffect(
        Set3Spells.SleepwiththeFishes,
    )
    return Unit(round_start_effects=effect)


# Attack: Grant me all keywords on allies.
def MechanizedMimic():
    # TODO custom effect
    return Unit(attack_commit_effect=MechanizedMimicEffect())


# Support: Grant my supported ally +2|+2.
# If it has Support, grant its supported ally +2|+2 and
# continue for each supported ally in succession.
def MountainSojourners():
    return Unit(effects=MountainSojournersEffect)


# Round End: If you cast a spell on me this round, I strike the weakest enemy.
def ArreltheTracker():
    effect = StrikeEffect(
        target=AutoEntitySelector.WEAKEST_OPPONENT_UNIT,
        striker=AutoEntitySelector.SELF,
    )
    effect1 = TriggeredAction(
        event_filter=GameStateEnums.ROUND_END, action=effect, condition=...
    )
    # TODO value triggered?
    return Unit(effects=effect1)


# Nightfall: Give me and an ally Elusive this round.
def CygnustheMoonstalker():
    effect = AddKeywordEffect(
        target=AutoEntitySelector.SELF,
        keyword=KeywordEnum.ELUSIVE,
        round_only=True,
    )
    effect1 = AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        keyword=KeywordEnum.ELUSIVE,
        round_only=True,
    )
    return Unit(play_nightfall=(effect, effect1))


# When an ally with Fury kills an enemy for the first time each round,
# create a random Dragon follower in hand.
def InviolusVox():
    effect = CreateCardEffect(
        target=BaseCardFilter(
            subtype=SubTypes_.DRAGON,
            quantity=1,
            flags=CardFlags.IS_FOLLOWER,
        )
    )
    effect1 = TriggeredAction(
        event_filter=EntityEvents.KILL,
        ally_enum=OriginEnum.T_OPPO_O_ALLY,
        condition=...,
        action=effect,
        activations_per_round=1,
    )
    return Unit(summon_effect=effect1)


# Daybreak: Give me +4|+4 this round.
def SunGuardian():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=4,
        health=4,
        round_only=True,
    )
    return Unit(play_daybreak=effect)


# When I'm summoned, grant other Dragon allies everywhere +2|+2.
def KadregrintheInfernal():
    effect = BuffEverywhereEffect(
        filter_obj=BaseCardFilter(subtype=SubTypes_.DRAGON),
        attack=2,
        health=2,
    )
    return Unit(summon_effect=effect)


# Reduce my cost by 1 for each spell you've cast this game.
# When I'm summoned, create in hand a random 1 cost spell from your regions.
def WigglyBurblefish():
    effect = CreateCardEffect(
        target=BaseCardFilter(
            quantity=1, type=Types_.SPELL, cost=1, owner_same_regions=True
        ),
    )
    effect1 = DynamicCostModifier(value=PlayerStatistic.SPELL_CAST_THIS_GAME)
    return Unit(summon_effect=effect, effects=effect1)


# Reduce my cost by 1 for each time you've targeted or supported allies this game.
def ArbiterofthePeak():
    effect1 = DynamicCostModifier(value=PlayerStatistic)
    # TODO reduce cost for every target, supported
    return Unit(effects=effect1)


# Play: Pick 2 enemies.
# Round Start: Stun them.
def TheInfiniteMindsplitter():
    # TODO target
    effect = StunEffect(target=PostEventParam.TARGET)
    effect1 = TriggeredAction(event_filter=GameStateEnums.ROUND_START, action=effect)
    return Unit(effects=effect1)




# Play: Deal 1 to an ally and an enemy 4 times.
def BasiliskBloodseeker():
    effect = PlaySkill(target=Set3Skills.Gouge)
    return Unit(play_effect=effect)


# Play: Obliterate ALL landmarks or deal 3 to ALL other units.
def ItThatStares():
    effect1 = PlaySkill(target=Set3Skills.ExtinguishingRay)
    effect2 = PlaySkill(target=Set3Skills.DestructiveRay)
    effect = ChoiceAction(choices=[effect1, effect2])
    return Unit(play_effect=effect)


#
def UzgartheAncient():
    return Unit()


# Play: Grant 2 allies +0|+4.
def GrandfatherRumul():
    effect = BuffEffect(
        target=TargetEntity(quantity=2, filter=CardFilter()),
        health=4,
    )
    return Unit(effects=effect)


# Play: Capture a unit or landmark.
def CaptainArrika():
    effect = PlaySkill(target=Set3Skills.Claim)
    return Unit(play_effect=effect)


# Daybreak: The next Dragon or Celestial unit you play costs 2 less.
# Nightfall: Create a random Dragon and Celestial follower in hand.
def EclipseDragon():
    effect = CreateCardEffect(
        target=BaseCardFilter(type=None, subtype=SubTypes_.DRAGON)
    )
    effect1 = CreateCardEffect(
        target=BaseCardFilter(type=None, subtype=SubTypes_.CELESTIAL)
    )
    effect3 = DynamicCostModifier(
        target=CardFilter(subtype=(SubTypes_.CELESTIAL, SubTypes_.DRAGON)),
        value=2,
    )
    # TODO dynamic modifier -> filter + action
    return Unit(play_nightfall=(effect, effect1), play_daybreak=effect3)


# Play: Deal 1 to all other allies and grant me +1|+0 for each of them.
def WiseFry():
    # TODO exclude self, len
    effect = DamageEffect(target=CardFilter(), value=1)
    effect1 = BuffEffect(target=AutoEntitySelector.SELF, attack=...)
    return Unit(play_effect=(effect, effect1))


# When I'm summoned, if you Behold a Dragon, Rally.
def DragonguardLookout():
    effect = RallyEffect()
    effect1 = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
        condition=PlayerFlags.IS_BEHOLDING_DRAGON,
    )
    return Unit(effect=effect1)


# Play: If you Behold an 8+ cost card, grant an ally Overwhelm and Regeneration.
def AuguroftheOldOnes():
    effect = AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        keyword=(KeywordEnum.OVERWHELM, KeywordEnum.REGENERATION),
    )
    effect1 = TriggeredAction(
        event_filter=EntityEvents.PLAY,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
        condition=PlayerFlags.IS_BEHOLDING_8_COST_CARD,
    )
    return Unit(effect=effect1)


# Nightfall: Stun an enemy. If it's a follower, Stun it again at the next Round Start.
def TheClovenWay():
    effect = PlaySkill(target=Set3Skills.SkyCharge)
    return Unit(play_nightfall=effect)


# Daybreak: Create a random Daybreak card in hand.It's always Day for us.
def RahvunDaylightsSpear():
    effect = CreateCardEffect(
        BaseCardFilter(quantity=1, flags=CardFlags.HAS_DAYBREAK),
        LocEnum.HOMEBASE,
    )
    effect1 = ...
    # TODO always day for us
    return Unit(effects=..., play_daybreak=effect)


# Nightfall: Grant me +1|+0 for each time we've activated Nightfall this game.
def Duskrider():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=PlayerStatistic.ACTIVATED_NIGHTFALL,
    )
    return Unit(play_nightfall=effect)


# Strike: Double my Power.
def SwoleSquirrel():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=2,
        operator=Ops_.MULTIPLY,
    )
    return Unit(strike_effect=effect)


# Your Celestial cards cost 1 less.Allegiance: Invoke.
def MountainScryer():
    effect = InvokeEffect()
    effect1 = DynamicCostModifier(
        value=1,
        target=CardFilter(subtype=SubTypes_.CELESTIAL, location=None, type=None),
    )
    # TODO CardFilterSelector
    return Unit(effect1=effect, summon_allegiance_effect=effect)


# When you heal a damaged ally, give it Elusive this round.
def Stargazer():
    effect = AddKeywordEffect(
        target=PostEventParam.TARGET,
        keyword=KeywordEnum.ELUSIVE,
    )
    effect1 = TriggeredAction(
        event_filter=EntityEvents.HEAL,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        action=effect,
    )
    return Unit(effects=effect1)


# Play: Grant an ally Elusive.
def FaeGuide():
    effect = AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        keyword=KeywordEnum.ELUSIVE,
    )
    return Unit(play_effect=effect)


# When I'm summoned, give me Quick Attack this round.
def BrutalHunter():
    effect = AddKeywordEffect(
        target=AutoEntitySelector.SELF,
        keyword=KeywordEnum.QUICKSTRIKE,
        round_only=True,
    )
    return Unit(summon_effect=effect)


# Daybreak: Invoke a Celestial card that costs 4, 5, or 6.
def SolariPriestess():
    effect = InvokeEffect(
        target=InvokeBaseCardFilter(cost=(4, 6)),
    )
    return Unit(play_daybreak=effect)


# Nightfall: Invoke.
def LunariPriestess():
    effect = InvokeEffect()
    return Unit(play_nightfall=effect)


# Play: If you Behold a Celestial card, grant an ally +1|+1 and SpellShield.
def GiddySparkleologist():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=1,
        health=1,
        keyword=KeywordEnum.SPELLSHIELD,
    )
    effect1 = TriggeredAction(
        event_filter=EntityEvents.PLAY,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
        condition=PlayerFlags.IS_BEHOLDING_CELESTIAL,
    )
    return Unit(effects=effect1)


# When I'm supported, give me +0|+3 this round.Support: Give my supported ally +3|+0 this round.
def FuzzyCaretaker():
    effect = BuffEffect(target=AutoEntitySelector.SELF, health=3, round_only=True)
    ta = TriggeredAction(
        event_filter=EntityEvents.SUPPORT,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
    )
    effect1 = SupportEffect(
        attack=3,
        round_only=True,
    )
    return Unit(effects=ta, support_effect=effect1)


# Nightfall: Grant me +2|+0.
def CrescentGuardian():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=2,
    )
    return Unit(play_nightfall=effect)


# ALL spells cost 1 more.
def StonySuppressor():
    effect = DynamicCostModifier(
        value=1, operator=Ops_.INCREMENT, target=TargetShorthand.ALL_SPELLS
    )
    return Unit(effects=effect)


# While in hand, I have a random keyword that changes each round.
# When I'm summoned, grant me this keyword.
def PatchedPorobot():
    value = ...
    # TODO randomizer
    effect = SetAttribute(
        target=AutoEntitySelector.SELF,
        attribute=AttrEnum.INTERNAL_VALUE,
        value=value,
    )
    ta = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START,
        action=effect,
        condition=...,
    )
    effect1 = AddKeywordEffect(
        target=AutoEntitySelector.SELF,
        keyword=EntityAttribute(
            target=AutoEntitySelector.SELF, attribute=AttrEnum.INTERNAL_VALUE
        ),
    )
    return Unit(effects=ta, summon_effect=effect1)


# Strike: Create a Gem in hand.
def MountainGoat():
    effect = CreateCardEffect(Set3Spells.Gem)
    return Unit(strike_effect=effect)


# Dragon allies cost 1 less.
def HeraldofDragons():
    effect = DynamicCostModifier(
        value=1,
        target=CardFilter(subtype=SubTypes_.DRAGON, location=None),
    )
    return Unit(effects=effect)


# Nexus Strike: Draw 1 and shuffle me into the top 3 cards of your deck.
def TheFlight():
    effect = DrawEffect()
    effect1 = MoveEffect(
        target=AutoEntitySelector.SELF, location=LocEnum.DECK, index=(0, 2)
    )
    # TODO randomize
    return Unit(nexus_strike_effect=(effect, effect1))


# When you heal a damaged ally, grant me +2|+0.
def StarShepherd():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=2,
    )
    effect1 = TriggeredAction(
        event_filter=EntityEvents.HEAL,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        action=effect,
    )
    return Unit(effects=effect1)


# Play: Discard 1 to Invoke a Celestial card that costs 3 or less.
def SpaceySketcher():
    effect = DiscardEffect(target=TargetShorthand.ALLIED_HAND_CARD)
    effect1 = InvokeEffect(
        target=InvokeBaseCardFilter(cost=(0, 3)), fizz_if_fail=effect
    )
    return Unit(play_effect=(effect, effect1))


# Common


OneForEachCelestialPlayed = BuffEffect(
    target=AutoEntitySelector.SELF,
    attack=PlayerStatistic.PLAYED_CELESTIAL_CARDS,
)


# When I'm summoned, grant me +1|+0 for each Celestial card you played this game.
# Attack: Give other allies +2|+2 and Overwhelm this round.
def TheScourge():
    effect = OneForEachCelestialPlayed
    effect2 = BuffEffect(
        target=AutoEntitySelector.ALL_ALLIED_UNITS,
        exclude_origin=True,
        attack=2,
        health=2,
        keyword=KeywordEnum.OVERWHELM,
        round_only=True,
    )
    Unit(attack_commit_effect=effect2, summon_effect=effect)


# When I'm summoned, grant me +1|+0 for each Celestial card you played this game. I am a Dragon.
def TheGreatBeyond():
    effect = OneForEachCelestialPlayed
    effect2 = DynamicAttributeModifier(
        attribute=AttrEnum.SUBTYPES, value=SubTypes_.DRAGON, operator=Ops_.PUSH
    )
    return Unit(effects=effect2, summon_effect=effect)


# When I'm summoned, grant me +1|+0 for each Celestial card you played this game.
# The first time I would die, fully heal me instead.
def TheImmortalFire():
    effect = OneForEachCelestialPlayed
    effect1 = HealEffect(target=AutoEntitySelector.SELF, value=None, heal_max=True)
    effect2 = ActionReplacement(
        event_filter=EntityEvents.DIE,
        replacement_action=effect1,
        activate_once=True,
        ally_enum=OriginEnum.T_SELF,
    )
    return Unit(effects=effect2, summon_effect=effect)


# When I'm summoned, grant me +1|+0 for each Celestial card you played this game.
def TheDestroyer():
    effect = OneForEachCelestialPlayed
    return Unit(summon_effect=effect)


#
def WrathfulRider():
    return Unit()


#
def TheWarrior():
    return Unit()


#
def TheSilverSister():
    return Unit()


# When I'm summoned, summon The Silver Sister.
def TheGoldenSister():
    effect = CreateCardEffect(
        TheSilverSister,
        LocEnum.HOMEBASE,
    )
    return Unit(summon_effect=effect)


#
def StalkingBroodmother():
    return Unit()


# Play: Stun enemies with 2 or less Power.
def SneakyZeebles():
    effect = PlaySkill(target=Set3Skills.Mischief)
    return Unit(play_effect=effect)


# Play: Heal an ally and your Nexus 3.
def ResplendentStellacorn():
    effect = HealEffect(
        target=TargetEntity(
            choices=EntityFilter(player=TargetPlayer.ORIGIN_OWNER, ensure_player=True)
        ),
        value=3,
    )
    return Unit(play_effect=effect)


#
def ScreechingDragon():
    return Unit()


# Play: Invoke.
def Moondreamer():
    effect = InvokeEffect()
    return Unit(play_effect=effect)


# Nightfall: Drain 2 from the enemy Nexus.
def Doombeast():
    effect = PlaySkill(target=Set3Skills.Torment)
    return Unit(play_nightfall=effect)


#
def FledglingStellacorn():
    return Unit()


# Support: Give my supported ally Quick Attack and +1|+0 this round.
def YoungWitch():
    effect = SupportEffect(attack=1, keyword=KeywordEnum.QUICKSTRIKE, round_only=True)
    return Unit(support_effect=effect)


# Support: Grant my supported ally +0|+2.
def TyaritheTraveler():
    effect = SupportEffect(health=2, round_only=True)
    return Unit(support_effect=effect)


# When I'm summoned, if you Behold an 8+ cost card, grant me +3|+0.
def TrollScavenger():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=3,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
        condition=PlayerFlags.IS_BEHOLDING_8_COST_CARD,
    )
    return Unit(effects=ta)


# When I'm summoned, refill 2 spell mana if you Behold a Nightfall card.
def TheSkyShadows():
    effect = RefillSpellMana(value=2)
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
        condition=Condition(
            target=TargetPlayer.ORIGIN_OWNER,
            condition=PlayerFlags.IS_BEHOLDING_X_CARD,
            parameter=BaseCardFilter(flags=CardFlags.HAS_NIGHTFALL),
        ),
    )
    return Unit(effects=ta)


# When I'm summoned, draw 1.
def TheMessenger():
    effect = DrawEffect()
    return Unit(summon_effect=effect)


# Last Breath: Create 2 copies of me in the enemy deck.
def PeskySpecter():
    effect = CreateCardEffect(
        PeskySpecter,
        LocEnum.DECK,
        owner=TargetPlayer.OPPONENT,
        quantity=2,
    )
    return Unit(last_breath_effect=effect)


#
def TheSerpent():
    return Unit()


# Round Start: Deal 2 to me.
def LoungingLizard():
    effect = DamageEffect(target=AutoEntitySelector.SELF, value=2)
    return Unit(round_start_effects=effect)


#
def Sparklefly():
    return Unit()


# When I'm summoned, create a Spring Gifts in hand.
def SpringGuardian():
    effect = CreateCardEffect(Set3Spells.SpringGifts)
    return Unit(summon_effect=effect)


#
def TastyFaefolk():
    return Unit()


# Play: Grant an ally Overwhelm.
def CrystalIbex():
    effect = AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        keyword=KeywordEnum.OVERWHELM,
    )
    return Unit(play_effect=effect)


# Daybreak: Give me Lifesteal this round.
def SolariSunforger():
    effect = AddKeywordEffect(
        target=AutoEntitySelector.SELF,
        keyword=KeywordEnum.LIFESTEAL,
        round_only=True,
    )
    return Unit(play_daybreak=effect)


# Play: Invoke.
def TheTraveler():
    effect = InvokeEffect()
    return Unit(play_effect=effect)


#
def WhiteflameProtector():
    return Unit()


#
def FusedFirebrand():
    return Unit()


# When I'm summoned, if you Behold an 8+ cost card, grant me Regeneration.
def TrollRavager():
    effect = AddKeywordEffect(
        target=AutoEntitySelector.SELF,
        keyword=KeywordEnum.REGENERATION,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
        condition=PlayerFlags.IS_BEHOLDING_8_COST_CARD,
    )
    return Unit(effects=ta)


#
def TheTrickster():
    return Unit()


# Play: Refill 8 mana.
# Play and Round Start: Give the strongest enemy Vulnerable this round.
def IcePillar():
    effect = RefillManaEffect(value=8)
    effect1 = AddKeywordEffect(
        target=AutoEntitySelector.STRONGEST_OPPONENT_BOARD_UNIT,
        keyword=KeywordEnum.VULNERABLE,
        round_only=True,
    )
    return Unit(play_effect=(effect, effect1), round_start_effects=effect1)


#
def DaringPoro():
    return Unit()


#
def ArmedGearhead():
    return Unit()


#
def Nyandroid():
    return Unit()
