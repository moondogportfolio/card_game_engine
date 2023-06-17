from actions.activations.multiple_activations import MultipleActivationsEffect
from actions.activations.play_skill import PlaySkill
from actions.activations.recast_spell import RecastEventOfAction
from actions.attachments.autoequip import AutoEquipEffect
from actions.attachments.equip import EquipEffect
from actions.attachments.forge import ForgeEffect
from actions.attribute.buff import BuffCostEffect, BuffEffect
from actions.attribute.buff_everywhere import BuffEverywhereEffect
from actions.attribute.damage import DamageEffect
from actions.attribute.heal import HealEffect
from actions.attribute.rally import RallyEffect
from actions.branching.branching_action import BranchingAction
from actions.champ.level_up import LevelupEffect
from actions.common.strike import StrikeEffect
from actions.create.create_card import CreateCardEffect
from actions.create.summon_specific_cards import SpawnEffect, SummonHuskEffect
from actions.keywords.add_keyword import AddKeywordEffect, AddRandomKeywordEffect
from actions.keywords.copy_keywords import CopyKeywords
from actions.movement.move import MoveEffect
from actions.movement.recall import RecallEffect
from actions.movement.swap import SwapPositionsEffect
from actions.reactions.action_modifier import ActionModifier
from actions.reactions.dynamic_attr_modifier import DynamicAttackModifier
from actions.reactions.triggered_action import TriggeredAction
from actions.reactions.value_triggered_action import (
    EventCounterEnum,
    ValueTriggeredAction,
)
from actions.transform.transform import TransformEffect
from actions.traps.set_trap import (
    PlantChimes,
    PlantFlashBombTrap,
    PlantMysteriousPortalEffect,
)
from card_classes.champion import Champion
from card_classes.unit import Unit
from conditions.base_condition import Condition
from entity_selectors.base_card_filter import BaseCardFilter
from entity_selectors.card_filter import CardFilter
from entity_selectors.input import ChoiceBaseCard, ChoiceValue
from enums.attribute import AttrEnum
from enums.card_sorters import CardSorter
from enums.entity_events import EntityEvents
from enums.gamestate import GameStateEnums
from enums.keywords import KeywordEnum
from enums.location import LocEnum
from enums.operator import Ops_
from enums.origin_enum import OriginEnum
from enums.post_event_param import PostEventParam
from enums.types import Types_
from resolvable_enums.auto_card_selector import AutoEntitySelector
import Sets.SET5.Spells as Set5Spells
import Sets.SET6.Units as SET6Units
import Sets.SET5.Skills as Set5Skills
import Sets.SET6.Equipments as SET6Equipments
from resolvable_enums.card_conditions import CardFlags
from resolvable_enums.player_conditions import PlayerFlags
from resolvable_enums.target_player import TargetPlayer
from value.entity_attribute import EntityAttribute


# Last Breath: Summon Sion Returned.
# When I'm discarded, grant your strongest ally Overwhelm and place me into your deck.
def Sion():
    effect = AddKeywordEffect(
        target=AutoEntitySelector.STRONGEST_BOARD_UNIT, keyword=KeywordEnum.OVERWHELM
    )
    effect1 = MoveEffect(target=AutoEntitySelector.SELF, destination=LocEnum.DECK)
    trigger2 = TriggeredAction(
        event_filter=EntityEvents.DISCARD,
        action=[effect, effect1],
        ally_enum=OriginEnum.T_SELF,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Sion2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.DAMAGE,
        threshold=35,
        action_on_value=levelup,
        ally_enum=OriginEnum.O_ALLY,
        condition=...,
        instance_bound=False,
        event_counter=EventCounterEnum.COUNT_VALUE,
    )
    buff = DynamicAttackModifier(max_value=7, value=...)
    return Champion(effects=[trigger2, watcher, buff])


def Sion2():
    effect = AddKeywordEffect(
        target=AutoEntitySelector.STRONGEST_BOARD_UNIT, keyword=KeywordEnum.OVERWHELM
    )
    effect1 = MoveEffect(target=AutoEntitySelector.SELF, destination=LocEnum.DECK)
    trigger2 = TriggeredAction(
        event_filter=EntityEvents.DISCARD,
        action=[effect, effect1],
        ally_enum=OriginEnum.T_SELF,
    )
    create = CreateCardEffect(target=SionReturned, location=LocEnum.HOMEBASE)
    return Champion(effects=trigger2, last_breath_effect=create)


