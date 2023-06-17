from importlib import import_module
from typing import Any, List, Tuple, Dict, Optional, Union
import libcst as cst

from data.data_marshal import _load_cards, name2cardcode, cardcode_json_dict


class TypingTransformer(cst.CSTTransformer):
    def __init__(self) -> None:
        super().__init__()
        self.name = ""

    def visit_FunctionDef(self, node: cst.FunctionDef) -> Optional[bool]:
        self.name = node.name.value

    # def leave_Call(self, original_node: cst.Call, updated_node: "Call") -> "BaseExpression":
    #     original_node.
    #     return super().leave_Call(original_node, updated_node)

    def leave_Return(self, original_node: cst.Return, updated_node: cst.Return):
        val: cst.Call = original_node.value
        new_args = [x for x in val.args]
        cc = f"'{name2cardcode[self.name]}'"
        new_arg = cst.Arg(
            keyword=cst.Name("cardcode"),
            value=cst.SimpleString(value=cc),
            equal=cst.AssignEqual(
                whitespace_after=cst.SimpleWhitespace(" "),
                whitespace_before=cst.SimpleWhitespace(" "),
            ),
        )
        print(cst.Module([]).code_for_node(new_arg))
        new_args.append(new_arg)
        new_val = cst.Call(func=val.func, args=new_args)
        new_return = cst.Return(value=new_val)
        return new_return
    

def modifier(set_number: int, type: str):
    directory = f"./Sets/SET{set_number}/{type}.py"
    new_directory = f"./Sets/SET{set_number}/{type}new.py"
    code = None
    with open(directory, "r") as source:
        x = cst.parse_module(source.read())
        transformer = TypingTransformer()
        new_tree = x.visit(transformer)
        code = new_tree.code
    with open(new_directory, "wt") as dest:
        dest.write(code)


modifier(6, "Equipments")
