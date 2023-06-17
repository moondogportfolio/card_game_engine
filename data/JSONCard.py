
from typing import Dict, List, Optional, TypedDict


class JsonCard(TypedDict):
    associatedCards: List
    associatedCardRefs: List
    assets: List[Dict]
    regions: str
    regionRefs: str
    attack: int
    cost: int
    health: int
    description: str
    descriptionRaw: str
    levelupDescription: str
    levelupDescriptionRaw: str
    flavorText: str
    artistName: str
    name: str
    cardCode: str
    keywords: List[str]
    keywordRefs: List[str]
    spellSpeed: str
    spellSpeedRef: str
    rarity: Optional[str]
    rarityRef: Optional[str]
    subtype: str
    subtypes: List[str]
    supertype: str
    type: str
    collectible: bool
    set: str
