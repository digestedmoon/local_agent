from typing import Any
from pydantic import BaseModel


class FunctionCall(BaseModel):
    name: str
    arguments: dict[str, Any]


class ToolCall(BaseModel):
    function: FunctionCall