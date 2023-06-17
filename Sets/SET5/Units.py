from random import choice
import Sets.SET1.Units as Set1Units
import Sets.SET1.Spells as Set1Spells
import Sets.SET2.Spells as Set2Spells
import Sets.SET2.Units as Set2Units
import Sets.SET3.Units as Set3Units
import Sets.SET3.Spells as Set3Spells
import Sets.SET4.Units as Set4Units
import Sets.SET5.Units as Set5Units
import Sets.SET5.Spells as Set5Spells
import Sets.SET5.Skills as Set5Skills
import Sets.SET4.Landmarks as Set4Landmarks
import Sets.SET5.Landmarks as Set5Landmarks
import Sets.SET5.Champions as Set5Champions

import Sets.SET6.Equipments as Set6Equipments
from actions.action_modifiers.silence import SilenceEffect
from actions.activations.copy_spell import CopySpellWithSameTargets
from actions.activations.multiple_activations import MultipleActivationsEffect
from actions.activations.negate_spell import NegateSpell
from actions.attachments.destroy import DestroyAttachmentsEffect, DestroyEquipEffect
from actions.attachments.equip import EquipEffect
from actions.attachments.forge import ForgeEffect
from actions.attachments.improvise import ImproviseEffect
from actions.attachments.transfer_equip import TransferEquipmentEffect
from actions.attack.challenge import ChallengeEffect
from actions.attack.free_attack import FreeAttackEffect
from actions.attack.overwhelm_effect import OverwhelmEffect
from actions.attribute.buff import BuffCostEffect, BuffEffect, BuffSupportEffect
from actions.attribute.buff_everywhere import BuffEverywhereEffect
from actions.attribute.countdown import AdvanceCountdownEffect
from actions.attribute.damage import DamageEffect
from actions.attribute.destroy_mana_gem import DestroyManaGem
from actions.attribute.drain import DrainEffect
from actions.attribute.frostbite import FrostbiteEffect
from actions.attribute.gain_mana_gem import GainManaGemEffect
from actions.attribute.heal import HealEffect
from actions.attribute.phase import PhaseMoonWeaponEffect
from actions.attribute.rally import RallyEffect
from actions.attribute.refill_mana import RefillManaEffect, RefillSpellMana
from actions.attribute.reveal import RevealEffect
from actions.attribute.set_attribute import SetAttribute
from actions.attribute.shuffle_attributes import StatShuffleEfect
from actions.attribute.support import SupportEffect
from actions.attribute.swap_attributes import SwapAttributesEffect
from actions.branching.branching_action import BranchingAction
from actions.champ.level_up import LevelupEffect
from actions.combination_action import CombinationAction
from actions.common.strike import MutualStrikeEffect, StrikeEffect
from actions.create.bladedance import BladedanceEffect

from actions.create.create_card import CreateCardEffect
from actions.create.create_copy import CreateCopyEffect, CreateExactCopyEffect
from actions.create.create_hand_cards import ReforgeEffect
from actions.create.fill_location import FillHandWithCards
from actions.create.invoke import InvokeEffect
from actions.create.manifest import ManifestEffect
from actions.create.post_events import CreatePostActParams
from actions.create.replace_deck import ReplaceDeck
from actions.create.summon_specific_cards import SpawnEffect, SummonHuskEffect
from actions.keywords.add_keyword import AddKeywordEffect, AddRandomKeywordEffect
from actions.create.tellstones import TellstonesEffect
from actions.keywords.keyword_multiplier import MultiplyKeywordValue
from actions.keywords.remove_keyword import (
    RemoveKeywordEffect,
)
from actions.keywords.stun_effect import StunEffect
from actions.meta.create_ta import CreateTriggeredAction
from actions.movement.capture import CaptureEffect
from actions.movement.discard import DiscardEffect
from actions.movement.draw import DrawEffect, TargetedDrawAction
from actions.movement.kill import DestroyLandmarkEffect, KillAction
from actions.movement.move import MoveEffect
from actions.movement.nba import NabEffect
from actions.movement.obliterate import ObliterateEffect
from actions.movement.predict import PredictEffect
from actions.movement.recall import RecallEffect
from actions.movement.revive import ReviveEffect
from actions.movement.summon import SummonEffect
from actions.movement.toss import TossEffect
from actions.postevent import PostEventParamGetter
from actions.reactions.action_negator import ActionNegator
from actions.reactions.action_replacement import ActionReplacement
from actions.reactions.dynamic_attr_modifier import (
    DynamicAttackModifier,
    DynamicCostModifier,
    DynamicKeywordModifier,
)
from actions.reactions.event_filter import EventFilter
from actions.reactions.onceyouve import OnceYouve
from actions.reactions.triggered_action import AllyOrigin_TA, TriggeredAction
from actions.reactions.value_triggered_action import ValueTriggeredAction
from actions.requisite.action_requisite import ActionRequisite
from actions.transform.transform import TransformEffect
from actions.traps.set_trap import (
    ActivateBoons,
    PlantChimes,
    PlantFlashBombTrap,
    PlantMysteriousPortalEffect,
    PlantPuffcaps,
    SetTrapEffect,
    TrapMultiplier,
)
from card_classes.spell import Spell
from card_classes.unit import Unit
from conditions.base_condition import Condition
from entity_selectors.base_card_filter import (
    BaseCardFilter,
    InvokeBaseCardFilter,
    ManifestBaseCardFilter,
)
from entity_selectors.card_filter import (
    CardFilter,
    DrawCardFilter,
    EntityFilter,
    StackSpellFilter,
)
from entity_selectors.input import ChoiceAction, ChoiceBaseCard, Input
from entity_selectors.target_game_card import TargetEntity
from entity_selectors.target_player import TargetPlayerInput
from enums.attribute import AttrEnum
from enums.card_rarity import CardRarity
from enums.card_sorters import CardSorter
from enums.counters import TrapEnums
from enums.deck_archetypes import DeckArchetypes
from enums.entity_events import EntityEvents
from enums.entity_pools import EntityPool
from enums.keywords import KeywordEnum
from enums.gamestate import GameStateEnums
from enums.location import LocEnum
from enums.operator import Ops_
from enums.origin_enum import OriginEnum
from enums.post_event_param import PostEventParam
from enums.spell_speed import SpellSpeedEnum
from enums.subtypes import SubTypes_
from enums.types import Types_
from events.event_query import EventQuery
from events.event_query_enum import EventQueryParamGetter, EventQueryTimeframe
from resolvable_enums.active_cards_selector import TargetShorthand
from resolvable_enums.auto_card_selector import AutoEntitySelector
from resolvable_enums.card_conditions import CardFlags
from resolvable_enums.player_conditions import PlayerFlags
from resolvable_enums.target_player import TargetPlayer
from value.branching_value import BranchingValue
from value.entity_attribute import EntityAttribute
from value.player_statistic import PlayerStatistic


