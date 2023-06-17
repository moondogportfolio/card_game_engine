from random import choice
import Sets.SET1.Units as Set1Units
import Sets.SET1.Spells as Set1Spells
import Sets.SET2.Spells as Set2Spells
import Sets.SET2.Units as Set2Units
import Sets.SET3.Units as Set3Units
import Sets.SET3.Spells as Set3Spells
import Sets.SET4.Spells as Set4Spells
import Sets.SET4.Units as Set4Units
import Sets.SET5.Units as Set5Units
import Sets.SET4.Landmarks as Set4Landmarks
import Sets.SET5.Landmarks as Set5Landmarks
import Sets.SET5.Champions as Set5Champions
import Sets.SET5.Spells as Set5Spells
from Sets.SET6.CustomSpells import FrozeninFearEffect, ProximityPuffcapEffect, SecondSkinEffect, SneezyBiggledustEffect

import Sets.SET6.Units as Set6Units
import Sets.SET6.Champions as Set6Champions

import Sets.SET6.Equipments as Set6Equipments
from actions.action_modifiers.silence import SilenceEffect
from actions.activations.alternative_effect import AlternativeActivationEffect
from actions.activations.copy_spell import CopySpellWithSameTargets
from actions.activations.multiple_activations import MultipleActivationsEffect
from actions.activations.negate_spell import NegateSpell
from actions.activations.recast_spell import RecastEventOfAction
from actions.attachments.destroy import DestroyAttachmentsEffect, DestroyEquipEffect
from actions.attachments.equip import EquipEffect
from actions.attachments.forge import ForgeEffect
from actions.attachments.improvise import ImproviseEffect
from actions.attachments.transfer_equip import TransferEquipmentEffect
from actions.attachments.unequip import UnequipEffect
from actions.attack.challenge import ChallengeEffect
from actions.attack.free_attack import FreeAttackEffect
from actions.attack.overwhelm_effect import OverwhelmEffect
from actions.attribute.buff import BuffCostEffect, BuffEffect
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
from actions.branching.branching_action import BranchingAction
from actions.champ.level_up import LevelupEffect
from actions.combination_action import CombinationAction
from actions.common.strike import MutualStrikeEffect, StrikeEffect
from actions.create.bladedance import BladedanceEffect

from actions.create.create_card import CreateCardEffect
from actions.create.create_copy import CreateExactCopyEffect
from actions.create.create_hand_cards import ReforgeEffect
from actions.create.fill_location import FillHandWithCards
from actions.create.invoke import InvokeEffect
from actions.create.manifest import ManifestEffect
from actions.create.post_events import CreatePostActParams
from actions.create.replace_deck import ReplaceDeck
from actions.create.summon_specific_cards import SpawnEffect, SummonHuskEffect
from actions.keywords.add_keyword import AddKeywordEffect, AddRandomKeywordEffect
from actions.create.tellstones import TellstonesEffect
from actions.keywords.remove_keyword import (
    PurgeKeywordsEffect,
    RemoveKeywordEffect,
)
from actions.keywords.stun_effect import StunEffect
from actions.meta.create_ta import CreateTriggeredAction
from actions.movement.capture import CaptureEffect
from actions.movement.discard import DiscardEffect
from actions.movement.draw import (
    DrawEffect,
    DrawSpecificReturnRestEffect,
    TargetedDrawAction,
)
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
from actions.reactions.action_modifier import ActionModifier
from actions.reactions.action_negator import ActionNegator
from actions.reactions.action_replacement import ActionReplacement
from actions.reactions.dynamic_attr_modifier import (
    DynamicAttackModifier,
    DynamicCostModifier,
    DynamicKeywordModifier,
)
from actions.reactions.event_filter import EventFilter
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


# For the rest of the game, when you Blade Dance, summon another attacking Blade.
# Blade Dance 1.
def StormofBlades():
    effect = BladedanceEffect(quantity=1)
    effect1 = CreateCardEffect(
        target=Set4Units.Blade,
        location=LocEnum.BATTLEFIELD,
        triggering_effect=effect2,
    )
    effect2 = AllyOrigin_TA(action=effect1, event_filter=EntityEvents.BLADE_DANCE)
    create = CreateTriggeredAction(triggered_action=effect2)
    return Spell(activation_effect=[effect, create])


# Create a Fleeting Shady Character or Chempunk Shredder in hand and reduce its cost by 1.
def DiscreetInvitation():
    effect1 = ChoiceBaseCard(
        choices=[Set1Units.ChempunkShredder, Set1Units.ShadyCharacter]
    )
    effect = CreateCardEffect(target=effect1, cost=1)
    return Spell(activation_effect=effect)


# Nagakabouros starts a free attack with 4 Nagakabouros' Tentacle.
def NagakabourosTantrum():
    effect1 = FreeAttackEffect(target=AutoEntitySelector.NAGAKABOUROS_MINIONS)
    effect = CreateCardEffect(
        target=Set6Units.NagakabourosTentacle,
        quantity=4,
        location=LocEnum.BATTLEFIELD,
    )
    return Spell(activation_effect=[effect1, effect])


# Deal 2 to a unit and summon a Scrappy Bomb.
def DroptheBomb():
    effect = DamageEffect(target=TargetShorthand.ANY_BOARD_UNIT)
    effect1 = CreateCardEffect(
        target=Set5Landmarks.ScrappyBomb, location=LocEnum.HOMEBASE
    )
    return Spell(activation_effect=[effect, effect1])


# Give allies +1|+1 this round. If they're created, give them +2|+2 instead.
def SneezyBiggledust():
    return Spell(activation_effect=SneezyBiggledustEffect())


