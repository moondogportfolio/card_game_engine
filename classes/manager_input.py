from __future__ import annotations
from asyncio import Event, get_event_loop
import sys
from typing import TYPE_CHECKING, List
from random import choices as random_pickings

from classes.manager_spellstack import TargetCoords

if TYPE_CHECKING:
    from entity_selectors.input import Input


class InputManager:

    def __init__(self) -> None:
        self.input_stack = None

    def set_input_object(self, input_obj):
        self.input_stack = input_obj

    # async def manual_input(self):
    #     if self.input_stack is None:
    #         return
    #     print(' ______________')
    #     print(f'|{self.input_stack.message}')
    #     print('|______________')
    #     print(*self.input_stack.choices, sep='\n')
    #     print('______________')
    #     inp = int(await self.ainput())
    #     self.input_stack.selection = self.input_stack.choices[inp]
    #     self.input_stack = None

    def generate_target_coords(self, target):
        try:
            coords = TargetCoords(
                index=target.index,
                location=target.location,
                player=target.owner,
            )
            return coords
        except AttributeError:  # target is not card
            return target

    async def manual_input(self, input_obj: Input, choices: List):
        if input_obj.randomize:
            if input_obj.quantity < len(choices):
                random_objects = random_pickings(choices, k=input_obj.quantity)
            else:
                random_objects = choices
            return [self.generate_target_coords(subchoice) for subchoice in random_objects]
        if input_obj.minimum == 0:
            choices.append('pass')
        print(' ______________')
        print(f'|{input_obj.message}')
        print(f'|max: {input_obj.quantity}')
        print(f'|min: {input_obj.minimum}')
        print('|______________')
        print(*choices, sep='\n')
        print('______________')
        inp = await self.ainput()
        inp = inp[:-1]
        inputs = [self.generate_target_coords(choices[subinput]) for subinput in map(int, list(inp))]
        return inputs if len(inputs) > 1 else inputs[0]



    async def ainput(self, string: str=' ') -> str:
        await get_event_loop().run_in_executor(
                None, lambda s=string: sys.stdout.write(s+' '))
        return await get_event_loop().run_in_executor(
                None, sys.stdin.readline)