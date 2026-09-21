"""Minimal Ollama client stub for local Ollama HTTP API."""

import json
from typing import Optional

try:
    import requests  # type: ignore
except Exception:
    requests = None  # type: ignore

OLLAMA_BASE = "http://127.0.0.1:11434"
OLLAMA_URL = OLLAMA_BASE + "/api/generate"
MODEL = "llama3.2"
DEFAULT_TIMEOUT = 120


def _is_ollama_up(timeout: float = 2.0) -> bool:
    if not requests:
        return False
    try:
        r = requests.get(OLLAMA_BASE + "/api/tags", timeout=timeout)
        return r.ok
    except requests.exceptions.RequestException:
        return False


def ask_llama(prompt: str, model: Optional[str] = None, timeout: Optional[int] = None) -> str:
    if model is None:
        model = MODEL
    if timeout is None:
        timeout = DEFAULT_TIMEOUT

    if not requests:
        return "Error: missing 'requests' library. Install with: pip install requests"

    if not _is_ollama_up():
        return f"Error: Ollama not reachable at {OLLAMA_BASE}. Start ollama serve and ensure the model is available."

    payload = {"model": model, "prompt": prompt, "stream": False}

    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, dict):
            # Ollama responses vary; prefer common keys
            return data.get("response") or data.get("text") or json.dumps(data)
        return resp.text
    except requests.exceptions.RequestException as e:
        return f"Error: Ollama request failed. {type(e).__name__}: {e}"