# Deal 3 to an enemy unit.Spawn 3.Deal 1 to the enemy Nexus.
def RiptideSermon():
    effect = DamageEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT, value=3)
    effect1 = SpawnEffect(quantity=3)
    effect2 = DamageEffect(target=TargetPlayer.OPPONENT, value=1)
    return Spell(activation_effect=[effect, effect1, effect2])


# Manifest a follower you can afford.
def RansomRiches():
    effect = ManifestEffect(target=BaseCardFilter(is_follower=True, can_afford=True))
    return Spell(activation_effect=effect)


# Summon an Honored Lord.
def RoyalDecree():
    effect = CreateCardEffect(target=..., location=LocEnum.HOMEBASE)
    effect1 = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        keyword=KeywordEnum.CHALLENGER,
        attack=2,
        health=2,
        round_only=True,
    )
    effect2 = ChoiceAction(choices=[effect, effect1])
    return Spell(activation_effect=effect2)


# Create a Fleeting More Powder!, Playful Trickster, or Chum the Waters in hand.
def BilgewaterTellstones():
    effect = CreateCardEffect(
        is_fleeting=True,
        target=ChoiceBaseCard(
            choices=[
                Set2Spells.MorePowder,
                Set2Spells.PlayfulTrickster,
                Set2Spells.ChumtheWaters,
            ]
        ),
    )
    return Spell(activation_effect=effect)


# Summon a random Husk and grant it +1|+0.
def Allure():
    effect = SummonHuskEffect(attack=(Ops_.INCREMENT, 1))
    return Spell(activation_effect=effect)


# Summon a Keeper of Masks. Draw 1.
def KinkousCall():
    # TODO alternative effect
    effect = CreateCardEffect(target=Set1Units.KeeperofMasks, location=LocEnum.HOMEBASE)
    ta = TriggeredAction(
        event=GameStateEnums.ROUND_START,
        action=effect,
        activate_once=True,
    )
    effect1 = CreateTriggeredAction(triggered_action=ta)
    effect2 = DrawEffect()
    effect3 = ChoiceAction(choices=(effect, effect1))
    return Spell(activation_effect=(effect3, effect2))


# Frostbite an enemy.Summon a Rimefang Pack.
# Grant it +1|+1 for each time you've Frostbitten enemies this game.
def FrozeninFear():
    effect = FrozeninFearEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT)
    return Spell(activation_effect=effect)


# Grant an enemy "Frostbite me at the next Round Start."
def CrackingIce():
    effect = FrostbiteEffect(target=AutoEntitySelector.ORIGIN)
    ta = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START,
        effect=effect,
        activate_once=True,
    )
    effect1 = CreateTriggeredAction(
        triggered_action=ta,
        target=TargetShorthand.OPPONENT_BOARD_UNIT,
    )
    return Spell(activation_effect=effect1)


# Transform an allied follower into an Alpha Wildclaw.
def WildclawsFerocity():
    effect = TransformEffect(
        target=TargetShorthand.ALLIED_BOARD_FOLLOWER,
        new_form=Set1Units.AlphaWildclaw,
    )
    return Spell(activation_effect=effect)


# Costs 2 less if you have supported an ally this game.
# Give an ally Barrier this round.
def MoralSupport():
    # TODO dynamic modifier activate once
    effect = DynamicCostModifier(
        value=2,
        condition=Condition(
            target=TargetPlayer.ORIGIN_OWNER,
            condition=PlayerFlags.HAS_SUPPORTED_THIS_GAME,
        ),
    )
    effect1 = AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT, keyword=KeywordEnum.BARRIER
    )
    return Spell(activation_effect=effect1, effects=effect)


# Stun 2 enemies.
def StrategicExecution():
    effect = StunEffect(
        target=Input(quantity=2, choices=CardFilter(owner=TargetPlayer.OPPONENT))
    )
    effect1 = CreateCardEffect(
        target=Set1Units.LegionGeneral, location=LocEnum.HOMEBASE
    )
    effect2 = AlternativeActivationEffect(activation_effects=effect1, spell_cost=6)
    return Spell(activation_effect=effect, alternative_effect=effect2)


# Grant an ally +1|+2 and remove all negative KeywordEnum from it.
def MikhaelsBlessing():
    target = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = BuffEffect(target=target, attack=1, health=2)
    effect1 = PurgeKeywordsEffect(target=target, purge_negative=True)
    return Spell(activation_effect=[effect, effect1])


# Grant an ally Elusive and "Nexus Strike: Draw 1."
def ScavengedCamocloaker():
    target = TargetEntity(choices=CardFilter())
    effect = AddKeywordEffect(target=target, keyword=KeywordEnum.ELUSIVE)
    effect1 = DrawEffect(quantity=1)
    ta = TriggeredAction(
        event_filter=EntityEvents.NEXUS_STRIKE,
        action=effect1,
        ally_enum=OriginEnum.SELF,
    )
    effect2 = CreateTriggeredAction(triggered_action=ta, target=target)
    return Spell(activation_effect=[effect, effect2])


# Stop all enemy spells and skills targeting Evelynn and she strikes an enemy.
def LastCaress():
    # TODO
    effect = NegateSpell(
        target=StackSpellFilter(target=BaseCardFilter(card_class=Set6Champions.Evelynn))
    )
    effect1 = StrikeEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT,
        striker=CardFilter(card_class=Set6Champions.Evelynn),
    )
    return Spell(activation_effect=[effect, effect1])


# Deal 4 to a unit.
def SecondBounce():
    effect = DamageEffect(target=TargetShorthand.ANY_BOARD_UNIT, value=4)
    return Spell(activation_effect=effect)


# Grant allied Kai'Sas everywhere another ally's positive KeywordEnum.
def SecondSkin():
    #TODO target exclude
    effect = SecondSkinEffect(target=TargetEntity(choices=CardFilter()))
    return Spell(activation_effect=effect)


