from attr import define


@define
class EventCounter:
    value: int

@define
class RoundEventCounter(EventCounter):
    last_round_tracked: int


@define
class InstanceCounter(EventCounter):
    ...

@define
class AttributeCounter(EventCounter):
    ...
