"""Minimal Ollama client stub for local Ollama HTTP API.

This module provides a small wrapper with basic health checks and
robust error handling so the application can surface helpful messages
when the local Ollama server isn't running or times out.
"""
from typing import Optional

import requests
from requests.exceptions import RequestException


OLLAMA_BASE = "http://localhost:11434"
OLLAMA_URL = OLLAMA_BASE + "/api/generate"
MODEL = "llama3.2"
DEFAULT_TIMEOUT = 15


def _is_ollama_up(timeout: float = 2.0) -> bool:
    """Try several common health endpoints to detect a running Ollama server."""
    candidates = ["/v1/health", "/health", "/api/health", "/"]
    for path in candidates:
        try:
            r = requests.get(OLLAMA_BASE + path, timeout=timeout)
            if r.ok:
                return True
        except RequestException:
            continue
    return False


def ask_llama(prompt: str, model: Optional[str] = None, timeout: Optional[int] = None) -> str:
    """Send a request to Ollama and return a text response.

    On network errors or timeouts, returns a friendly error string that the
    caller (UI or CLI) can display to the user instead of raising.
    """
    if model is None:
        model = MODEL
    if timeout is None:
        timeout = DEFAULT_TIMEOUT

    if not _is_ollama_up():
        return (
            f"Error: Unable to reach Ollama at {OLLAMA_BASE}. "
            "Make sure the Ollama server is running and reachable on localhost:11434."
        )

    payload = {"model": model, "prompt": prompt, "stream": False}

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
        response.raise_for_status()
    except RequestException as e:
        return (
            f"Error: request to Ollama failed: {e}. "
            "Check that Ollama is running and try again."
        )

    try:
        data = response.json()
        # Ollama response schemas vary; prefer 'response' but fall back to text
        return data.get("response") or data.get("text") or response.text
    except ValueError:
        return response.text