# Summon a Vastayan Disciple and draw 1.
def ShimonWind():
    effect = CreateCardEffect(
        target=Set6Units.VastayanDisciple, location=LocEnum.HOMEBASE
    )
    effect1 = DrawEffect()
    return Spell(activation_effect=[effect, effect1])


# Grant an ally Overwhelm and SpellShield.
def Supercharge():
    effect = AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        keyword=[KeywordEnum.SPELLSHIELD, KeywordEnum.OVERWHELM],
    )
    return Spell(activation_effect=effect)


# Deal 1 to a follower. If you've Evolved, deal  3 instead.
def VoidSeeker():
    dyn_value = BranchingValue(
        condition=Condition(
            target=TargetPlayer.ORIGIN_OWNER, condition=PlayerFlags.EVOLVED
        ),
        if_true=3,
        if_false=1,
    )
    effect = DamageEffect(value=dyn_value, target=TargetShorthand.ANY_BOARD_FOLLOWER)
    return Spell(activation_effect=effect)


# Manifest an allied landmark that has been destroyed this game and summon it.
def RiteofPassage():
    choices = EventQuery(
        event=EntityEvents.DESTROY_LANDMARK, param_getter=PostEventParamGetter.TARGET
    )
    # TODO event query, target
    effect = ManifestEffect(target=choices)
    effect1 = CreateCardEffect(target=effect1, location=LocEnum.HOMEBASE)
    return Spell(activation_effect=[effect, effect1])


# Create a Fleeting Heroic Refrain, Yordle Contraption, or Keeper's Verdict in hand.
def BandleTellstones():
    choices = [
        Set5Spells.HeroicRefrain,
        Set5Spells.YordleContraption,
        Set5Spells.KeepersVerdict,
    ]
    effect = CreateCardEffect(is_fleeting=True, target=ChoiceBaseCard(choices=choices))
    return Spell(activation_effect=effect)


# Costs 2 less for each different Ascended ally you've played this game.
# Manifest a card from the Emperor's Deck with cost 9 or less.
def GlorysCall():
    effect = ManifestEffect(
        target=BaseCardFilter(deck=DeckArchetypes.EMPERORS_DECK, cost=(0, 9))
    )
    effect2 = DynamicCostModifier()
    # TODO
    return Spell(activation_effect=effect, effects=effect2)


# Summon two Ghastly Bands.
def StrikeUpTheBand():
    effect = CreateCardEffect(target=Set6Units.GhastlyBand, location=LocEnum.HOMEBASE)
    return Spell(activation_effect=effect)


# Kill an ally to deal 2 to a unit and summon a random Husk.
def HateSpike():
    target_obj = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = KillAction(target=target_obj)
    effect1 = DamageEffect(
        target=TargetShorthand.ANY_BOARD_UNIT,
        target_exclusion=target_obj,
        value=2,
        fizz_if_fail=effect,
    )
    effect2 = SummonHuskEffect()
    return Spell(activation_effect=[effect, effect1, effect2])


# Kill an ally to deal damage equal to its Power to an enemy.
def ThreadtheNeedle():
    target_obj = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = KillAction(target=target_obj)
    effect1 = DamageEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT,
        value=EntityAttribute(target=target_obj, attribute=AttrEnum.ATTACK),
        fizz_if_fail=effect,
    )
    return Spell(activation_effect=[effect, effect1])


# Create copies in hand of 2 allied followers that have died this game.
def FormalInvitation():
    target_obj = EventQueryParamGetter(
        query=EventQuery(event=EntityEvents.DIE),
        parameter=PostEventParameter.TARGET,
        quantity=2,
    )
    # TODO event
    effect = CreateCardEffect(target=target_obj, is_fleeting=True)
    return Spell(activation_effect=effect)


# Plant a Mysterious Portal randomly in the top 4 cards of your deck and plant a Chime on the top card of your deck.
def MagicalJourney():
    effect = PlantMysteriousPortalEffect()
    effect1 = PlantChimes()
    return Spell(activation_effect=[effect, effect1])


# Draw a follower, then activate the effects of all boons in the top 3 cards of your deck.
def TravelersCall():
    effect = DrawEffect(
        filter_obj=TargetEntity(
            automatic=True,
            choices=CardFilter(location=LocEnum.DECK, flags=CardFlags.IS_FOLLOWER),
        )
    )
    effect1 = ActivateBoons(top_x_cards=3)
    return Spell(activation_effect=[effect, effect1])


# Give Jax Barrier this round and Forge him.
def CounterStrike():
    target_obj = TargetEntity(choices=CardFilter(card_class=Set6Champions.Jax))
    effect = AddKeywordEffect(target=target_obj, keyword=KeywordEnum.BARRIER)
    effect1 = ReforgeEffect(target=target_obj)
    return Spell(activation_effect=effect)


# Plant 2 Mysterious Portals randomly in the top 4 cards of your deck. Draw 1.
def Portalpalooza():
    effect = PlantMysteriousPortalEffect(quantity=2, top_x_cards=4)
    effect1 = DrawEffect(quantity=1)
    return Spell(activation_effect=[effect, effect1])


# For each ally, plant a Mysterious Portal and 3 Chimes in the top 10 cards of your deck and plant a Flashbomb Trap and 3 Poison Puffcaps on random cards in the enemy deck.
def EclecticCollection():
    # TODO multiplier
    effect = PlantMysteriousPortalEffect(top_x_cards=10, quantity=1)
    effect1 = PlantChimes(
        top_x_cards=10,
        quantity=3,
    )
    effect2 = PlantFlashBombTrap(quantity=1, entire_deck=True)
    effect3 = PlantPuffcaps(
        quantity=3,
        entire_deck=True,
    )
    return Spell(activation_effect=[effect, effect1, effect2, effect3])


