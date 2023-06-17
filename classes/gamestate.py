
from classes.manager_attachment import AttachmentManager
from classes.manager_counter import CounterManager
from classes.manager_entity import EntityManager
from classes.manager_event import EventManager
from classes.manager_input import InputManager
from classes.manager_listeners import ListenerManager
from classes.manager_location import LocationManager
from classes.manager_spellstack import SpellStackManager
from classes.manager_stack import StackManager
from entity_classes.player import Player
from enums.gamestate import GameStateEnums





class GameState:
    def __init__(self) -> None:
        self.entity_man = EntityManager()
        self.event_man = EventManager()
        self.game_phase: GameStateEnums | None = None
        self.loc_man = LocationManager()
        self.stack_manager = StackManager()
        self.input_manager = InputManager()
        self.player_turn: Player | None = None
        self.player_out_of_turn: Player | None = None
        self.listener_man = ListenerManager()
        self.counter_man = CounterManager()
        self.spell_stack_man = SpellStackManager()
        self.attach_man = AttachmentManager()


    def transition(self, new_state):
        ...

    async def step(self):
        if not self.stack_manager.stack:
            return False
        self.stack_manager.resolve_stack(self)

    def change_location(self):
        self.loc_man

    def set_phase(self, state: GameStateEnums, events):
        print(f'Entering {state} phase.')
        self.game_phase = state
        for event in events:
            self.stack_manager.add_to_queue(event)
        self.stack_manager.resolve_stack(self)
