from models.message import Message

def from_ollama(ollama_message)-> Message:
    return Message(
        role = ollama_message.role,
        content = ollama_message.content,
        tool_name= ollama_message.tool_name, 
        tool_calls= 
        (
            [call.model_dump() for call in ollama_message.tool_calls] if ollama_message.tool_calls else None
        )
    )