# When I'm summoned, Rally.
def SionReturned():
    return Unit(summon_effect=RallyEffect())


def Galio():
    effect = BuffEffect(exclude_origin=True, target=CardFilter(), health=3)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Galio2)
    condition = Condition(
        target=CardFilter(), condition=CardFlags.HEALTH_REACHES_AMOUNT, parameter=25
    )
    trigger2 = TriggeredAction(
        event_filter=GameStateEnums.ROUND_END,
        action=levelup,
        condition=condition,
    )
    return Champion(effects=trigger2, summon_effect=effect)


# When I'm summoned, grant other allies +0|+3. Each round, the first time an ally takes damage, Rally.


def Galio2():
    effect = BuffEffect(exclude_origin=True, target=CardFilter(), health=3)
    rally = RallyEffect()
    trigger2 = TriggeredAction(
        event_filter=EntityEvents.DAMAGE,
        action=rally,
        activations_per_round=1,
        ally_enum=OriginEnum.T_ALLY,
    )
    return Champion(effects=trigger2, summon_effect=effect)


def Udyr():
    effect = CreateCardEffect(target=Set5Spells.StanceSwap)
    set_cost = BuffCostEffect(
        target=CardFilter(location=LocEnum.HAND, card_type=Set5Spells.StanceSwap),
        value=0,
        operator=Ops_.SET,
    )
    condition = Condition(
        target=TargetPlayer.ORIGIN_OWNER,
        condition=PlayerFlags.HAS_NO_X_HAND_CARD,
        parameter=Set5Spells.StanceSwap,
    )
    effect1 = BranchingAction(condition=condition, if_true=effect, if_false=set_cost)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Udyr2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL,
        threshold=3,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        condition=...,
        instance_bound=False,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(effects=watcher, strike_effect=effect1, summon_effect=effect1)


# When I'm summoned or Strike: Create a Stance Swap in hand or, if you have one, reduce it's cost to 0. I have +1|+1 for each stance you've cast this game.


def Udyr2():
    effect = CreateCardEffect(target=Set5Spells.StanceSwap)
    set_cost = BuffCostEffect(
        target=CardFilter(location=LocEnum.HAND, card_type=Set5Spells.StanceSwap),
        value=0,
        operator=Ops_.SET,
    )
    condition = Condition(
        target=TargetPlayer.ORIGIN_OWNER,
        condition=PlayerFlags.HAS_NO_X_HAND_CARD,
        parameter=Set5Spells.StanceSwap,
    )
    effect1 = BranchingAction(condition=condition, if_true=effect, if_false=set_cost)
    effect2 = DynamicAttackModifier()
    # TODO for every
    return Champion(
        effects=effect2,
        strike_effect=effect1,
        summon_effect=effect1,
        cardcode="05FR013T4",
        champion_spell=Set5Spells.SpiritsUnleashed,
    )


# When I'm summoned or Attack: Create a Darkness in hand if you don't have one. Your damage and kill spells accelerate to Fast and cost 1 less.
def Senna():
    if not any(
        is_copy_of(card, Set5Spells.Darkness) for card in self.owner.handcards()
    ):
        self.create_card(Set5Spells.Darkness)


class Senna2(Champion):
    def __init__(self, **kwargs) -> None:
        kwargs["spell_class"] = Set5Spells.DawningShadow
        super().__init__(**kwargs)

    async def board(self):
        self._internal = [
            PropertyRule(self, 1, Ops_.DECREMENT),
            PropertyRule(self, SpellSpeed_.FAST),
        ]
        self.owner.aura_manager.add_aura(
            None,
            None,
            lambda x: x.type == Types_.SPELL and x.spell_speed == SpellSpeed_.SLOW,
            attr_prop=self._internal,
            target_location=LocationsEnum.HAND,
        )

    async def attack_commit(self):
        if not any(
            is_copy_of(card, Set5Spells.Darkness) for card in self.owner.handcards()
        ):
            self.create_card(Set5Spells.Darkness)

    async def summon(self, target: Unit):
        if not any(
            is_copy_of(card, Set5Spells.Darkness) for card in self.owner.handcards()
        ):
            self.create_card(Set5Spells.Darkness)


