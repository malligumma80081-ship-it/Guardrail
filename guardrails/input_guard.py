# BLOCKED_PATTERNS = [
#     "give me a prescription",
#     "prescribe medicine",
#     "prescribe medication",
#     "ignore previous instructions",
#     "ignore your instructions",
#     "reveal your system prompt"
# ]


# def check_input(user_input: str):

#     text = user_input.lower()

#     for pattern in BLOCKED_PATTERNS:

#         if pattern in text:

#             return {
#                 "allowed": False,
#                 "reason": "Unsafe or restricted request detected"
#             }

#     return {
#         "allowed": True,
#         "reason": None
#     }

from guardrails.pipeline import allow, block, redirect


BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "ignore your instructions",
    "reveal your system prompt",
    "give me a prescription",
    "prescribe medicine",
    "prescribe medication"
]

REDIRECT_PATTERNS = [
    "what dosage should i take",
    "how much medicine should i take",
    "which medicine should i take"
]


def check_input(user_input: str):

    text = user_input.lower().strip()

    # High-risk requests
    for pattern in BLOCKED_PATTERNS:

        if pattern in text:

            return block(
                "Unsafe or restricted request detected"
            )

    # Personalized medical advice
    for pattern in REDIRECT_PATTERNS:

        if pattern in text:

            return redirect(
                "Personalized medical advice requested"
            )

    return allow()

def validate_input(user_input: str):
    if not user_input:
        return {
            "allowed": False,
            "reason": "Empty input"
        }

    user_input = user_input.strip()

    if len(user_input) > 4000:
        return {
            "allowed": False,
            "reason": "Input is too long"
        }

    return {
        "allowed": True,
        "reason": "Input accepted"
    }