# Revive an Ephemeral copy ofthe strongest dead allied follower and give enemies -1|-0 this round.
def HarrowingReturn():
    pool = EventQueryParamGetter(query=EventQuery(event=EntityEvents.DIE))
    target_obj = TargetEntity(
        automatic=True,
        entity_pool=pool,
        choices=CardFilter(
            location=None,
            flags=CardFlags.IS_FOLLOWER,
            sort_by=CardSorter.STRONGEST,
        ),
    )
    # TODO selector
    effect = ReviveEffect(target=target_obj, is_ephemeral=True)
    effect1 = BuffEffect(
        target=CardFilter(owner=TargetPlayer.OPPONENT), attack=-1, round_only=True
    )
    return Spell(activation_effect=[effect, effect1])


# Spawn 2, then your strongest Tentacle and an enemy strike each other.
def TentacleSmash():
    effect = SpawnEffect(quantity=2)
    effect1 = MutualStrikeEffect(
        first_striker=TargetShorthand.OPPONENT_BOARD_UNIT,
        second_striker=CardFilter(
            card_class=Set6Units.Tentacle, sort_by=CardSorter.STRONGEST
        ),
    )
    return Spell(activation_effect=[effect, effect1])


# Give an ally with an attachment the stats and keywords of its attachment this round
# and move the attachment to another ally.
def Sharesies():
    target_obj = TargetEntity(choices=TargetShorthand.EQUIPPED_ALLIED_UNIT)
    effect = BuffEffect(
        target=target_obj, attack=..., health=..., keyword=..., round_only=True
    )
    effect1 = TransferEquipmentEffect(
        source=target_obj, destination=TargetEntity(exclusion=target_obj)
    )
    # TODO
    return Spell(activation_effect=[effect, effect1])


# To play, discard 1. Draw 2 and if you discarded an equipment, summon a Icathian Mirage.
def PartsMadeWhole():
    # TODO
    effect1 = DiscardEffect(target=TargetShorthand.ALLIED_HAND_CARD)
    effect2 = DrawEffect(quantity=2)
    effect3 = SummonEffect(
        target=Set6Units.IcathianMirage,
        condition=Condition(
            target=PostEventParamGetter(
                effect=effect1, parameter=PostEventParameter.TARGET
            ),
            condition=CardFlags.IS_EQUIPMENT,
        ),
    )
    return Spell(activation_effect=[effect2, effect3], play_requisite=effect1)


# Destroy a unit's equipment and deal 2 to it.
def HeavyMetal():
    target = TargetEntity(choices=TargetShorthand.ANY_BOARD_UNIT)
    effect = DestroyEquipEffect(target=target)
    effect1 = DamageEffect(target=target, value=2)
    return Spell(activation_effect=[effect, effect1])


# Deal 2 to an enemy and Stun another. Plant 6 Chimes on random cards in your deck.
def CosmicBinding():
    target_obj = TargetEntity(choices=TargetShorthand.OPPONENT_BOARD_UNIT)
    effect = DamageEffect(target=target_obj, value=2)
    effect1 = StunEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT, target_exclusion=target_obj
    )
    effect2 = PlantChimes(quantity=6)
    return Spell(activation_effect=[effect, effect1, effect2])


# Deal 2 to a unit. Draw 1 at the next Round Start for each damage dealt and give them Fleeting.
def LoadedVessel():
    # TODO
    effect1 = DamageEffect(target=TargetShorthand.ANY_BOARD_UNIT, value=2)
    effect2 = DrawEffect(
        quantity=PostEventParam.VALUE,
        is_fleeting=True,
        coevent=effect1
    )
    effect3 = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START, activate_once=True, action=effect2
    )
    return Spell(activation_effect=(effect1, effect3))


# Give an ally +1|+1 this round.
def Catch():
    target = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect1 = BuffEffect(target=target, attack=1, health=1, round_only=True)
    equip_target = TargetEntity(
        choices=CardFilter(type=Types_.EQUIPMENT, cost=(0, 2), location=LocEnum.HAND)
    )
    effect2 = EquipEffect(equipment=equip_target, target=target)
    effect = ChoiceAction(choices=[effect1, effect2])
    return Spell(activation_effect=effect)


# Spawn 4.
def AnsweredPrayer():
    effect1 = SpawnEffect(quantity=4)
    effect2 = SpawnEffect(quantity=2)
    effect3 = AlternativeActivationEffect(activation_effects=effect1, spell_cost=5)
    return Spell(activation_effect=effect2, alternative_effect=effect3)


# Deal 1 to a unit. If one of your traps or boons activated this round, deal 3 to it instead.
def ProximityPuffcap():
    effect = ProximityPuffcapEffect(target=TargetShorthand.ANY_BOARD_UNIT)
    return Spell(activation_effect=effect)


# Destroy a unit's equipment, and if it's a follower, Silence it.
def SilenceandSuppress():
    target_obj = TargetEntity(owner=TargetShorthand.ANY_BOARD_UNIT)
    effect = DestroyEquipEffect(target=target_obj)
    effect1 = SilenceEffect(
        target=target_obj,
        condition=Condition(target=target_obj, condition=CardFlags.IS_FOLLOWER),
    )
    return Spell(activation_effect=[effect, effect1])


# Give Kayn Quick Attack this round. He starts a free attack challenging an enemy.
def Shadowstep():
    target_obj = TargetEntity(
        choices=TargetEntity(choices=CardFilter(card_class=Set6Champions.Kayn))
    )
    effect = AddKeywordEffect(target=target_obj, keyword=KeywordEnum.QUICKSTRIKE)
    effect1 = FreeAttackEffect(target=effect)
    effect2 = ChallengeEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT, challenger=target_obj
    )
    return Spell(activation_effect=[effect, effect1, effect2])


