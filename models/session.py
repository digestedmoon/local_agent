from pydantic import BaseModel
from datetime import datetime
from .message import Message

class Session(BaseModel):
    session_id: str
    created_at: datetime
    updated_at: datetime
    messages: list[Message]
