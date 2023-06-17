
from typing import Callable, List, Tuple
from attr import define, field

from data.JSONCard import JsonCard
from data.data_marshal import cardcode_json_dict
from enums.card_rarity import CardRarity
from enums.card_sorters import CardSorter
from enums.keywords import KeywordEnum
from enums.region import RegionEnum
from enums.spell_speed import SpellSpeedEnum
from enums.subtypes import SubTypes_
from enums.types import Types_
from resolvable_enums.card_conditions import CardFlags


@define(slots=False)
class BaseCardFilter:
    
    card_type: None = field(default=None)

    attack: int | Tuple | None = field(kw_only=True, default=None)
    health: int | Tuple | None = field(kw_only=True, default=None)
    cost: int | Tuple | None = field(kw_only=True, default=None)
    type: Types_ | None = field(default=Types_.UNIT)
    keyword: KeywordEnum | None = field(kw_only=True, default=None)
    
    subtype: SubTypes_ | None = field(kw_only=True, default=None)
    spell_speed: SpellSpeedEnum | None = field(kw_only=True, default=None)
    regions: RegionEnum | None = field(kw_only=True, default=None)
    rarity: CardRarity | None = field(kw_only=True, default=None)

    is_follower: bool = field(kw_only=True, default=None)
    is_new: bool | None = field(kw_only=True, default=None)
    can_afford: bool | None = field(kw_only=True, default=None)
    flags: List[CardFlags] | CardFlags = field(kw_only=True, default=None)
    excluding_flags: List[CardFlags] | None = field(kw_only=True, default=None)
    owner_same_regions: bool | None = field(kw_only=True, default=None)

    custom_filter: Callable[[JsonCard], bool] = field(kw_only=True, default=None)
    entity_pool: List | None = field(kw_only=True, default=None)
    output_count: bool | None = field(default=None, kw_only=True)

    def get_attributes_filter(self) -> List[Callable[[JsonCard], bool]]:
        # if self.card_type:
        #     card = class2jsondata(self.card_class)
        #     return [(self.card_class, card)]
       
        
        # if self.regions:
        #     aregion = (
        #         set([r.value for r in region])
        #         if isinstance(region, list)
        #         else set([region.value])
        #     )
        #     region_filter = lambda x: not region.isdisjoint(set(x["regionRefs"]))
        filters: Tuple[bool, Callable[[JsonCard], bool]] = (
            (True, lambda x: len(x["cardCode"]) == 7),
            (True, lambda x: x["set"] == "Set1"),
            (self.type, lambda x: x["type"] == self.type.value),
            (self.attack, lambda x: x["attack"] == self.attack),
            (self.health, lambda x: x["health"] == self.health),
            (self.spell_speed, lambda x: x["spellSpeed"] == self.spell_speed),
            # (self.regions, lambda x: region_filter(x)),
            (self.rarity, lambda x: x["rarity"] == self.rarity),
            (self.cost, lambda x: x["cost"] == self.cost),
            # (
            #     self.flags and CardFlags.IS_MULTIREGION in self.flags,
            #     lambda x: len(x["regions"]) > 1,
            # ),
            # (
            #     (self.flags and CardFlags.IS_FOLLOWER in self.flags)
            #     or self.is_follower,
            #     lambda x: self.is_follower
            #     == (x["type"] == "Unit" and x["supertype"] != "Champion"),
            # ),
        )
        return [
            filter_tuple[1] for filter_tuple in filters if filter_tuple[0] is not None
        ]
        # ret_val = [
        #     (import_card(st[1]), st[1])
        #     for st in cards.items()
        #     if all(filter_obj[1](st[1]) for filter_obj in filters)
        # ]
        # if self.quantity:
        #     return sample(ret_val, k=self.quantity)
        # return ret_val

    def resolve(self, origin):
        cards = cardcode_json_dict
        filter_obj = self.get_attributes_filter()
        cards = {k:v for k,v in cards.items() if all(subfilter(v) for subfilter in filter_obj)}
        if self.owner_same_regions:
            region = {r.value for r in origin.owner.regions}
            lam = lambda x,y: not region.isdisjoint(y["regionRefs"])
            return {k:v for k,v in cards.items() if lam(k,v)}
        else:
            return cards
    
@define
class InvokeBaseCardFilter(BaseCardFilter):
    type: Types_ | None = field(kw_only=True, default=None)
    subtype: SubTypes_ = field(init=False, default=SubTypes_.CELESTIAL)
    quantity: int = field(kw_only=False, default=3)


@define
class ManifestBaseCardFilter(BaseCardFilter):
    quantity: int = field(init=False, default=3)


# @define
# class BaseCardRandomSelector(BaseCardFilter, EntitySelector):
#     ...


@define
class BaseCardRandomSelector():
    ...