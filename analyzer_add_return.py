from importlib import import_module
from typing import Any, List, Tuple, Dict, Optional, Union
import libcst as cst

from data.data_marshal import _load_cards, name2cardcode, cardcode_json_dict


class TypingTransformer(cst.CSTTransformer):
    def __init__(self) -> None:
        super().__init__()

        # activation = cst.Arg(value=self.activation_effects, keyword=cst.Name('activation_effect'))
        # effects = cst.Arg(value=self.effects, keyword=cst.Name('effects'))
        # fnc = cst.Call(func=cst.Name('Spell'), args=[activation, effects])
    

    def leave_FunctionDef(self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef):
        # expr = cst.Expr(cst.parse_expression(f'Spell(activation_effect = effect)'))
        expr = cst.Expr(cst.parse_expression(f'Unit(effects = effect)'))
        return cst.FlattenSentinel([updated_node, expr])

    # def leave_FunctionDef(
    #     self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    # ):
    #     print(original_node.body)
    #     raise ImportError
    #     return super().leave_FunctionDef(original_node, updated_node)


def modifier(set_number: int, type: str):
    directory = f"./Sets/SET{set_number}/{type}new.py"
    new_directory = f"./Sets/SET{set_number}/{type}new_return.py"
    code = None
    with open(directory, "r") as source:
        x = cst.parse_module(source.read())
        transformer = TypingTransformer()
        new_tree = x.visit(transformer)
        code = new_tree.code
    with open(new_directory, "wt") as dest:
        dest.write(code)


modifier(5, "Units")