# When an allied landmark is destroyed or Round Start: Deal 5 to the weakest enemy or the enemy Nexus if there are none.If an enemy unit would die, Obliterate it instead.
def Xerath():
    damage(get_weakest(self.opponent.boardunits()), 1)


class Xerath2(Champion):
    _cardcode = "05SH014T1"

    def __init__(self, **kwargs) -> None:
        kwargs["level_up_obj"] = Xerath3
        kwargs["spell_class"] = Set5Spells.RiteoftheArcane
        super().__init__(**kwargs)

    async def board(self):
        self.listener.aftereffect(EntityEvents.DESTROY_LANDMARK, self.card_effect)

    async def init(self):
        self.listener.aftereffect(
            EntityEvents.SUNDISC_RESTORED,
            self.owner.execute_level_up,
            unique=True,
            player_bound=True,
            form=Xerath2,
        )

    async def card_effect(self):
        damage(get_weakest(self.opponent.boardunits()), 3)


class Xerath3(Champion):
    _cardcode = "05SH014T2"

    def __init__(self, **kwargs) -> None:
        kwargs["spell_class"] = Set5Spells.RiteoftheArcane
        super().__init__(**kwargs)

    async def board(self):
        self.listener.aftereffect(EntityEvents.DESTROY_LANDMARK, self.card_effect)
        self.opponent.listener.tamper_event(EntityEvents.DIE, self.card_effect2)

    async def round_start(self):
        self.card_effect()

    async def card_effect2(self, effect_target, **kwargs):
        obliterate(effect_target)

    async def card_effect(self):
        try:
            damage(next(self.opponent.boardunits()), 5)
        except StopIteration:
            damage(self.opponent, 5)


# When I'm summoned, create a Darkness in hand if you don't have one. Round Start: Grant your Darkness everywhere 1 extra damage.
def Veigar():
    buff_everywhere(
        partial(
            set_attribute,
            attribute=Attr_.SPELL_DAMAGE,
            value=1,
            operator=Ops_.INCREMENT,
        ),
        lambda x: is_copy_of(x, Set5Spells.Darkness),
    )
    # TODO


class Veigar2(Champion):
    _cardcode = "05BC093T2"

    def __init__(self, **kwargs) -> None:
        kwargs["spell_class"] = Set5Spells.EventHorizon
        super().__init__(**kwargs)

    async def init(self):
        aura = self.listener.add_aura

    async def summon(self, **kwargs):
        if not any(card.cardcode == "05SI029" for card in self.owner.handcards()):
            create_card("05SI029")

    async def round_start(self):
        self.summon()
        buff_everywhere_advanced(
            lambda x: x.execute_set_attribute(Attr_.SPELL_DAMAGE, 1, Ops_.INCREMENT),
            lambda x: x.cardcode == "05SI029",
        )


# When you deal damage to the enemy Nexus, create a random Mecha-Yordle in hand or if you have one, grant all Mecha-Yordles in hand +1|+1 and reduce their cost by 1.
def Rumble():
    self.listener.on_event_counter(
        EntityEvents.DAMAGE,
        self.owner.execute_level_up,
        12,
        target_obj=TargetObject_.ORIGIN,
        subscribe=True,
        form=Rumble,
        increment_function=itemgetter("value"),
    )


class Rumble2(Champion):
    _cardcode = "05BC088T2"

    def __init__(self, **kwargs) -> None:
        kwargs["spell_class"] = Set5Spells.Flamespitter
        super().__init__(**kwargs)

    async def board(self):
        self.listener.aftereffect(
            EntityEvents.DAMAGE,
            self.card_effect,
            target_obj=TargetObject_.ORIGIN,
            condition_aftereffect=lambda x: x is self.opponent,
        )

    async def card_effect(self):
        mechas = self.owner.handcards(lambda x: is_subtype(x, SubTypes_.MECHA_YORDLE))
        if any(mechas):
            buff_attack_health(mechas, 1, 1)
            buff_cost(mechas, 1, 1)
        else:
            cardcode = json_manager.invoke(subtype=SubTypes_.MECHA_YORDLE)
            create_card(cardcode)