# Pick a follower or equipment from the top 4 cards of your deck. Draw it, place the rest into your deck.
def TemptingProspect():
    effect = DrawSpecificReturnRestEffect(
        top_x_cards=4,
        filter_obj=DrawCardFilter(type=[Types_.UNIT, Types_.EQUIPMENT]),
    )
    return Spell(activation_effect=effect)


# Forge an ally.
def TimeandDedication():
    effect = ForgeEffect(target=TargetShorthand.ALLIED_BOARD_UNIT)
    return Spell(activation_effect=effect)


# Create a Fleeting Mark of the Isles, Spirit Journey, or Crumble in hand.
def ShadowIslesTellstones():
    choices_obj = [
        Set1Spells.MarkoftheIsles,
        Set4Spells.SpiritJourney,
        Set3Spells.Crumble,
    ]
    effect = TellstonesEffect(target=ChoiceBaseCard(choices=choices_obj))
    return Spell(activation_effect=effect)


# Create a Fleeting Prismatic Barrier, Detain, or For Demacia! in hand.
def DemacianTellstones():
    choices_obj = [
        Set1Spells.ForDemacia,
        Set1Spells.PrismaticBarrier,
        Set1Spells.Detain,
    ]
    effect = TellstonesEffect(target=ChoiceBaseCard(choices=choices_obj))
    return Spell(activation_effect=effect)


# Create a Fleeting Health Potion, Homecoming, or Stand United in hand.
def IonianTellstones():
    choices_obj = [
        Set1Spells.StandUnited,
        Set3Spells.Homecoming,
        Set1Spells.HealthPotion,
    ]
    effect = TellstonesEffect(target=ChoiceBaseCard(choices=choices_obj))
    return Spell(activation_effect=effect)


# Create a Fleeting Wish, Paddle Star, or Blessing of Targon in hand.
def TargonianTellstones():
    choices_obj = [
        Set3Spells.Wish,
        Set3Spells.PaddleStar,
        Set3Spells.BlessingofTargon,
    ]
    effect = TellstonesEffect(target=ChoiceBaseCard(choices=choices_obj))
    return Spell(activation_effect=effect)


# Create a Fleeting Sharpened Resolve, Whirling Death, or Weapons of the Lost in hand.
def NoxianTellstones():
    choices_obj = [
        Set3Spells.SharpenedResolve,
        Set1Spells.WhirlingDeath,
        Set5Spells.WeaponsoftheLost,
    ]
    effect = TellstonesEffect(target=ChoiceBaseCard(choices=choices_obj))
    return Spell(activation_effect=effect)


# Deal 5 to a unit. If it would die, Obliterate it instead.
def Hexbliterator():
    target_obj = TargetEntity(choices=TargetShorthand.ANY_BOARD_UNIT)
    effect = DamageEffect(value=5, target=target_obj)
    effect1 = ObliterateEffect(target=target_obj, condition=Condition())
    # TODO


# Create a Fleeting Aftershock, Hextech Transmogulator, or Progress Day! in hand.
def PiltovanTellstones():
    choices_obj = [
        Set1Spells.ProgressDay,
        Set1Spells.HextechTransmogulator,
        Set3Spells.Aftershock,
    ]
    effect = TellstonesEffect(target=ChoiceBaseCard(choices=choices_obj))
    return Spell(activation_effect=effect)


# Deal 1 to anything, then Rally.
def BloodintheWater():
    effect = DamageEffect(target=TargetShorthand.ANYTHING)
    effect1 = RallyEffect()
    return Spell(activation_effect=[effect, effect1])


# Create a Fleeting Ruthless Predator, Weight of Judgment, or Spirit Fire in hand.
def ShurimanTellstones():
    choices_obj = [
        Set4Spells.RuthlessPredator,
        Set4Spells.WeightofJudgment,
        Set4Spells.SpiritFire,
    ]
    effect = TellstonesEffect(target=ChoiceBaseCard(choices=choices_obj))
    return Spell(activation_effect=effect)


# Forge an ally and deal 1 to all units, then do it again.
def BellowsBreath():
    effect = ForgeEffect(target=TargetShorthand.ALLIED_BOARD_UNIT)
    effect1 = DamageEffect(target=CardFilter(owner=None), value=1)
    effect2 = RecastEventOfAction(target=[effect, effect1], multiplier=2)
    return Spell(activation_effect=effect)


# Heal your Nexus 4 and grant all allies and equipment in your deck +1|+1. Draw 1 of them.
def GiftoftheHearthblood():
    effect = HealEffect(target=TargetPlayer.ORIGIN_OWNER, value=4)
    filter_obj = CardFilter(
        type=[Types_.UNIT, Types_.EQUIPMENT],
        location=LocEnum.DECK,
    )
    effect1 = BuffEffect(target=filter_obj, attack=1, health=1)
    effect2 = DrawEffect(quantity=1, filter_obj=filter_obj)
    return Spell(activation_effect=[effect, effect1, effect2])


# Reduce the cost of a spell in your hand by 1.
def Preparation():
    filter_obj = CardFilter(type=Types_.SPELL, location=LocEnum.HAND)
    effect = BuffCostEffect(target=TargetEntity(choices=filter_obj), value=1)
    return Spell(activation_effect=effect)


# Give an ally +2|+0 this round.Create a Meditate in hand.
def WujuStyle():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT, attack=2, round_only=True
    )
    effect1 = CreateCardEffect(target=Meditate)
    return Spell(activation_effect=[effect, effect1])


# Spawn 2.Draw 2.
def EyeofNagakabouros():
    effect = SpawnEffect(quantity=2)
    effect1 = DrawEffect(quantity=2)
    return Spell(activation_effect=[effect, effect1])


