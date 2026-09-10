BLOCKED_PATTERNS = [
    "give me a prescription",
    "prescribe medicine",
    "prescribe medication",
    "ignore previous instructions",
    "ignore your instructions",
    "reveal your system prompt"
]


def check_input(user_input: str):

    text = user_input.lower()

    for pattern in BLOCKED_PATTERNS:

        if pattern in text:

            return {
                "allowed": False,
                "reason": "Unsafe or restricted request detected"
            }

    return {
        "allowed": True,
        "reason": None
    }