# Attack: Grant all allies with equal or less power than me +2|+2 and Impact.
def Poppy():
    self.listener.on_event_counter(
        GameStateEnums.ATTACK_COMMIT,
        self.owner.execute_level_up,
        3,
        form=Poppy,
        subscribe=True,
        condition_aftereffect=lambda x: x is self,
    )


class Poppy2(Champion):
    _cardcode = "05BC041T1"

    def __init__(self, **kwargs) -> None:
        kwargs["spell_class"] = Set5Spells.KeepersVerdict
        super().__init__(**kwargs)

    async def attack_commit(self):
        target = self.owner.boardunits(lambda x: x.attack <= self.attack)
        buff_attack_health(target, 1, 1)
        add_keyword(target, Keywords.IMPACT)


def Kennen():
    create = CreateCardEffect(Set5Spells.MarkoftheStorm)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Kennen2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.SUMMON,
        threshold=5,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        event_counter=EventCounterEnum.UNIQUE_TARGETS,
    )
    return Champion(effects=watcher, summon_effect=create)


def Kennen2():
    create = CreateCardEffect(Set5Spells.MarkoftheStorm)
    ta = TriggeredAction(
        event_filter=EntityEvents.BLOCK, ally_enum=OriginEnum.T_SELF, action=create
    )
    return Champion(
        attack_commit_effect=create,
        effects=ta,
        summon_effect=create,
        cardcode="05BC058T2",
        champion_spell=Set5Spells.LightningRush,
    )



def Pantheon():
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Pantheon2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.TARGETED,
        threshold=5,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        event_counter=EventCounterEnum.DISCRETE_ROUNDS,
    )
    return Champion(effects=watcher)


# Once a Pantheon has leveled up, grant me a random keyword for each round you've targeted allies this game.
def Pantheon2():
    # TODO event query
    effect = AddRandomKeywordEffect(target=AutoEntitySelector.SELF, count=...)
    ta = TriggeredAction(
        event_filter=EntityEvents.LEVEL_UP, action=effect, ally_enum=OriginEnum.SELF
    )
    return Champion(
        effects=ta, cardcode="05MT003T2", champion_spell=Set5Spells.ShieldVault
    )


def Jayce():
    choice_keyword = ChoiceValue(
        choices=[KeywordEnum.QUICKSTRIKE, KeywordEnum.CHALLENGER]
    )
    keyword = AddKeywordEffect(target=AutoEntitySelector.SELF, keyword=choice_keyword)
    create = CreateCardEffect(Set5Spells.AccelerationGate)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.LEVEL_UP, action=create, ally_enum=OriginEnum.T_SELF
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Jayce2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL,
        threshold=2,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        instance_bound=False,
        condition=...,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(play_effect=keyword, effects=[ta1, watcher])


# Each round, the first time you cast a 6+ cost spell, cast it again on the same targets.
def Jayce2():
    choice_keyword = ChoiceValue(
        choices=[KeywordEnum.QUICKSTRIKE, KeywordEnum.CHALLENGER]
    )
    keyword = AddKeywordEffect(target=AutoEntitySelector.SELF, keyword=choice_keyword)
    effect = RecastEventOfAction(target=...)
    ta = TriggeredAction(
        event_filter=EntityEvents.PLAY,
        action=effect,
        activations_per_round=1,
        condition=...,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
    )
    return Champion(
        effects=ta,
        play_effect=keyword,
        cardcode="05PZ022T2",
        champion_spell=Set5Spells.ShockBlast,
    )


