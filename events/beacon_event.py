from attr import define

from enums.entity_events import EntityEvents


@define
class BeaconEvent:
    event: EntityEvents