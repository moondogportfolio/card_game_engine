from typing import Any, List
from attr import define

from enums.custom_function import CustomFunctionEnum


@define
class CustomFunction:
    evaluator: CustomFunctionEnum
    parameters: Any | List