# The first time you slay a unit with a spell, grant me +2|+1.
def BurgeoningSentinel():
    # CONDITION 
    action = BuffEffect(target=AutoEntitySelector.SELF, attack=2, health=1)
    effect = TriggeredAction(
        event=EntityEvents.SLAY,
        activate_once=True,
        action=action,
        ally_enum=OriginEnum.T_OPPO_O_ALLY,
        condition=...,
    )
    return Unit(effects=effect)


# Strike: Refill 1 spell mana.
def ForgeChief():
    effect = RefillSpellMana()
    return Unit(strike_effect=effect)


# When I�m summoned, summon a Scrappy Bomb.
def InventiveChemist():
    effect = CreateCardEffect(
        target=Set5Landmarks.ScrappyBomb,
        location=LocEnum.HOMEBASE,
    )
    return Unit(summon_effect=effect)


# When I'm summoned, create a Prank in hand.
def Otterpus():
    effect = CreateCardEffect(Set5Spells.Prank)
    return Unit(effects=effect, summon_effect=effect)


#
def PetriciteHound():
    return Unit()


#
def ProtoPoro():
    ...
    return Unit()


# To play, discard 1.
# When I'm discarded, summon an exact copy of me.
def RebornGrenadier():
    effect1 = DiscardEffect(
        target=CardFilter(
            location=LocEnum.HAND,
            type=None,
            exclude_origin=True,
        ),
    )
    effect = CreateExactCopyEffect(
        target=AutoEntitySelector.SELF, location=LocEnum.HOMEBASE
    )
    effect2 = TriggeredAction(
        event_filter=EntityEvents.DISCARD,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
    )
    return Unit(effects=effect2, play_requisite=effect1)


#
def SagaSeeker():
    return Unit()


# Last Breath: Create a copy of me in the enemy deck with 2 Poison Puffcaps attached.
def StinkyWhump():
    effect1 = PlantPuffcaps(
        quantity=2,
        target_cards=PostEventParam.CREATED,
        each=True,
    )
    effect = CreateCardEffect(
        StinkyWhump,
        LocEnum.DECK,
        target_player=TargetPlayer.OPPONENT,
        coevent=effect1,
    )
    return Spell(activation_effect=[effect, effect1])


# Nexus Strike: Recall me.
def TheMourned():
    effect = RecallEffect(target=AutoEntitySelector.SELF)
    return Unit(nexus_strike_effect=effect)


# Play: Create a Tiny Spear or a Tiny Shield in hand.
def YordleSquire():
    target = ChoiceBaseCard(choices=(Set5Spells.TinySpear, Set5Spells.TinyShield))
    effect = CreateCardEffect(target=target)
    return Unit(effects=effect)


# Nexus Strike: Draw a spell that costs 3 or less.
def AssistantLibrarian():
    effect = DrawEffect(filter_obj=DrawCardFilter(type=Types_.SPELL, cost=(0, 3)))
    return Unit(nexus_strike_effect=effect)


#
def HungryOwlcat():
    return Unit()


# Nexus Strike: Create a Hungry Owlcat in hand.
def BandleCommando():
    effect = CreateCardEffect(HungryOwlcat)
    return Unit(nexus_strike_effect=effect)


#
def LavaLizard():
    return Unit()


# Round End: If you've damaged the enemy Nexus this round, transform me into Lava Lizard.
def BitsyLizard():
    action = TransformEffect(target=AutoEntitySelector.SELF, new_form=LavaLizard)
    effect = TriggeredAction(
        event_filter=GameStateEnums.ROUND_END,
        action=action,
        activate_once=True,
        condition=PlayerFlags.PLUNDER,
    )
    return Unit(effects=effect)


# Play: Grant me Impact.
def BlastconeSeedling():
    effect = AddKeywordEffect(
        target=AutoEntitySelector.SELF, keyword=KeywordEnum.BARRIER
    )
    effect1 = AddKeywordEffect(
        target=AutoEntitySelector.SELF, keyword=KeywordEnum.IMPACT
    )
    effect2 = ChoiceAction(choices=[effect, effect1])
    return Unit(play_effect=effect2)


# When I'm summoned, create a random landmark that costs 2 or less in hand.
def BomberTwins():
    effect = CreateCardEffect(
        target=BaseCardFilter(cost=(0, 2), type=Types_.LANDMARK, quantity=1)
    )
    return Unit(summon_effect=effect)


# When I survive damage, deal 1 to the enemy Nexus.
def BoneScryer():
    action = DamageEffect(target=TargetPlayer.OPPONENT, value=1)
    effect = TriggeredAction(
        event_filter=EntityEvents.DAMAGE_SURVIVE,
        action=action,
        ally_enum=OriginEnum.T_SELF,
    )
    return Unit(effects=effect)


# Play: Manifest a spell from your regions that costs 3 or less.
def Conchologist():
    effect = ManifestEffect(
        choices=ManifestBaseCardFilter(
            type=Types_.SPELL,
            owner_same_regions=True,
            cost=(0, 3),
        ),
    )
    return Unit(play_effect=effect)


# When I'm summoned, create a Darkness in hand if you don't have one.
def DarkbulbAcolyte():
    effect = CreateDarknessIfNoneInHand
    return Unit(summon_effect=effect)


# When you summon another ally, grant it +0|+1.
def DurandSculptor():
    effect = BuffEffect(
        target=PostEventParam.TARGET,
        health=1,
        exclude_origin=True,
    )
    effect1 = TriggeredAction(
        event=EntityEvents.SUMMON, action=effect, ally_enum=OriginEnum.T_ALLY_O_ALLY
    )
    return Unit(effects=effect1)


#
def RisenRider():
    return Unit()


# When I'm discarded, create a Risen Rider in hand.
def FallenRider():
    effect = CreateCardEffect(RisenRider)
    effect1 = TriggeredAction(
        event_filter=EntityEvents.DISCARD, action=effect, ally_enum=OriginEnum.T_SELF
    )
    return Unit(effects=effect1)


# Play: Manifest a 6+ cost spell from your regions.
def FerrosFinancier():
    effect = ManifestEffect(
        choices=ManifestBaseCardFilter(
            cost=(6, 0), owner_same_regions=True, type=Types_.SPELL
        )
    )
    return Unit(play_effect=effect)


# The first time you discard a card or damage the enemy Nexus, grant me +2|+1.
def FixEmUppers():
    effect = BuffEffect(target=AutoEntitySelector.SELF, attack=2, health=1)
    effect1 = TriggeredAction(event_filter=..., action=effect, activate_once=True)
    # TODO multiple
    return Unit(effects=effect1)


# When I'm summoned, create a Hungry Owlcat in hand.When you summon another Fae, grant it +1|+0.
def GrandfatherFae():
    effect = BuffEffect(
        target=PostEventParam.TARGET,
        attack=1,
    )
    effect2 = CreateCardEffect(HungryOwlcat)
    effect1 = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
    )
    return Unit(effects=effect1, summon_effect=effect2)


