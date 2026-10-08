from pydantic import BaseModel
from .tool import ToolCall


class Message(BaseModel):
    role : str 
    content: str | None = None 
    tool_name : str | None = None
    tool_calls : list[ToolCall]| None = None