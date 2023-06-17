from random import choice
import Sets.SET1.Units as Set1Units
import Sets.SET1.Spells as Set1Spells
import Sets.SET2.Spells as Set2Spells
import Sets.SET2.Units as Set2Units
import Sets.SET3.Units as Set3Units
import Sets.SET3.Spells as Set3Spells
import Sets.SET3.Skills as Set3Skills

import Sets.SET4.Spells as Set4Spells
import Sets.SET4.Units as Set4Units
import Sets.SET5.Units as Set5Units
import Sets.SET4.Landmarks as Set4Landmarks
import Sets.SET5.Landmarks as Set5Landmarks
import Sets.SET5.Champions as Set5Champions
import Sets.SET5.Spells as Set5Spells

import Sets.SET6.Units as Set6Units
import Sets.SET6.Champions as Set6Champions

import Sets.SET6.Equipments as Set6Equipments
from actions.action_modifiers.silence import SilenceEffect
from actions.activations.copy_spell import CopySpellWithSameTargets
from actions.activations.countdown import CountdownEffect
from actions.activations.multiple_activations import MultipleActivationsEffect
from actions.activations.negate_spell import NegateSpell
from actions.activations.play_skill import PlaySkill
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
from actions.beacons.restore_sun import RestoreSundisc
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
from actions.keywords.copy_keywords import CopyKeywords
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
from actions.reactions.value_triggered_action import (
    EventCounterEnum,
    ValueTriggeredAction,
)
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
from actions.win.win_con import DeclareGameResult
from card_classes.champion import Champion
from card_classes.landmark import Landmark
from card_classes.spell import Spell
from card_classes.unit import Unit
from conditions.base_condition import Condition
from entity_selectors.base_card_filter import (
    BaseCardFilter,
    InvokeBaseCardFilter,
    ManifestBaseCardFilter,
)
from entity_selectors.card_filter import (
    BeholdingFilter,
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
from value.card_counter import CardCounter
from value.entity_attribute import EntityAttribute


class ScrappyBomb(Landmark):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.listener.aftereffect(EntityEvents.DIE, self.card_effect)
        self.listener.aftereffect(EntityEvents.DIE, self.card_effect)
        # TODO COUNTDOWN

    async def card_effect(self):
        await damage(self.opponent, 1)


class RisenAltar(Landmark):
    def __init__(self, **kwargs) -> None:
        super().__init__("", countdown=3)
        self.listener.aftereffect(EntityEvents.DESTROY_LANDMARK, self.card_effect)

    def countdown(self):
        create_card("", LocationsEnum.HOMEBASE)

    def card_effect(self):
        create_card("", LocationsEnum.HOMEBASE)


class TheBandleTree(Landmark):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.listener.aftereffect(
            GameStateEnums.ROUND_START, self.card_effect
        )
        self.listener.aftereffect(
            EntityEvents.SUMMON, self.card_effect2
        )
        # TODO

    def card_effect2(self, entity: Unit):
        if entity.regions == ...:
            pass
        ....add(entity.regions)
        if len(...) >= 10:
            self.listener.omni.signal("wincon")

    def card_effect(self):
        regions = 1
        chosen = choice(self.entity_manager.regions().difference())
        chosen = self.json_manager.invoke(region=regions)
        self.entity_manager.create_card(self, self.owner, chosen, "hand")


class Sarcophagus(Landmark):

    ...


class CatalogueofRegrets(Landmark):

    _spells_last_round: List[CardCode] = []

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.listener.aftereffect(GameStateEnums.ROUND_START, self.card_effect)
        # CONTAINER FOR SPELLS
        # TODO

    async def card_effect(self):
        self.entity_manager.create_card(self, self.owner, "", LocationsEnum.HOMEBASE)


class TheForgeOfTomorrow(Landmark):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.listener.aftereffect(
            EntityEvents.ACTIVATE_SPELL,
            self.card_effect,
            activate_once=True,
            condition_aftereffect=lambda x: x.cost>=6,
        )

    def summon(self):
        create_card("", LocationsEnum.HOMEBASE)

    def card_effect(self):
        create_card("", LocationsEnum.HOMEBASE)
        set_attribute(self.owner, Attr_.SPELL_MANA, operator=Ops_.MAX)


class GodWillowSeedling(Landmark):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.listener.aftereffect(
            GameStateEnums.ROUND_START, self.card_effect
        )
        self.listener.aftereffect(
            EntityEvents.SUMMON, self.card_effect2
        )

    def play(self):
        target = self.acquire_target(self.owner.boardunits())
        create_card(
            "",
            LocationsEnum.HOMEBASE,
            function=lambda x: add_keyword(x, Keywords.EPHEMERAL),
        )

    def countdown(self):
        create_card(
            "",
            LocationsEnum.HOMEBASE,
            function=lambda x: add_keyword(x, Keywords.EPHEMERAL),
        )


class ObeliskofPower(Landmark):
    def __init__(self, **kwargs) -> None:
        super().__init__("", countdown=3)
        self.listener.aftereffect(EntityEvents.SUMMON, self.countdown)
        self.listener.aftereffect(EntityEvents.DESTROY_LANDMARK, self.countdown)

    def countdown(self):
        buff_attack_health(filter_strongest(self.opponent.boardunits()), 2, 0)


class HexplosiveMinefield(Landmark):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listener.aftereffect(EntityEvents.DESTROY_LANDMARK, self.card_effect)
        self.listener.aftereffect(EntityEvents.SUMMON, self.card_effect)

    def card_effect(self):
        stun(filter_strongest(self.opponent.boardunits()))