# Play: Discard 1 to draw a unit.
def GravePhysician():
    effect = DiscardEffect(target=TargetShorthand.ALLIED_HAND_CARD)
    effect1 = DrawEffect(filter_obj=DrawCardFilter(), fizz_if_fail=effect)
    return Unit(play_effect=[effect, effect1])


#
def Grumbleslug():
    return Unit()


# When I'm summoned, create a Cloud Stance in hand.
def GustMonk():
    effect = CreateCardEffect(Set5Spells.CloudStance)
    return Unit(summon_effect=effect)


# Nexus Strike: Create a Prank in hand.
def KelpMaidens():
    effect = CreateCardEffect(Set5Spells.Prank)
    return Unit(nexus_strike_effect=effect)


# Play: Manifest a Celestial that costs 3 or less, Epic, or multi-region follower.
def LopingTelescope():
    a = InvokeBaseCardFilter(quantity=1, cost=(0, 3))
    b = BaseCardFilter(quantity=1, rarity=CardRarity.EPIC)
    c = BaseCardFilter(
        quantity=1,
        flags=[CardFlags.IS_FOLLOWER, CardFlags.IS_FOLLOWER],
    )
    effect = ManifestEffect(choices=[a, b, c])
    return Unit(effects=effect)


# When I'm summoned, if you've cast a spell this round, grant me Elusive.
def MaraiSongstress():
    effect = AddKeywordEffect(
        target=AutoEntitySelector.SELF,
        keyword=KeywordEnum.ELUSIVE,
    )
    effect1 = TriggeredAction(
        event_filter= EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
        condition=...
    )
    #TODO condition
    
    return Unit(summon_effect=effect)


# When I'm summoned, summon a random 1 cost follower.
def MaraiWarden():
    effect = CreateCardEffect(
        BaseCardFilter(cost=1, flags=CardFlags.IS_FOLLOWER, quantity=1),
        location=LocEnum.HOMEBASE,
    )
    return Unit(summon_effect=effect)


# Last Breath: Create a copy of me in hand at the next Round Start.
def Minion():
    effect = CreateCardEffect(Minion)
    effect2 = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START, action=effect, activate_once=True
    )
    effect1 = CreateTriggeredAction(triggered_action=effect2)
    return Unit(last_breath_effect=effect1)


#
def PetriciteBroadwing():
    return Unit()


# Strike: Plant 3 Poison Puffcaps on random cards in the enemy deck.
def PuffcapPup():
    effect = PlantPuffcaps(quantity=3, entire_deck=True)
    return Unit(strike_effect=effect)


#
def QuickQuill():
    return Unit()


# Play: Destroy an allied landmark to grant allied Ruinous Acolytes everywhere +1|+1.
def RuinousAcolyte():
    effect = DestroyLandmarkEffect(target=TargetShorthand.ALLIED_LANDMARK)
    effect1 = BuffEverywhereEffect(
        filter_obj=BaseCardFilter(card_class=RuinousAcolyte),
        attack=1,
        health=1,
        fizz_if_fail=effect,
    )
    return Unit(play_effect=[effect, effect1])


# Play: Discard 1 to Manifest a Mecha-Yordle.
def Squeaker():
    effect = DiscardEffect(target=TargetShorthand.ALLIED_HAND_CARD)
    effect1 = ManifestEffect(
        choices=ManifestBaseCardFilter(subtype=SubTypes_.MECHA_YORDLE),
        fizz_if_fail=effect,
    )
    return Unit(effects=[effect, effect1])


# Nexus Strike: Plant 2 Flashbomb Traps randomly in the top 10 cards of the enemy deck.
def StingOfficer():
    effect = PlantFlashBombTrap(quantity=2)
    return Unit(nexus_strike_effect=effect)


#
def StoneStackers():
    return Unit()

    # HERE


# When I'm summoned, grant me +1|+0 and a random keyword.
# I keep these stat buffs and keywords when I'm Recalled.
def TornadoWarrior():
    effect = BuffEffect(target=AutoEntitySelector.SELF, attack=1)
    effect1 = AddRandomKeywordEffect(target=AutoEntitySelector.SELF)
    # TODO retain
    return Unit(summon_effect=[effect, effect1])


# Play: Deal 1 to ALL Nexuses.
def TuskSpeaker():
    return Unit(unit_spell=Set5Spells.DanceofTusks)


# Strike: Grant your Darkness everywhere 1 extra damage.
def TwistedCatalyzer():
    effect = BuffEverywhereEffect(
        filter_obj=BaseCardFilter(card_class=Set5Spells.Darkness),
    )
    # TODO spell damage
    return Unit(strike_effect=effect)


# When I'm summoned, create a Stance Swap in hand.
def VulpineWanderer():
    effect = CreateCardEffect(Set5Spells.StanceSwap)
    return Unit(summon_effect=effect)


# When you summon another Yordle, grant it +1|+0.
def YordleExplorer():
    effect = BuffEffect(
        target=PostEventParam.TARGET,
        attack=1,
    )
    effect1 = TriggeredAction(
        event=EntityEvents.SUMMON, action=effect, ally_enum=OriginEnum.T_ALLY_O_ALLY
    )
    return Unit(effects=effect1)


# Attack: Give all allies with equal or less Power than me Quick Attack this round.
def YordleSmith():
    effect = AddKeywordEffect(
        target=CardFilter(attack=...),
        # TODO callable
        keyword=KeywordEnum.QUICKSTRIKE,
        round_only=True,
    )
    return Unit(attack_commit_effect=effect)


#
def ArenaKingpin():
    return Unit()


# When I'm summoned, create a Hungry Owlcat in hand.
def BabblingBalladeers():
    effect = CreateCardEffect(HungryOwlcat)
    return Unit(summon_effect=effect)


# Each round, the first multi-region unit you play costs 1 less.
# Play: Manifest a multi-region follower.
def BandleCityMayor():
    effect1 = ManifestEffect(
        choices=ManifestBaseCardFilter(
            flags=CardFlags.IS_MULTIREGION,
            is_follower=True,
        ),
    )
    effect2 = DynamicCostModifier
    # TODO the first
    return Unit(effects=effect2, play_effect=effect1)


# Play: Discard 1 to create a multi-region follower in hand.
def BandlePainter():
    effect = DiscardEffect(target=TargetShorthand.ALLIED_HAND_CARD)
    effect1 = ManifestEffect(
        choices=ManifestBaseCardFilter(
            flags=CardFlags.IS_MULTIREGION, is_follower=True
        ),
        fizz_if_fail=effect,
    )
    return Unit(play_effect=[effect, effect1])


# Play: Discard 1 to Manifest a Mecha-Yordle and grant it SpellShield.
def BilgeratRascal():
    effect = DiscardEffect(target=TargetShorthand.ALLIED_HAND_CARD)
    effect1 = ManifestEffect(
        choices=ManifestBaseCardFilter(subtype=SubTypes_.MECHA_YORDLE),
        fizz_if_fail=effect,
        keywords=KeywordEnum.SPELLSHIELD,
    )
    return Unit(effects=[effect, effect1])


