from models import Message

class ContextManager:
    def __init__(self, tokenizer:int, context_window:int, max_output_tokens: int= 2048, safety_margin: int= 256):
        self.tokenizer = tokenizer
        self.context_window = context_window
        self.max_output_tokens = max_output_tokens
        self.safety_margin = safety_margin

    @property
    def input_budget(self) -> int:
        return (self.context_window- self.max_output_tokens  - self.safety_margin)

    def build_context(self,messages: list[Message],) -> list[Message]:

        if not messages:
            return []

        system_message = messages[0]
        remaining_messages = messages[1:]

        selected = []

        for message in reversed(remaining_messages):
            candidate = [system_message,message,*selected,]

            token_count = self.tokenizer.count(candidate)

            if token_count > self.input_budget:
                break

            selected.append(message)

        selected.reverse()

        return [
            system_message,
            *selected,
        ]
        