# Give an ally +0|+2 this round.
def Meditate():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT, health=2, round_only=True
    )
    return Spell(activation_effect=effect)


# Give an ally Challenger this round. If it's Equipped, draw 1.
def EntrancingLure():
    target_obj = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = AddKeywordEffect(
        target=target_obj,
        keyword=KeywordEnum.CHALLENGER,
        round_only=True,
    )
    effect1 = DrawEffect(
        condition=Condition(target=target_obj, condition=CardFlags.IS_EQUIPPED)
    )
    return Spell(activation_effect=[effect, effect1])


# Start a free attack with 2 Dragonlings.
def DragonAmbush():
    effect = CreateCardEffect(
        target=Set2Units.Dragonling, location=LocEnum.HOMEBASE, quantity=2
    )
    effect1 = FreeAttackEffect(target=PostEventParam.CREATED_CARD, coevent=effect)
    return Spell(activation_effect=(effect, effect1))


# Give an ally +1|+0 this round.
def MomentousChoice():
    condition = Condition(
        target=TargetPlayer.ORIGIN_OWNER,
        condition=PlayerFlags.HAS_EQUIPPED_ALLY_THIS_GAME,
    )
    effect = BuffEffect(target=CardFilter(), attack=1, round_only=True)
    effect1 = BuffEffect(target=CardFilter(), health=1, round_only=True)
    choice_action = ChoiceAction(choices=[effect, effect1])
    meffect1 = RecastEventOfAction(target=effect, condition=condition)
    return Spell(activation_effect=[choice_action])

    # TODO


# Obliterate a unit or landmark.
def CelestialImpact():
    effect = ObliterateEffect(target=TargetShorthand.ANY_BOARD_UNIT_OR_LANDMARK)
    return Spell(activation_effect=effect)


# Manifest a non-champion card from the opponent's hand. Plunder: I cost 1 less.
def Swindle():
    effect = ManifestEffect(
        target=CardFilter(
            location=LocEnum.HAND,
            excluding_flags=CardFlags.IS_CHAMPION,
            type=None,
            owner=TargetPlayer.OPPONENT,
        )
    )
    effect1 = DynamicCostModifier(value=1, condition=PlayerFlags.PLUNDER)
    return Spell(activation_effect=effect, effects=effect1)


# Invoke a low, medium, and high cost Celestial card.
def CelestialTrifecta():
    effect = InvokeEffect(target=InvokeBaseCardFilter(cost=(0, 3)))
    effect1 = InvokeEffect(target=InvokeBaseCardFilter(cost=(4, 6)))
    effect2 = InvokeEffect(target=InvokeBaseCardFilter(cost=(9, 0)))
    return Spell(activation_effect=[effect, effect1, effect2])


# Obliterate an ally and create a Corrupted Form with its stats.
def SealInSteel():
    target_obj = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = ObliterateEffect(target=target_obj)
    effect1 = CreateCardEffect(
        target=Set6Equipments.CorruptedForm,
        with_my_stats_source=target_obj,
        fizz_if_fail=effect,
    )
    return Spell(activation_effect=[effect, effect1])


# An Equipped ally strikes an enemy.
def FuriousWielder():
    target_obj1 = TargetEntity(choices=CardFilter(flags=CardFlags.IS_EQUIPPED))
    target_obj2 = TargetEntity(choices=CardFilter(owner=TargetPlayer.OPPONENT))
    effect = StrikeEffect(target_obj2, target_obj1)
    return Spell(activation_effect=effect)


# Give an ally "Last Breath: Summon a Icathian Mirage with my equipment" this round.
def BladesoftheFallen():
    effect = CreateCardEffect(
        target=Set6Units.IcathianMirage,
        attachment=PostEventParam.TARGET,
    )
    ta = TriggeredAction(
        event_filter=EntityEvents.LASTBREATH,
        action=effect,
        ally_enum=OriginEnum.T_SELF,
        round_only=True,
    )
    create_ta = CreateTriggeredAction(
        triggered_action=ta,
        target=TargetShorthand.ALLIED_BOARD_UNIT,
    )
    return Spell(activation_effect=create_ta)


# Grant allies +1|+1.
def InspiringLight():
    effect = BuffEffect(target=CardFilter(), attack=1, health=1)
    return Spell(activation_effect=effect)


# Once you have equipped an ally this game, I cost 2 less. Revive the Strongest dead allied champion.
def HeedlessResurrection():
    # TODO watcher
    cost = DynamicCostModifier(
        value=2,
        condition=Condition(
            target=TargetPlayer.ORIGIN_OWNER,
            condition=PlayerFlags.HAS_EQUIPPED_ALLY_THIS_GAME,
        ),
    )
    target_obj = TargetEntity(
        choices=CardFilter(
            flags=CardFlags.IS_CHAMPION,
            sort_by=CardSorter.STRONGEST,
            location=LocEnum.GRAVEYARD,
        ),
        automatic=True,
    )
    effect = ReviveEffect(target=target_obj)
    return Spell(activation_effect=effect, effects=cost)


# Give an ally "Last Breath: Summon a Icathian Mirage with my equipment" this round.
def BladesoftheFallen():
    effect = SummonEffect(
        target=...,
    )
    effect1 = TriggeredAction(
        event_filter=EntityEvents.LASTBREATH,
        ally_enum=OriginEnum.T_SELF,
        action=effect,
    )
    effect2 = CreateTriggeredAction(
        triggered_action=effect1,
        target=TargetShorthand.ALLIED_BOARD_UNIT,
    )
    return Spell(activation_effect=(effect2))


