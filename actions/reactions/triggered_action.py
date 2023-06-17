
from enum import Enum
from typing import List
from attr import define, field
from actions.base_action import BaseAction
from actions.reactions.continuous_action import ContinuousAction

@define
class TriggeredAction(ContinuousAction):
    action: BaseAction | List[BaseAction]

    

@define
class AllyOrigin_TA(TriggeredAction):
    '''
    Action origin is ally, target is any
    '''
    ...

@define
class BearerTarget_TA(TriggeredAction):
    ...