# The first time you slay a unit with a spell, grant me +2|+1.
def BuhruSentinel():
    effect = BuffEffect(target=AutoEntitySelector.SELF, attack=2, health=1)
    effect1 = TriggeredAction(
        event=EntityEvents.SLAY,
        activate_once=True,
        action=effect,
        ally_enum=OriginEnum.T_OPPO_O_ALLY,
        condition=...
        # TODO condition
    )
    return Unit(effects=effect1)


# When an ally transforms, fully heal it and grant it +1|+1.
def ChiefNakotak():
    effect = HealEffect(target=PostEventParam.TARGET)
    effect1 = BuffEffect(target=PostEventParam.TARGET, attack=1, health=1)
    ta = TriggeredAction(
        event=EntityEvents.TRANSFORM,
        action=[effect, effect1],
        ally_enum=OriginEnum.T_ALLY,
    )
    return Unit(effects=ta)


# Support: Give my supported ally +0|+2 and Formidable this round.
def DurandArchitect():
    effect = SupportEffect(
        health=2,
        keyword=KeywordEnum.FORMIDABLE,
        round_only=True,
    )
    return Unit(support_effect=effect)


# Play: Grant an ally +0|+1 and Tough.
def DurandProtege():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        health=1,
        keyword=KeywordEnum.TOUGH,
    )
    return Unit(play_effect=effect)


# Last Breath: Summon a Sarcophagus.
def EndlessDevout():
    effect = CreateCardEffect(
        Set5Landmarks.Sarcophagus,
        LocEnum.HOMEBASE,
    )
    return Unit(last_breath_effect=effect)


# Each round, the first Fae you play costs 2 less.
def GleamingLantern():
    effect = DynamicCostModifier()
    # TODO the next you play
    return Unit(effects=effect)


# Grant Tech allies everywhere +1|+1 once you've cast a 6+ cost spell this game.
def HextechHandler():
    effect = BuffEverywhereEffect(
        filter_obj=BaseCardFilter(subtype=SubTypes_.TECH),
        attack=1,
        health=1,
    )
    effect1 = OnceYouve(
        state=PlayerFlags.HAS_PLAYED_A_6_COST_SPELL,
        action=effect
    )
    return Unit(effects=effect)


# Attack: Grant the top champion in your deck +1|+1 and a random keyword.
def Hothead():
    target_obj = CardFilter(
        location=LocEnum.DECK, flags=CardFlags.IS_CHAMPION, quantity=1
    )
    # TODO shareable cardfilter
    effect = BuffEffect(
        target=target_obj,
        attack=1,
        health=1,
    )
    effect1 = AddRandomKeywordEffect(target=target_obj)
    return Unit(attack_commit_effect=(effect, effect1))


# Play: Give an ally Spellshield and Overwhelm this round.
def Iula():
    effect1 = AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        keyword=[KeywordEnum.SPELLSHIELD, KeywordEnum.OVERWHELM],
        round_only=True,
    )
    return Unit(play_effect=effect1)


#
def JourneyingSandhopper():
    return Unit()


def MushroomRingEvaluator():
    ...
    # TODO custom function
    return


# When I'm summoned or Round Start: Give me Power this round equal to the number of other
# allied Fae in play or Attached.
def MushroomRing():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=MushroomRingEvaluator,
        round_only=True,
    )
    effect = TriggeredAction(event_filter=GameStateEnums.ROUND_START, action=effect)
    return Unit(summon_effect=effect, effects=effect)


# Grant me +2|+1 once you've discarded 3+ cards this game.
def NobleRebel():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=2,
        health=1,
    )
    effect1 = OnceYouve(
        state=...,
        action=effect
    )
    return Unit(effects=effect)


#
def PompousCavalier():
    return Unit()


# When I'm summoned, create a random 1, 2, and 3 cost follower in hand.
def ProfessorVonMech():
    a = BaseCardFilter(quantity=1, cost=1, flags=CardFlags.IS_FOLLOWER)
    b = BaseCardFilter(quantity=1, cost=2, flags=CardFlags.IS_FOLLOWER)
    c = BaseCardFilter(quantity=1, cost=3, flags=CardFlags.IS_FOLLOWER)
    effect = CreateCardEffect(
        target=[a, b, c],
    )
    return Unit(summon_effect=effect)


def CreateDarknessIfNoneInHand():
    effect = CreateCardEffect(
        Set5Spells.Darkness,
    )
    return TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
        condition=Condition(
            target=TargetPlayer.ORIGIN_OWNER,
            condition=PlayerFlags.HAS_NO_X_HAND_CARD,
            parameter=Set5Spells.Darkness,
        ),
    )


# When I'm summoned, create a Darkness in hand if you don't have one.
def SolariSentinel():
    effect = CreateDarknessIfNoneInHand()
    return Unit(effects=effect)


# Play: Pick a spell in the top 5 cards of your deck and create an exact Fleeting copy in hand.
def StationArchivist():
    effect = CreateExactCopyEffect(
        target=TargetEntity(
            choices=CardFilter(type=Types_.SPELL, location=LocEnum.DECK, top_x_cards=5)
        ),
        location=LocEnum.HAND,
        is_fleeting=True,
    )
    return Unit(play_effect=effect)


#
def MasaCrashingThunder():
    return Unit()


# When I�m summoned, if you�ve summoned a Thunder Fist this game,
# transform me into Masa, Crashing Thunder.
def ThunderFist():
    effect = TransformEffect(
        target=AutoEntitySelector.SELF,
        new_form=MasaCrashingThunder,
    )
    # TODO condition
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
        condition=...,
    )
    return Unit(effect=ta)


# When an allied landmark is destroyed, grant me +1|+1.
def WasteWalker():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=1,
        health=1,
    )
    effect1 = TriggeredAction(
        event=EntityEvents.DESTROY_LANDMARK,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        action=effect,
    )
    return Unit(effects=effect1)


# Round Start: Refill 1 spell mana.
def WizenedWizard():
    effect = RefillSpellMana()
    ta = TriggeredAction(event_filter=GameStateEnums.ROUND_START, action=effect)
    return Unit(effects=ta)


# When I�m summoned, give me +1|+0 and Elusive this round.
def WoodlandKeeper():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=1,
        round_only=True,
        keyword=KeywordEnum.ELUSIVE,
    )
    return Unit(summon_effect=effect)


#
def WoundedWhiteflame():
    return Unit()


# When I�m summoned, if you�ve added 2+ cards to your hand this round, grant me +1|+2.
def YordleNewbie():
    # TODO playerstatistic con
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=1,
        health=2,
    )
    ta = ValueTriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
        condition=...,
    )
    return Unit(effects=ta)


