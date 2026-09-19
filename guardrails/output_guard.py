# guardrails/output_guard.py

import re


UNSAFE_MEDICAL_PATTERNS = [

    r"\byou should increase your dose\b",

    r"\bincrease your medication\b",

    r"\bdouble your dose\b",

    r"\bstop taking your medication\b",

    r"\bstop taking your medicine\b",

    r"\bstart taking .* medication\b",

    r"\btake .* mg .* daily\b",

    r"\btake .* mg .* twice a day\b",
]


DIAGNOSIS_PATTERNS = [

    r"\byou definitely have\b",

    r"\byou have been diagnosed with\b",

    r"\bthis means you have\b",

    r"\byou are suffering from\b",
]

def detect_unsafe_output(text: str):

    text = text.lower()

    violations = []

    for pattern in UNSAFE_MEDICAL_PATTERNS:

        if re.search(pattern, text):

            violations.append({
                "type": "UNSAFE_MEDICAL_ADVICE",
                "pattern": pattern
            })


    for pattern in DIAGNOSIS_PATTERNS:

        if re.search(pattern, text):

            violations.append({
                "type": "DIAGNOSIS_CLAIM",
                "pattern": pattern
            })


    return violations

def validate_output(text: str):

    violations = detect_unsafe_output(text)

    if not violations:

        return {
            "safe": True,
            "action": "allow",
            "violations": []
        }


    return {
        "safe": False,
        "action": "block",
        "violations": violations
    }