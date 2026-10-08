import ollama
from models import ModelInfo

def inspect_model(model_name: str) -> ModelInfo:
    """Inspect an Ollama model and return normalized model metadata."""

    response = ollama.show(model_name)

    details = response.details
    model_info = response.modelinfo
    if __name__ == "__main__":
        print(f"Details: {details}")
        print(f"Model Info:{model_info}")


    context_window = 8192

    for key, value in model_info.items():
        if key.endswith(".context_length"):
            context_window = int(value)
            break

    architecture = model_info.get(
        "general.architecture",
        getattr(details, "family", "unknown"),
    )

    quantization = getattr(
        details,
        "quantization_level",
        "unknown",
    )

    # 3. Infer HuggingFace Tokenizer name (Extract from HF link if present, or generate clean repo format)
    hf_link = model_info.get("general.license.link", "")
    tokenizer_name = resolve_tokenizer(hf_link,model_name, architecture)

    return ModelInfo(
        name=model_name,
        architecture= architecture,
        context_window=context_window,
        quantization=quantization,
        tokenizer_name= tokenizer_name,
    )


def resolve_tokenizer(hf_link: str,model_name:str, architecture: str) -> str:
    """Resolve the Hugging Face tokenizer for an Ollama model."""
    tokenizer_name = "" 
    if "huggingface.co/" in hf_link:
        # Extracts 'Qwen/Qwen3-4B' from 'https://huggingface.co/Qwen/Qwen3-4B/blob/main/LICENSE'
        parts = hf_link.split("huggingface.co/")[1].split("/")
        if len(parts) >= 2:
            tokenizer_name = f"{parts[0]}/{parts[1]}"
            return tokenizer_name
    
    if not tokenizer_name:
        # Fallback formatting: e.g. "Qwen/qwen2.5-coder"
        tokenizer_name = f"{architecture.capitalize()}/{model_name}"
        return tokenizer_name
    