# When you cast a spell, give me +2|+0 this round.
def AbyssalGuard():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=2,
        round_only=True,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL,
        action=effect,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
    )
    return Unit(effects=ta)


# When I�m summoned, ALL players draw 1, then your opponent discards their highest cost card.
def AloofTravelers():
    effect = DrawEffect(player=TargetPlayer.ALL_PLAYERS)
    effect1 = DiscardEffect(
        target=CardFilter(
            owner=TargetPlayer.OPPONENT,
            location=LocEnum.HAND,
            type=None,
            sorter=CardSorter.EXPENSIVEST,
        )
    )
    return Unit(summon_effect=[effect, effect1])


# Play: Discard 1 to Manifest a Mecha-Yordle and reduce its cost by 1.
def ArenaPromoter():
    effect = DiscardEffect(target=TargetShorthand.ALLIED_HAND_CARD)
    effect1 = ManifestEffect(
        choices=ManifestBaseCardFilter(subtype=SubTypes_.MECHA_YORDLE),
        cost=(Ops_.DECREMENT, 1),
        fizz_if_fail=effect,
    )
    return Unit(effects=[effect, effect1])


# When I'm summoned, create 2 Pranks in hand.
def Benemone():
    effect = CreateCardEffect(Set5Spells.Prank, quantity=2)
    return Unit(summon_effect=effect)


# Play: Grant an ally +1|+1 and Silence an enemy follower.
def BlindedMystic():
    effect = BuffEffect(target=TargetShorthand.ALLIED_BOARD_UNIT, attack=1, health=1)
    effect2 = SilenceEffect(
        target=TargetEntity(
            choices=CardFilter(is_follower=True, owner=TargetPlayer.OPPONENT)
        )
    )
    return Unit(play_effect=[effect, effect2])


# When you summon another ally, grant me +1|+0.
def EmberMonk():
    effect = BuffEffect(target=AutoEntitySelector.SELF, attack=2, exclude_origin=True)
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
    )
    # TODO condition exclude self
    return Unit(effects=ta)


# Grant me +2|+0 once you've cast a 6+ cost spell this game.
def FerrosSkycruiser():
    effect = BuffEffect(target=AutoEntitySelector.SELF, attack=2, exclude_origin=True)
    return Unit(effects=effect)


# Allegiance: Summon another Yordle follower that costs 3 or less.
def GruffGrenadier():
    effect = CreateCardEffect(
        BaseCardFilter(cost=(0, 3), is_follower=True, subtype=SubTypes_.YORDLE),
        LocEnum.HOMEBASE,
    )
    return Unit(summon_effect=effect)


# Whenever your opponent draws, plant 1 Flashbomb Trap randomly in the top 10 cards in the enemy deck.
def JusticeRider():
    effect1 = PlantFlashBombTrap()
    ta = TriggeredAction(
        event_filter=EntityEvents.DRAW,
        action=effect1,
        ally_enum=OriginEnum.O_OPPO,
    )
    return Unit(effects=ta)


# Attack: Create a Fleeting Poison Dart in hand.
def LecturingYordle():
    effect = CreateCardEffect(
        Set5Spells.PoisonDart,
        is_fleeting=True,
    )
    return Unit(attack_commit_effect=effect)


# When I'm summoned, create 5 random 6+ cost spells in your deck and lower their cost to 3.
def MaraiGreatmother():
    effect = CreateCardEffect(
        BaseCardFilter(quantity=5, cost=(6, 0), type=Types_.SPELL),
        location=LocEnum.DECK,
        cost=(Ops_.DECREMENT, 3),
    )
    return Unit(summon_effect=effect)


# When I transform, draw a unit.
def MurkwolfRager():
    effect = DrawEffect(filter_obj=DrawCardFilter())
    ta = TriggeredAction(
        event_filter=EntityEvents.TRANSFORM,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
    )
    return Unit(effects=effect)


# Round End: If you've damaged the enemy Nexus this round, transform me into Murkwolf Rager.
def MurkwolfShaman():
    effect1 = TransformEffect(target=AutoEntitySelector.SELF, new_form=MurkwolfRager)
    ta = TriggeredAction(
        event_filter=GameStateEnums.ROUND_END,
        action=effect1,
        condition=PlayerFlags.PLUNDER,
    )
    return Unit(effects=ta)


# Each round, the first time you slay a unit with a spell, summon an Ephemeral Mistwraith.
def Mistkeepers():
    effect = CreateCardEffect(
        Set1Units.Mistwraith,
        LocEnum.HOMEBASE,
        is_ephemeral=True,
    )
    effect1 = TriggeredAction(
        event_filter=EntityEvents.SLAY,
        activations_per_round=1,
        condition=...,
        action=effect,
    )
    # TODO condition
    return Unit(effects=effect1)


# When I'm summoned, if you've destroyed 4+ allied landmarks this game, grant your champions everywhere +2|+2 and Overwhelm.
def HeraldoftheMagus():
    effect = BuffEverywhereEffect(
        filter_obj=BaseCardFilter(flags=CardFlags.IS_CHAMPION),
        attack=2,
        health=2,
        keyword=KeywordEnum.OVERWHELM,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
        condition=Condition(
            target=TargetPlayer.ORIGIN_OWNER,
            condition=PlayerFlags.HAS_DESTROYED_X_LANDMARKS,
            parameter=4,
        ),
    )
    return Unit(effects=ta)


# When I'm summoned or Attack: Create a Gem in hand.
def FreedColossus():
    effect = CreateCardEffect(Set3Spells.Gem)
    return Unit(summon_effect=effect, attack_commit_effect=effect)


# For every 2 spells you cast in a round, grant other allies +1|+1.
def FleetAdmiralShelly():
    effect = BuffEffect(
        target=CardFilter(),
        exclude_origin=True,
        attack=1,
        health=1,
    )

    # self.listener.on_event_counter(
    #     EntityEvents.ACTIVATE_SPELL,
    #     self.card_effect,
    #     2,
    #     subscriber=self,
    #     round=True,
    # )
    # # TODO value
    return Unit(effects=effect)


# When I'm summoned, grant Can't Block to the weakest enemy.Last Breath: Create a Risen Reckoner in hand.
def FallenReckoner():
    effect = AddKeywordEffect(
        target=CardFilter(
            quantity=1, sorter=CardSorter.WEAKEST, owner=TargetPlayer.OPPONENT
        ),
        keyword=KeywordEnum.CANT_ATTACK,
    )
    effect1 = CreateCardEffect(RisenReckoner)
    return Unit(summon_effect=effect, last_breath_effect=effect1)


# When I'm summoned, grant Can't Block to the weakest enemy.
def RisenReckoner():
    effect = AddKeywordEffect(
        target=CardFilter(
            quantity=1, sorter=CardSorter.WEAKEST, owner=TargetPlayer.OPPONENT
        ),
        keyword=KeywordEnum.CANT_ATTACK,
    )
    return Unit(summon_effect=effect)


