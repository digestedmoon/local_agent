from pydantic import BaseModel


class ModelInfo(BaseModel):
    name: str
    architecture: str
    quantization: str

    native_context_window: int 
    runtime_context_window: int

    tokenizer_name: str