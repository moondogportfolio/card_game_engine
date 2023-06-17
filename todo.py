from actions.attribute.buff_everywhere import BuffEverywhereEffect
from actions.attribute.damage import DamageEffect
from actions.base_action import BaseAction
from actions.postevent import PostEventParamGetter
from actions.reactions.state_triggered_action import StateTriggeredAction
from actions.reactions.triggered_action import TriggeredAction
from actions.reactions.value_triggered_action import ValueTriggeredAction


TriggeredAction
    #MULTIPLE TRIGGERS
    #CONDITION

ValueTriggeredAction
TriggeredAction
    #ONCE YOU'VE

DamageEffect / BaseAction
    #MODIFIERS


PostEventParamGetter
    #CREATE -> BUFF CREATED

#Status effects selectors
    #STUN, select weakest among not stunned units

#Event history
    #STRONGEST DEAD

StateTriggeredAction
    #TriggeredAction but for new cards

#RANDOMIZE


BuffEverywhereEffect
    #-> DynamicModifier
    # 

# When I'm summoned, grant me all positive KeywordEnum allies have had this game.
# When I see an ally with a new positive keyword, grant it to me. 