# When I'm discarded, grant your strongest ally +2|+0.
def AncientWarmonger():
    effect = BuffEffect(
        target=AutoEntitySelector.STRONGEST_BOARD_UNIT,
        attack=2,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.DISCARD, action=effect, ally_enum=OriginEnum.T_SELF
    )
    return Unit(effects=ta)


# When you summon another ally with equal or less Power than me, grant it +1|+1.
def YordleCaptain():
    effect = BuffEffect(
        target=PostEventParam.TARGET,
        attack=1,
        health=1,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        condition=...,
    )
    # TODO condition
    return Unit(effects=ta)


# Each round, the first time you slay a unit with a spell, deal 2 to the enemy Nexus.
def WatcherontheIsles():
    effect = DamageEffect(target=TargetPlayer.OPPONENT, value=2)
    ta = TriggeredAction(
        event_filter=EntityEvents.SLAY,
        activations_per_round=1,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
        condition=...,
    )
    # TODO condition
    return Unit(effects=ta)


# When a non-Fleeting ally in hand is discarded, create a Fleeting copy of it in hand.
def TheLadyofBlood():
    effect = CreateCopyEffect(
        PostEventParam.TARGET,
        is_fleeting=True,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.DISCARD,
        action=effect,
        ally_enum=OriginEnum.T_ALLY,
        condition=...,
    )
    # TODO condition
    return Unit(effects=effect)


#
def BassofBurden():
    return Unit()


# When I'm summoned, if you've played a created card or killed a unit with a spell this game,
# summon a Bass of Burden.
def TenorofTerror():
    # TODO cONDITION
    effect = CreateCardEffect(BassofBurden, LocEnum.BOARD)
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
        condition=(PlayerFlags),
    )
    return Unit(effects=ta)


# Round Start: Deal 1 to the enemy Nexus.
def Terrordactyl():
    effect = DamageEffect(
        target=TargetPlayer.OPPONENT,
        value=1,
    )
    return Unit(round_start_effects=effect)


# Round End: If you've damaged the enemy Nexus this round, transform me into Terrordactyl.
def Teenydactyl():
    effect = TransformEffect(
        target=AutoEntitySelector.SELF,
        new_form=Terrordactyl,
    )
    ta = TriggeredAction(
        event_filter=GameStateEnums.ROUND_END,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
        condition=PlayerFlags.PLUNDER,
    )
    return Unit(effects=ta)


# When I�m summoned, if you've added 2+ cards to your hand this round, grant me +1|+0 and Elusive.
def SwoleScout():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=1,
        keyword=KeywordEnum.ELUSIVE,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
        condition=Condition(
            target=TargetPlayer.ORIGIN_OWNER,
            condition=PlayerFlags.HAS_ADDED_CARDS_TO_HAND_THIS_ROUND,
            parameter=2,
        ),
    )
    return Unit(effects=ta)


# When I'm summoned, reduce the cost of your Darkness everywhere by 1.
def StiltedRobemaker():
    effect = BuffEverywhereEffect(
        cost=1,
        filter_obj=BaseCardFilter(
            card_type=Set5Spells.Darkness,
        ),
    )
    return Unit(summon_effect=effect)


# Support: I take all damage for my supported ally this round.
def PetriciteStag():
    return Unit()
    # TODO tamper


#
def Rainbowfish():
    return Unit()


#
def ScholarlyClimber():
    return Unit()


# Costs 2 less if you've Recalled a unit this round.
def PathlessAncient():
    con = EventHasHappened(EventQuery(event=EntityEvents.RECALL, this_round=True))
    effect = DynamicCostModifier(value=2, condition=con)
    return Unit(effects=effect)


# Fury grants me +0|+2 instead of +1|+1.
def MountainDrake():
    effect = ...
    ta = TriggeredAction(
        event_filter=EntityEvents.FURY,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
        condition=...,
    )
    # TODO FURY gives me 0/2
    return Unit(effects=...)


# When I�m summoned, create a Most Wanted in hand.
def OfficerSquad():
    effect = CreateCardEffect(Set5Spells.MostWanted)
    return Unit(summon_effect=effect)


# Play me on an ally to give it my stats and keywords while I'm Attached. When that ally leaves play, Recall me.
def PapercraftDragon():
    return Unit()


# Attack: Summon an attacking random 1 cost Poro.
def PoroSled():
    effect = CreateCardEffect(
        target=BaseCardFilter(quantity=1, cost=1, subtype=SubTypes_.PORO),
        location=LocEnum.BATTLEFIELD,
    )
    return Unit(attack_commit_effect=effect)


#
def Stormcloud():
    effect = AddKeywordEffect(
        target=AutoEntitySelector.SELF, keyword=KeywordEnum.IMPACT, quantity=3
    )
    return Unit(effects=effect)


# When I'm summoned, summon a Stormcloud.
def RissuTheSilentStorm():
    effect = CreateCardEffect(Stormcloud, LocEnum.HOMEBASE)
    return Unit(summon_effect=effect)


# When I'm summoned, draw 1. If you drew a landmark, repeat this effect.
def Sandseer():
    effect = DrawEffect()
    # TODO effect looper
    return Unit(effects=effect)


# When I transform, deal 1 to all enemies.
def GigaGromp():
    effect = DamageEffect(
        target=AutoEntitySelector.ALL_OPPONENT_UNITS,
        value=1,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.TRANSFORM,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
    )
    return Unit(effects=ta)


# Round End: If you've damaged the enemy Nexus this round, transform me into Giga Gromp.
def SpottedToad():
    effect1 = TransformEffect(
        target=AutoEntitySelector.SELF,
        new_form=GigaGromp,
    )
    ta = TriggeredAction(
        event_filter=GameStateEnums.ROUND_END,
        action=effect1,
        condition=PlayerFlags.PLUNDER,
    )
    return Unit(effects=ta)


# Each round, the first time you Recall a follower, summon an exact Ephemeral copy of it.
def TailCloakMatriarch():
    effect = CreateCardEffect(
        target=PostEventParam.TARGET,
        location=LocEnum.HOMEBASE,
        is_ephemeral=True,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.RECALL,
        action=effect,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        activations_per_round=1,
    )
    return Unit(effects=ta)


# Attack: Give other attacking allies +2|+0 this round.
def ArenaMechacaster():
    effect = BuffEffect(
        target=CardFilter(),
        exclude_origin=True,
        attack=2,
        round_only=True,
    )
    return Unit(attack_commit_effect=effect)


# When I'm summoned or Round End: Plant 3 Poison Puffcaps on random cards in the enemy deck.
# Traps on enemy cards are doubled when activated.
def AvaAchiever():
    effect = SetTrapEffect(
        quantity=3,
        entire_deck=True,
    )
    # TODO trap
    effect1 = TrapMultiplier()
    double_effect = TriggeredAction(
        event_filter=EntityEvents.ACTIVATE_TRAP,
        action=effect1,
        ally_enum=OriginEnum.T_OPPO,
        condition=...,
    )
    return Unit(effects=double_effect, summon_effect=effect, round_end_effects=effect)


