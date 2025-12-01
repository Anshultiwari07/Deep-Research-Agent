import os
from typing import Optional

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL_ID = os.getenv("HF_MODEL_ID", "meta-llama/Meta-Llama-3-8B-Instruct")

_client: Optional[InferenceClient] = None


def _get_client() -> Optional[InferenceClient]:
    """
    Lazily create a single InferenceClient for the whole app.
    """
    global _client

    if _client is not None:
        return _client

    if not HF_API_KEY:
        print("[HF LLM] HF_API_KEY not set – skipping real LLM calls.")
        return None

    try:
        _client = InferenceClient(
            model=HF_MODEL_ID,
            token=HF_API_KEY,
        )
        return _client
    except Exception as e:
        print(f"[HF LLM] Failed to init InferenceClient: {e}")
        return None


def generate_section_with_hf(
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 600,
    temperature: float = 0.3,
) -> str:
    """
    Call Hugging Face chat-completion model and return plain text.
    """
    client = _get_client()
    if client is None:
        return "[HF LLM NOT CONFIGURED]"

    try:
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[HF LLM] Error during generation: {e}")
        return "[HF LLM ERROR]"