# Strike: Create a Pokey Stick in hand or, if you have one, reduce its cost by 1.
def Gnar():
    effect = CreateCardEffect(target=Set5Spells.PokeyStick)
    set_cost = BuffCostEffect(
        target=CardFilter(location=LocEnum.HAND, card_type=Set5Spells.PokeyStick),
        value=2,
    )
    condition = Condition(
        target=TargetPlayer.ORIGIN_OWNER,
        condition=PlayerFlags.HAS_NO_X_HAND_CARD,
        parameter=Set5Spells.PokeyStick,
    )
    effect1 = BranchingAction(condition=condition, if_true=effect, if_false=set_cost)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Gnar2)
    ta = TriggeredAction(
        event_filter=GameStateEnums.ROUND_END,
        action=levelup,
        condition=PlayerFlags.PLUNDER,
    )
    return Champion(strike_effect=effect1, effects=ta)


def Gnar2():
    # TODO internal
    levelup = TransformEffect(target=AutoEntitySelector.SELF, new_form=Gnar)
    ta = TriggeredAction(
        event_filter=GameStateEnums.ROUND_END, action=levelup, condition=...
    )
    buff = AddKeywordEffect(
        target=AutoEntitySelector.STRONGEST_OPPONENT_BOARD_UNIT,
        keyword=KeywordEnum.OVERWHELM,
    )
    ta1 = TriggeredAction(
        event_filter=EntityEvents.LEVEL_UP, action=buff, ally_enum=OriginEnum.T_SELF
    )
    return Champion(
        effects=[ta, ta1], cardcode="05BC161T1", champion_spell=Set5Spells.Wallop
    )


def Ziggs():
    effect = PlaySkill(target=Set5Skills.ShortFuse)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Ziggs2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.DESTROY_LANDMARK,
        threshold=4,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        instance_bound=False,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(effects=watcher, attack_commit_effect=effect)


# Attack: Deal 2 to my blocker and the enemy Nexus.When an allied landmark is destroyed, deal 2 to the enemy Nexus.


def Ziggs2():
    effect = PlaySkill(target=Set5Skills.ShortFuse2)
    effect1 = DamageEffect(target=TargetPlayer.OPPONENT, value=2)
    ta = TriggeredAction(
        event_filter=EntityEvents.DESTROY_LANDMARK,
        action=effect1,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
    )
    return Champion(
        effects=ta,
        attack_commit_effect=effect,
        cardcode="05BC163T1",
        champion_spell=Set5Spells.BouncingBomb,
    )


def Yuumi():
    effect1 = BuffEffect(target=AutoEntitySelector.SELF, attack=1, health=1)
    effect2 = BuffEffect(
        target=AutoEntitySelector.THIS_ATTACHMENT_BEARER, attack=1, health=1
    )
    effect3 = BranchingAction(condition=..., if_true=effect2, if_false=effect1)
    ta = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START,
        action=effect3,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Yuumi2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.ATTACK_COMMIT,
        threshold=3,
        action_on_value=levelup,
        condition=...,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(effects=[watcher, ta])


def Yuumi2():
    effect1 = BuffEffect(
        target=AutoEntitySelector.SELF,
        attack=1,
        health=1,
        keyword=KeywordEnum.SPELLSHIELD,
    )
    effect2 = BuffEffect(
        target=AutoEntitySelector.THIS_ATTACHMENT_BEARER,
        attack=1,
        health=1,
        keyword=KeywordEnum.SPELLSHIELD,
    )
    effect3 = BranchingAction(condition=..., if_true=effect2, if_false=effect1)
    ta = TriggeredAction(
        event_filter=GameStateEnums.ROUND_START,
        action=effect3,
    )
    return Champion(
        effects=ta, cardcode="05BC058T2", champion_spell=Set5Spells.ProwlingProjectile
    )


def Tristana():
    effect = BuffEffect(target=PostEventParam.TARGET, attack=1)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        action=effect,
        condition=...,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Tristana2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.SUMMON,
        threshold=4,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        condition=...,
        instance_bound=False,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    # TODO for every
    effect1 = DynamicAttackModifier(value=...)
    return Champion(effects=[watcher, ta1, effect1])