# If you would get a mana gem, instead refill your spell mana.When you cast a spell, create in hand a random spell that costs 3 or less and give it Fleeting.
def AvataroftheTides():
    effect1 = RefillSpellMana(value=Ops_.MAX)
    refill = ActionReplacement(
        event_filter=EntityEvents.GAIN_MANA_GEM,
        replacement_action=effect1,
        ally_enum=OriginEnum.T_ALLY,
    )
    effect = CreateCardEffect(
        target=BaseCardFilter(type=Types_.SPELL, cost=(0, 3)),
        is_fleeting=True,
        quantity=1,
    )
    create = TriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL,
        action=effect,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
    )
    return Unit(effects=[create, refill])


# When I'm summoned, if you've targeted allies 6+ times this game, grant me
# Spellshield, Overwhelm, and Challenger.
def CamphortheDoubt():
    # TODO CONDITION
    effect = AddKeywordEffect(
        target=AutoEntitySelector.SELF,
        keyword=(
            KeywordEnum.SPELLSHIELD,
            KeywordEnum.OVERWHELM,
            KeywordEnum.CHALLENGER,
        ),
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
        condition=...,
    )
    return Unit(effects=ta)


# Play: Plant 5 Flashbomb Traps randomly or
# activate the effects of all traps in the top 5 cards of the enemy deck.
def CorinaMastermind():
    return Unit(unit_spell=Set5Spells.BeguilingBlossom)


# When you pick a non-champion card from randomly selected options,
# create a copy in hand and reduce its cost by 1.
def CuriousShellfolk():
    effect = CreateCardEffect(
        target=PostEventParamGetter(effect=effect1, parameter=PostEventParam.TARGET),
        cost=(Ops_.DECREMENT, 1),
    )
    effect1 = TriggeredAction(
        event=EntityEvents.CARD_OPTION_SELECT,
        ally_enum=OriginEnum.T_ALLY,
        action=effect,
        condition=CardFlags.IS_NON_CHAMPION,
    )
    return Unit(effects=effect)


# When I'm summoned, create a Stance Swap in hand. It costs 0 this round.
def HyaraAllseer():
    effect = CreateCardEffect(Set5Spells.StanceSwap)
    effect1 = BuffCostEffect(
        target=PostEventParam.CREATED,
        value=0,
        round_only=True,
        operator=Ops_.SET,
    )
    return Unit(summon_effect=(effect, effect1))


# When I'm summoned, create a Darkness in hand if you don't have one.
# When you play your next Darkness this round, copy it targeting the enemy Nexus.
def IxtaliSentinel():
    effect = CreateDarknessIfNoneInHand()
    # TODO RECAST different target
    return Unit(effects=effect)


# Round Start: Grant me +2|+2.
def MammothRager():
    effect1 = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=2,
        health=2,
    )
    ta = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START,
        action=effect1,
    )
    return Unit(effects=ta)


# Round End: If you've damaged the enemy Nexus this round, transform me into Mammoth Rager.
def MammothShaman():
    effect1 = TransformEffect(
        target=AutoEntitySelector.SELF,
        new_form=MammothRager,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect1,
        condition=PlayerFlags.PLUNDER,
    )
    return Unit(effects=ta)


# Round Start: Create a Inspection Passed! in hand.
def SafetyInspector():
    effect = CreateCardEffect(Set5Spells.InspectionPassed)
    ta = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START,
        action=effect,
    )
    return Unit(effects=ta)


# When I'm summoned, draw 2 and give all allies +1|+1 this round.
def SainenThousandTailed():
    effect = DrawEffect(quantity=2)
    effect1 = BuffEffect(target=CardFilter(), attack=1, health=1, round_only=True)
    return Unit(summon_effect=[effect, effect1])


# Play: Recall a unit.
def Windsinger():
    return Unit(unit_spell=Set5Spells.Gust)


# Attack: Grant all allies with equal or less power than me +0|+1.
def YordleRanger():
    # TODO custom func
    effect = BuffEffect(
        target=CardFilter(attack=...),
        health=1,
    )
    return Unit(attack_commit_effect=effect)


# When I'm summoned, draw Jayce. Attack:
# Deal 1 to the enemy Nexus. For each 6+ cost spell you've cast this game, increase it by 1.
def AlbusFerros():
    # TODO dynamic action modifier
    effect = DrawEffect(filter_obj=DrawCardFilter(card_type=Set5Champions.Jayce))
    effect1 = DynamicAttackModifier
    return Unit(effects=Set5Skills.FerrosDividend, summon_effect=effect)


# When I'm summoned, if you've dealt damage to the enemy Nexus 4+ times, grant me Impact 4 times.
def FuriousFaefolk():
    con = Condition(
        target=TargetPlayer.ORIGIN_OWNER,
        condition=PlayerFlags.DEALT_DAMAGE_TO_NEXUS_X_TIMES,
        parameter=4,
    )
    effect = AddKeywordEffect(
        target=AutoEntitySelector.SELF, keyword=KeywordEnum.IMPACT, quantity=4
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
        condition=con,
    )
    return Unit(effects=ta)


#
def MiniMinitee():
    return Unit()


# Round Start: Transform the strongest enemy into a 3|3 Mini-Minitee and Silence it.
# It can't block.
def Megatee():
    # TODO same target different effects
    target_obj = TargetEntity(choices=AutoEntitySelector.STRONGEST_BOARD_UNIT)
    effect1 = TransformEffect(target=target_obj)
    effect2 = SilenceEffect(target=target_obj)
    effect3 = AddKeywordEffect(target=target_obj, keyword=KeywordEnum.CANT_ATTACK)
    return Unit(round_start_effects=(effect1, effect2, effect3))


# Round End: If you've damaged the enemy Nexus this round, transform me into Megatee.
def Minitee():
    effect = TransformEffect(
        target=AutoEntitySelector.SELF,
        new_form=Megatee,
    )
    effect1 = TriggeredAction(
        event_filter=GameStateEnums.ROUND_END,
        action=effect,
        activate_once=True,
        condition=PlayerFlags.PLUNDER,
    )
    return Unit(effects=effect1)


#
def ShortTooth():
    return Unit()


# When allies attack, spend 1 spell mana to summon an attacking Short Tooth.
def SharkTrainer():
    # TODO spend mana
    effect1 = ...
    effect = CreateCardEffect(ShortTooth, LocEnum.BATTLEFIELD, fizz_if_fail=effect1)
    effect1 = TriggeredAction(
        event_filter=EntityEvents.PLAYER_ATTACK_COMMIT,
        action=effect,
    )
    return Unit(effects=effect1)


