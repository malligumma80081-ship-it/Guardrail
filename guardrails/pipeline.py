from typing import Dict
from guardrails.pii_guard import (
    detect_pii,
    mask_pii
)

from guardrails.medical_safety import (
    classify_medical_safety,
    get_safe_response
)
from llm.ollama_client import ask_llama


def allow(reason=None) -> Dict:
    return {
        "allowed": True,
        "action": "allow",
        "risk_level": "low",
        "reason": reason
    }


def block(reason: str) -> Dict:
    return {
        "allowed": False,
        "action": "block",
        "risk_level": "high",
        "reason": reason
    }


def redirect(reason: str) -> Dict:
    return {
        "allowed": False,
        "action": "redirect",
        "risk_level": "medium",
        "reason": reason
    }

user_input = input("User: ")

# --------------------------------
# 1. PII Detection
# --------------------------------

pii_result = detect_pii(user_input)

safe_input = mask_pii(user_input)


# --------------------------------
# 2. Medical Safety
# --------------------------------

safety_result = classify_medical_safety(
    safe_input
)


# --------------------------------
# 3. Policy Decision
# --------------------------------

action = safety_result["action"]


if action in [
    "redirect",
    "emergency_redirect"
]:

    response = get_safe_response(action)

    print("\nAssistant:")
    print(response)

else:

    # Send safe input to Llama 3.2
    response = ask_llama(safe_input)

    print("\nAssistant:")
    print(response)