# I have +1|+0 for each multi-region ally you've summoned this game.When you summon a multi-region ally, grant me and it +1|+0 and Impact.
def Tristana2():
    effect = BuffEffect(
        target=[PostEventParam.TARGET, AutoEntitySelector.SELF],
        attack=1,
        keyword=KeywordEnum.IMPACT,
    )
    ta1 = TriggeredAction(
        event_filter=EntityEvents.SUMMON,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        action=effect,
        condition=...,
    )
    # TODO for every
    effect1 = DynamicAttackModifier(value=...)
    return Champion(
        effects=[ta1, effect1],
        cardcode="05BC133T1",
        champion_spell="Set5Spells.BusterShot",
    )


def Nami():
    # TODO not immobile
    effect = BuffEffect(
        target=CardFilter(
            sorter=CardSorter.WEAKEST,
            custom_filter=lambda x: not x.has_keyword(KeywordEnum.IMMOBILE),
        ),
        attack=1,
    )
    ta1 = TriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL,
        ally_enum=OriginEnum.T_ALLY,
        action=effect,
        activations_per_round=1,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Nami2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.REFILL_SPELL_MANA,
        threshold=8,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY,
        instance_bound=False,
        event_counter=EventCounterEnum.COUNT_VALUE,
    )
    return Champion(effects=[ta1, watcher])


# When you cast a spell, grant +2|+1 to the weakest other ally that isn't Immobile.
def Nami2():
    # TODO not immobile
    effect = BuffEffect(
        target=CardFilter(sorter=CardSorter.WEAKEST), attack=2, health=1
    )
    ta1 = TriggeredAction(
        event_filter=EntityEvents.PLAY_SPELL,
        ally_enum=OriginEnum.T_ALLY,
        action=effect,
        activations_per_round=1,
    )
    return Champion(effects=ta1, cardcode="05BW005T1", champion_spell=Set5Spells.Ebb)


def Ahri():
    effect1 = RecallEffect(target=...)
    effect2 = SwapPositionsEffect(target=..., destination=...)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.BATTLE_STRIKE,
        ally_enum=OriginEnum.O_SELF,
        action=[effect1, effect2],
        activations_per_round=1,
    )
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Ahri2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.RECALL,
        threshold=6,
        action_on_value=levelup,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        instance_bound=False,
        event_counter=EventCounterEnum.COUNT_INSTANCES,
    )
    return Champion(effects=[ta1, watcher], champion_spell=Set5Spells.Charm)


# When you Recall an ally, reduce its cost by 1.
# Attack: Each time I attack strike, swap me with the ally to my right, then Recall it.
def Ahri2():
    effect = BuffCostEffect(target=PostEventParam.TARGET, value=1)
    ta = TriggeredAction(
        event_filter=EntityEvents.RECALL,
        ally_enum=OriginEnum.T_ALLY_O_ALLY,
        action=effect,
    )
    effect1 = RecallEffect(target=...)
    effect2 = SwapPositionsEffect(target=..., destination=...)
    ta1 = TriggeredAction(
        event_filter=EntityEvents.BATTLE_STRIKE,
        ally_enum=OriginEnum.O_SELF,
        action=[effect1, effect2],
    )
    return Champion(
        cardcode="05IO004T2", effects=[ta, ta1], champion_spell=Set5Spells.Charm
    )


def Caitlyn():
    effect = PlantFlashBombTrap(quantity=2)
    levelup = LevelupEffect(target=AutoEntitySelector.SELF, new_form=Caitlyn2)
    watcher = ValueTriggeredAction(
        event_filter=EntityEvents.DAMAGE,
        threshold=12,
        action_on_value=levelup,
        ally_enum=OriginEnum.O_ALLY,
        condition=...,
        instance_bound=False,
        event_counter=EventCounterEnum.COUNT_VALUE,
    )
    return Champion(
        effects=watcher,
        strike_effect=effect,
        champion_spell=Set5Spells.PiltoverPeacemaker,
    )


# Strike: Plant 4 Flashbomb Traps randomly in the top 10 cards in the enemy deck and deal damage to the enemy Nexus equal to the number of your traps activated this round.
def Caitlyn2():
    effect = PlantFlashBombTrap(quantity=2)
    # TODO query
    damage = DamageEffect(target=TargetPlayer.OPPONENT, value=...)
    return Champion(
        strike_effect=[effect, damage],
        champion_spell=Set5Spells.PiltoverPeacemaker,
        cardcode="05PZ006T2",
    )