# Deal 1 to a unit. Create a Second Bounce in hand at the next Round Start.
def DancingGrenade():
    effect = DamageEffect(value=1, target=TargetShorthand.ANY_BOARD_UNIT)
    effect1 = CreateCardEffect(
        target=SecondBounce,
    )
    ta = TriggeredAction(event_filter=GameStateEnums.ROUND_START, action=effect1)
    effect2 = CreateTriggeredAction(triggered_action=ta)
    return Spell(activation_effect=(effect, effect2))


# Kill a unit with 2 or less power.
def Quietus():
    effect = KillAction(
        target=TargetEntity(choices=CardFilter(owner=None, attack=(0, 2)))
    )
    effect1 = DestroyEquipEffect(
        target=TargetEntity(choices=CardFilter(owner=None, flags=CardFlags.IS_EQUIPPED))
    )
    effect2 = ChoiceAction(choices=[effect, effect1])
    return Spell(activation_effect=effect2)


# Kill all units except allied Darkin and allied Equipped units.
def UtterDevastation():
    target = CardFilter(owner=None)
    exception_obj = CardFilter(subtype=SubTypes_.DARKIN)
    exception_obj1 = CardFilter(flags=CardFlags.IS_EQUIPPED)
    effect = KillAction(target=target, target_exclusion=[exception_obj, exception_obj1])
    return Spell(activation_effect=effect)


# Recall a unit with 3 or less Health.
def GruesomeTheater():
    effect = RecallEffect(
        target=TargetEntity(choices=CardFilter(owner=None, health=(0, 3)))
    )
    return Spell(activation_effect=effect)


# Give enemies -2|-0 this round. Create a Fleeting Instant Century in hand.
def SandsofTime():
    effect = BuffEffect(
        target=CardFilter(owner=TargetPlayer.OPPONENT), attack=-2, round_only=True
    )
    effect1 = CreateCardEffect(target=Set4Spells.InstantCentury, is_fleeting=True)
    return Spell(activation_effect=[effect, effect1])


# Deal 3 to ALL units.Enlightened: Heal your Nexus 3.
def WingsoftheCryophoenix():
    effect = DamageEffect(value=3, target=CardFilter(owner=None))
    effect1 = HealEffect(value=3, condition=PlayerFlags.ENLIGHTENED)
    return Spell(activation_effect=[effect, effect1])


# Toss 3.Drain 2 from a unit.
def Undergrowth():
    effect = TossEffect(quantity=3)
    effect1 = DrainEffect(target=TargetShorthand.ANY_BOARD_UNIT, value=2)
    return Spell(activation_effect=[effect, effect1])


# Fully heal an ally, then grow its Power equal to its Health.
def ConsulttheHeavens():
    target_obj = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = HealEffect(value=Ops_.MAX, target=target_obj)
    value = EntityAttribute(target=target_obj, attribute=AttrEnum.HEALTH)
    effect1 = BuffEffect(target=target_obj, attack=value, operator=Ops_.GROW)
    return Spell(activation_effect=[effect, effect1])


# Pick one of two new 2 cost spells to create in hand and set its cost to 0 this round. Repeat two more times.
def SputteringSongspinner():
    target = ChoiceBaseCard(
        choices=BaseCardFilter(quantity=2, type=Types_.SPELL, cost=(0, 2), is_new=True)
    )
    effect1 = CreateCardEffect(target=target)
    effect2 = BuffCostEffect(value=0, operator=Ops_.SET, round_only=True, target=...)
    effect3 = CombinationAction(actions=[effect1, effect2])
    effect4 = MultipleActivationsEffect(target=effect3, multiplier=3)
    return Spell(activation_effect=effect4)


# Destroy an enemy's equipment. An ally and that enemy strike each other.
def BrutalSkirmish():
    target = TargetEntity(choices=TargetShorthand.OPPONENT_BOARD_UNIT)
    effect1 = DestroyEquipEffect(target=target)
    effect2 = MutualStrikeEffect(
        first_striker=TargetShorthand.ALLIED_BOARD_UNIT, second_striker=target
    )
    return Spell(activation_effect=[effect1, effect2])


# If you've attacked 2+ times this round, I cost 5 less.An ally strikes an enemy.
def Condemn():
    effect1 = DynamicCostModifier(value=5, condition=...)
    effect = StrikeEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT,
        striker=TargetShorthand.ALLIED_BOARD_UNIT,
    )
    return Spell(activation_effect=effect, effects=effect1)


# Give an ally +2|+0 and Quick Attack this round.Flow: Create a new 2 cost spell in hand.
def CrowdPleaser():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        attack=2,
        keyword=KeywordEnum.QUICKSTRIKE,
        round_only=True,
    )
    effect1 = CreateCardEffect(
        target=BaseCardFilter(type=Types_.SPELL, cost=2), condition=PlayerFlags.FLOW
    )
    return Spell(activation_effect=[effect, effect1])


# Predict.
# Give a unit "I take double damage and if I would die, Obliterate me instead" this round.
def CurseoftheTomb():
    effect = PredictEffect()
    effect2 = ObliterateEffect(target=AutoEntitySelector.SELF)
    effect1 = ActionReplacement(event_filter=EntityEvents.DAMAGE)
    modifier = ActionModifier(
        event_filter=EntityEvents.DAMAGE,
        parameter=...,
        operator=Ops_.MULTIPLY,
        value=2,
        round_only=True,
        ally_enum=OriginEnum.T_SELF,
    )
    replacement = ActionReplacement(
        event_filter=EntityEvents.DIE,
        ally_enum=OriginEnum.T_SELF,
        replacement_action=effect2,
    )
    effect3 = CreateTriggeredAction(
        triggered_action=(modifier, replacement),
        target=TargetShorthand.ANY_BOARD_UNIT,
    )
    return Spell(activation_effect=(effect, effect3))


