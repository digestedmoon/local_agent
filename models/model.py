from pydantic import BaseModel


class ModelInfo(BaseModel):
    name: str
    architecture: str
    context_window: int
    quantization: str
    tokenizer_name: str