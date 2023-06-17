from importlib import import_module
from typing import Any, List, Tuple, Dict, Optional, Union
import libcst as cst

from data.data_marshal import _load_cards, name2cardcode, cardcode_json_dict

# body = cst.BaseSuite()
# cl = cst.FunctionDef(name='', params=None, body=body)


class Visitor(cst.CSTVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.cont: Dict[str, Any] = {}
        self.current_class: str = ""

    def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:
        # self.cont[node.name.value]
        self.current_class = node.name.value

    def visit_FunctionDef_body(self, node: cst.FunctionDef) -> None:
        # return super().visit_FunctionDef_body(node)
        self.cont[self.current_class] = node.body

    def leave_ClassDef_body(self, node: cst.ClassDef) -> None:
        self.current_class = ""


class TypingTransformer(cst.CSTTransformer):
    def __init__(self) -> None:
        super().__init__()
        self.current: str = ""
        self.body: cst.BaseSuite = ""
        self.activation_effects = []
        self.effects = []
        self.type = None

    def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:
        self.current = node.name.value

    def visit_FunctionDef(self, node: cst.FunctionDef) -> Optional[bool]:
        self.body = node.body

    # def leave_Call(self, original_node: cst.Call, updated_node: "Call") -> "BaseExpression":
    #     original_node.
    #     return super().leave_Call(original_node, updated_node)

    def leave_ClassDef(self, original_node: cst.ClassDef, updated_node: cst.ClassDef):
        # activation = cst.Arg(value=self.activation_effects, keyword=cst.Name('activation_effect'))
        # effects = cst.Arg(value=self.effects, keyword=cst.Name('effects'))
        # fnc = cst.Call(func=cst.Name('Spell'), args=[activation, effects])
        try:
            name = original_node.name.value
            print(name)
            cardcode = name2cardcode.get(name)
            descriptionRaw = cardcode_json_dict.get(cardcode).get('descriptionRaw')
        except AttributeError:
            return original_node
        descriptionRaw = descriptionRaw.replace('\n', '')
        descriptionRaw = descriptionRaw.replace('\r', '')
        comment = cst.Comment(f'#{descriptionRaw}')
        el = cst.EmptyLine(comment=comment)
        name = cst.Name(value=self.current)
        params = cst.Parameters()
        lines = cst.EmptyLine()
        return cst.FunctionDef(
            name=name,
            params=params,
            body=self.body,
            leading_lines=[lines],
            lines_after_decorators=[el],
        )
        # return updated_node

    # def leave_FunctionDef(
    #     self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    # ):
    #     print(original_node.body)
    #     raise ImportError
    #     return super().leave_FunctionDef(original_node, updated_node)

    # def leave_ClassDef(self, original_node: cst.ClassDef, updated_node: cst.ClassDef) -> Optional[bool]:
    #     name = original_node.name.value
    #     cardcode = _name2cardcode.get(name)
    #     descriptionRaw = _cards.get(cardcode).get('descriptionRaw')
    #     descriptionRaw = descriptionRaw.replace('\n', '')
    #     descriptionRaw = descriptionRaw.replace('\r', '')
    #     comment = cst.Comment(f'#{descriptionRaw}')
    #     el = cst.EmptyLine(comment=comment)
    #     new_node = original_node.with_changes(lines_after_decorators=[el])
    #     return new_node

    # print(original_node.body)
    # return cst.FlattenSentinel([original_node, el])


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


modifier(5, "Landmarks")

