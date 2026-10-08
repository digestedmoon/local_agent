from abc import ABC, abstractmethod
from transformers import AutoTokenizer
from models import Message, ModelInfo 

class Tokenizer(ABC):
    @abstractmethod
    def count(self, messsages: list[Message])-> int:
        pass 

class HFTokenizer(Tokenizer):
    def __init__(self, model_info: str):
        self.tokenzier = AutoTokenizer.from_pretrained(model_info)

    def count(self,messages: list[Message])->int:
        chat = [
            {
                "role": message.role,
                "content":message.role or "",
            }
            for message in messages
        ]
        tokens = self.tokenzier.apply_chat_template(chat, tokenize = True, add_generation_prompt = True)
        return len(tokens)

def create_tokenizer(model_info: ModelInfo) -> Tokenizer:

    if not model_info.tokenizer_name:
        raise ValueError(
            f"No tokenizer available for '{model_info.name}'."
        )

    return HFTokenizer(model_info.tokenizer_name)