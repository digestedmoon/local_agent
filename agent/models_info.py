import ollama
import re
from models import ModelInfo

def inspect_model(model_name: str) -> ModelInfo:
    """Inspect an Ollama model and return normalized model metadata."""

    response = ollama.show(model_name)

    details = response.details
    model_info = response.modelinfo

    context_window = 8192

    for key, value in model_info.items():
        if key.endswith(".context_length"):
            context_window = int(value)
            break

    running_context_window= 8192
    running_models = ollama.ps()

    for model in running_models.models:
        running_context_window= int(model.         context_length)
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

    MODELINFO = ModelInfo(
        name=model_name,
        architecture= architecture,
        native_context_window=context_window,
        runtime_context_window =running_context_window,
        quantization=quantization,
        tokenizer_name= tokenizer_name,
    )
    print(MODELINFO)
    return MODELINFO




def resolve_tokenizer(hf_link: str, model_name: str, architecture: str) -> str:
    """Dynamically clean architecture and model names into a valid HF repo ID."""
    
    # 1. If a HuggingFace link exists, extract org/repo directly
    if hf_link and "huggingface.co/" in hf_link:
        parts = hf_link.split("huggingface.co/")[1].split("/")
        if len(parts) >= 2:
            org, repo = parts[0], parts[1]
            clean_repo = re.sub(r'[^a-zA-Z0-9._-]', '', repo.replace(":", "-")).strip(".-")
            return f"{org}/{clean_repo}"

    # 2. Clean model name: drop ':latest', replace colons with dashes, remove bad chars
    clean_model = model_name.replace(":latest", "").replace(":", "-")
    clean_model = re.sub(r'[^a-zA-Z0-9._/-]', '', clean_model).strip(".-")

    # 3. If model already has a creator/org specified (e.g. "hhao/qwen2.5-coder-tools")
    if "/" in clean_model:
        return clean_model

    # 4. Dynamically clean architecture: remove numbers & symbols (e.g., 'qwen3' -> 'qwen')
    clean_arch = re.sub(r'[^a-zA-Z]', '', architecture).title() if architecture else "Unknown"

    # Combine org and model, ensuring start/end characters are valid alphanumeric
    org = re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$', '', clean_arch)
    repo = re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$', '', clean_model)
    final_name = f"{org}/{repo}"
    return final_name