# Guardrail — Minimal medical chatbot with Ollama integration

This repository contains a minimal CLI medical education chatbot that uses
a local Ollama HTTP backend. It includes conservative guardrails and a
local fallback when the model backend is unavailable.

Files
- app.py: CLI loop and `medical_chatbot()` flow. Implements guardrail checks
  and a local fallback responder when Ollama is unreachable.
- llm/ollama_client.py: Small Ollama client wrapper with health checks and
  robust timeout/connection handling. Returns helpful error strings when the
  local Ollama server cannot be reached.
- guardrails/input_guard.py: (input validation) Intended to contain the
  `check_input()` function used by `app.py` to block disallowed requests.
- guardrails/pipeline.py: (utility / pipeline helpers) created for future
  processing steps.

Quick start

1. Install dependencies:

```bash
pip install requests
```

2. (Optional) Run a local Ollama server if you want live model responses.
   If Ollama is not running, the app will use a safe local fallback.

3. Run the app:

```bash
python app.py
```

Notes
- The project intentionally returns conservative, non-diagnostic text and
  instructs users to consult healthcare professionals for personalized care.
- To improve the bot's behavior, expand `guardrails/input_guard.py`'s
  `check_input()` function and extend `llm/ollama_client.py` with streaming
  or authentication features if needed.

Contributing
- Open an issue or submit a PR with updates. Keep medical responses
  conservative and non-prescriptive.
