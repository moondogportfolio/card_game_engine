
from typing import Any, Callable

from attr import define



@define
class Watcher:
    value: Any
    event_filter: ...
    value_setter: Callable[[Any], Any]

@define
class IntegerWatcher(Watcher):
    value: int
    value_setter: Callable[[Any], int]


@define
class ListWatcher(Watcher):
    value: int
    value_setter: Callable[[Any], None]
