"""Minimal Ollama client stub for local Ollama HTTP API."""

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
        return "Error: missing 'requests' library. Install it with: pip install requests"

    if not _is_ollama_up():
        return "Error: Ollama is not running or not reachable at http://127.0.0.1:11434"

    payload = {"model": model, "prompt": prompt, "stream": False}

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict):
            return data.get("response") or data.get("text") or response.text

        return str(data)

    except requests.exceptions.RequestException as e:
        return f"Error: Ollama request failed. {type(e).__name__}: {e}"