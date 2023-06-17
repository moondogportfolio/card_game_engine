from typing import Any, Tuple
from attr import define

from actions.base_action import BaseTargetAction
from classes.gamestate import GameState
from events.base_event import BaseEvent
from events.battle.strike import StrikeEvent
from events.movement.recall_event import RecallEvent