# Draw 2.
# Flow: Reduce those cards' costs by 2.
def DrumSolo():
    effect1 = BuffCostEffect(
        target=PostEventParam.TARGET,
        value=2,
        condition=PlayerFlags.FLOW,
    )
    effect = DrawEffect(quantity=2, coevent=effect1)
    return Spell(activation_effect=(effect, effect1))


# An Equipped ally strikes an enemy, then is unequipped.
def FishFight():
    target = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    effect = StrikeEffect(target=TargetShorthand.ALLIED_BOARD_UNIT)
    effect1 = UnequipEffect(target=target)
    combined = CombinationAction(actions=[effect, effect1])
    effect2 = MutualStrikeEffect(
        first_striker=target,
        second_striker=TargetShorthand.OPPONENT_BOARD_UNIT,
    )
    action = ChoiceAction(choices=[combined, effect2])
    return Spell(activation_effect=action)


# Destroy a unit's equipment.
def Fracture():
    effect = DamageEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT, value=1)
    effect1 = DestroyEquipEffect(target=TargetShorthand.EQUIPPED_OPPONENT_UNIT)
    action = ChoiceAction(choices=[effect, effect1])
    return Spell(activation_effect=action)


# Deal 2 to a unit. If you've played 6+ other new spells this game, deal 1 to another unit.
def HighNote():
    effect = DamageEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT, value=2)
    effect = DamageEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT, value=1, target_exclusion=...
    )


# Create a Golden Spatula in hand.
def IcathianMyths():
    effect = CreateCardEffect(cost=0)
    effect1 = CreateCardEffect(...)


# Grow an ally to 5 Power this round.
def LegionaryCharge():
    effect1 = DrawEffect(quantity=1, filter_obj=BaseCardFilter(attack=(5, 0)))
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT, attack=5, round_only=True
    )


# Give an enemy Vulnerable this round. If it dies this round, deal 1 to the enemy Nexus.
def TestofSpirit():
    effect = AddKeywordEffect(
        target=TargetShorthand.OPPONENT_BOARD_UNIT,
        keyword=KeywordEnum.SPELLSHIELD,
        round_only=True,
    )
    effect1 = DamageEffect(
        target=TargetPlayer.OPPONENT, value=1, triggering_effect=effect2
    )
    effect2 = TriggeredAction(event_filter=EntityEvents.DIE, action=effect1)
    return Spell(activation_effect=[effect, effect1])


# Once you have Equipped an ally this game, I cost 2 less.Give an ally SpellShield this round.
def TheExpansesProtection():
    effect = AddKeywordEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT,
        keyword=KeywordEnum.SPELLSHIELD,
        round_only=True,
    )
    effect4 = DynamicCostModifier(
        value=2, condition=PlayerFlags.HAS_EQUIPPED_ALLY_THIS_GAME
    )
    return Spell(activation_effect=[effect], effects=effect4)


# Once you have Equipped an ally this game, I cost 2 less. Grow an ally to 5|5 this round.
def TheSuddenSurge():
    effect = BuffEffect(
        target=TargetShorthand.ALLIED_BOARD_UNIT, attack=5, health=5, round_only=True
    )
    effect4 = DynamicCostModifier(
        value=2, condition=PlayerFlags.HAS_EQUIPPED_ALLY_THIS_GAME
    )
    return Spell(activation_effect=effect, effects=effect4)


# Once you have Equipped an ally this game, I cost 2 less.Draw 2 and give them Fleeting.
def TheUnendingWave():
    effect = DrawEffect(quantity=2, is_fleeting=True)
    effect4 = DynamicCostModifier(
        value=5, condition=PlayerFlags.HAS_EQUIPPED_ALLY_THIS_GAME
    )
    return Spell(activation_effect=effect, effects=effect4)


# Frostbite the strongest enemy. If you have Equipped an ally this game, copy me.
def TheUnforgivingCold():
    effect = FrostbiteEffect(target=AutoEntitySelector.STRONGEST_OPPONENT_BOARD_UNIT)
    effect1 = CopySpellWithSameTargets(
        target=AutoEntitySelector.SELF,
        condition=PlayerFlags.HAS_EQUIPPED_ALLY_THIS_GAME,
    )
    return Spell(activation_effect=[effect, effect1])


# Deal 1 to a unit. If you have Equipped an ally this game, copy me with the same targets.
def TheViolentDischord():
    effect = DamageEffect(target=TargetShorthand.OPPONENT_BOARD_UNIT, value=1)
    effect1 = CopySpellWithSameTargets(
        target=TargetShorthand.SELF, condition=PlayerFlags.HAS_EQUIPPED_ALLY_THIS_GAME
    )
    return Spell(activation_effect=[effect, effect1])


# Equip an ally with an equipment in hand that costs 2 or less. It starts a free attack.
def Tumble():
    target = TargetEntity(choices=TargetShorthand.ALLIED_BOARD_UNIT)
    equip_target = TargetEntity(
        choices=CardFilter(type=Types_.EQUIPMENT, cost=(0, 2), location=LocEnum.HAND)
    )
    effect2 = EquipEffect(equipment=equip_target, target=target)
    effect3 = FreeAttackEffect(target=target)
    return Spell(activation_effect=[target, equip_target, effect2, effect3])


# Flow: I cost 2 less.Recall a unit or landmark. If it has any attachments, destroy them first.
def UnworthySoul():
    target = TargetEntity(choices=TargetShorthand.OPPONENT_LANDMARK_OR_BOARD_UNIT)
    effect2 = DestroyAttachmentsEffect(target=target)
    effect3 = RecallEffect(target=target)
    effect4 = DynamicCostModifier(value=5, condition=PlayerFlags.FLOW)
    return Spell(activation_effect=[target, effect2, effect3], effects=effect4)