# When I'm summoned, if you've summoned units from 4+ regions this game, grant me Impact 4 times.
def BandleGunners():
    con = Condition(
        target=TargetPlayer.ORIGIN_OWNER,
        condition=PlayerFlags.HAS_SUMMONED_UNITS_FROM_X_REGIONS,
        parameter=4,
    )
    effect = AddKeywordEffect(
        target=AutoEntitySelector.SELF, keyword=KeywordEnum.IMPACT, quantity=4
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        action=effect,
        condition=con,
        ally_enum=OriginEnum.T_SELF,
    )
    return Unit(summon_effect=ta)


# When I'm summoned, create a Darkness in hand if you don't have one.
# Your next Darkness this round costs 0 and gains �I deal damage to all enemy targets.�
def DessandAda():
    effect = CreateDarknessIfNoneInHand()
    # TODO future card
    return Unit(effects=effect)


# Last Breath: Create a Lost Soul in hand.
def TwinbladeRevenant():
    effect = CreateCardEffect(LostSoul)
    return Unit(last_breath_effect=effect)


# When I'm summoned or discarded, create a Twinblade Revenant in hand.
def LostSoul():
    effect = CreateCardEffect(TwinbladeRevenant)
    ta = TriggeredAction(
        event_filter=(EntityEvents.SUMMON, EntityEvents.DISCARD),
        ally=OriginEnum.T_SELF,
        action=effect,
    )
    return Unit(effects=ta)


# When you play a created follower, summon an exact copy.
# When you play a created spell, cast it again on the same targets.
def MirrorMage():
    effect1 = CreateExactCopyEffect(
        target=PostEventParam.TARGET,
        location=LocEnum.HOMEBASE,
    )
    effect2 = RecastActionSameTargets(target=PostEventParam.TARGET)
    effect3 = TriggeredAction(
        event=EntityEvents.PLAY_UNIT,
        action=effect1,
        condition=Condition(
            target=PostEventParam.TARGET, condition=CardFlags.IS_FOLLOWER
        ),
    )
    effect4 = TriggeredAction(
        event=EntityEvents.PLAY_SPELL,
        action=effect2,
        condition=Condition(
            target=PostEventParam.TARGET, condition=CardFlags.IS_CREATED
        ),
    )
    return Unit(effects=(effect3, effect4))


# When I'm summoned, grant me a random keyword for each allied landmark you've destroyed this game.
# When you destroy an allied landmark, grant me a random keyword.
def TheArsenal():
    effect = AddRandomKeywordEffect(
        target=AutoEntitySelector.SELF,
        count=PlayerStatistic.ALLIED_LANDMARKS_DESTROYED,
    )
    effect3 = AddRandomKeywordEffect(
        target=AutoEntitySelector.SELF,
        count=1,
    )
    effect2 = TriggeredAction(
        event=EntityEvents.DESTROY_LANDMARK,
        action=effect3,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
    )
    return Unit(summon_effect=effect, effects=effect2)


# When I'm summoned, swap my Health and your Nexus' Health.
# I can't be blocked by enemies with less Health than me.
def GorliththeUnscalable():
    effect = SwapAttributesEffect(
        target=AutoEntitySelector.SELF,
        second_entity=TargetPlayer.ORIGIN_OWNER,
        target_attr=AttrEnum.HEALTH,
        second_entity_attr=AttrEnum.HEALTH,
    )
    effect1 = ActionNegator(event=EntityEvents.BLOCK)
    # NEGATOR
    return Unit(effects=effect1, summon_effect=effect)


#
def ForgeWorker():
    return Unit()


# """
# MECHA-YORDLE
# """


# To play me, discard a unit.
# Last Breath: Summon an exact copy of the discarded unit.
def LilDipper():
    effect = DiscardEffect(target=TargetShorthand.ALLIED_HAND_UNIT)
    effect2 = CreateExactCopyEffect(
        target=PostEventParamGetter(effect=effect, parameter=...),
        location=LocEnum.HOMEBASE,
    )
    # TODO saved value
    return Unit(last_breath_effect=effect, play_effect=effect2)


# When I'm summoned, grant me Impact twice.
def SmashDash():
    effect = AddKeywordEffect(
        target=AutoEntitySelector.SELF,
        keyword=KeywordEnum.IMPACT,
        quantity=2,
    )
    return Unit(summon_effect=effect)


#
def BouncerBolt():
    return Unit()


# Attack: Double my Power and Impact.
def Earthshaker():
    effect = BuffEffect(
        target=AutoEntitySelector.SELF, attack=2, operator=Ops_.MULTIPLY
    )
    effect1 = MultiplyKeywordValue(
        target=AutoEntitySelector.SELF, keyword=KeywordEnum.IMPACT, multiplier=2
    )
    return Unit(effects=[effect, effect1])


#
def ShadowtechWalker():
    return Unit()


# Attack: Grant the top 3 allies in your deck +1|+1.
def FuryhornCrasher():
    effect = BuffEffect(
        target=CardFilter(top_x_cards=3, location=LocEnum.DECK),
        health=1,
        attack=1,
    )
    return Unit(attack_commit_effect=effect)


# Support: Give my supported ally SpellShield and +2|+2 this round.
def GeodeMechaforcer():
    effect = SupportEffect(
        attack=2,
        health=1,
        keyword=KeywordEnum.SPELLSHIELD,
        round_only=True,
    )
    return Unit(support_effect=effect)


# When I'm summoned, grant other allies +1|+1.
def Trumpetecher():
    effect = BuffEffect(
        target=CardFilter(exclude_origin=True),
        health=1,
        attack=1,
    )
    return Unit(summon_effect=effect)


# When I'm summoned or Round Start: Grant me +0|+2 for each card you discarded last round,
# then shuffle my stats.
def SaltySpinner():
    value = ...
    # TODO custom function
    effect = BuffEffect(target=AutoEntitySelector.SELF, health=value)
    effect1 = StatShuffleEfect(target=AutoEntitySelector.SELF)
    return Unit(summon_effect=(effect, effect1), round_start_effects=(effect, effect1))


# Attack: Summon 2 attacking Sand Soldiers.
def DunehopperMech():
    effect = CreateCardEffect(Set4Units.Sandsoldier, LocEnum.BATTLEFIELD, quantity=2)
    return Unit(attack_commit_effect=effect)


# When I'm summoned, summon a random 1 cost follower from your regions.
# When I'm Recalled, transform me into Nine Lives.
def LiminalGuardian():
    effect1 = CreateCardEffect(
        target=BaseCardFilter(
            quantity=1,
            cost=1,
            owner_same_regions=True,
            flags=CardFlags.IS_FOLLOWER,
        ),
        location=LocEnum.HOMEBASE,
    )
    effect = TransformEffect(
        target=AutoEntitySelector.SELF,
        new_form=Set5Spells.NineLives,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.RECALL, action=effect, ally_enum=OriginEnum.T_SELF
    )
    return Unit(effects=ta, summon_effect=effect1)
