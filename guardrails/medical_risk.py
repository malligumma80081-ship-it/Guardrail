import re


MEDICAL_KEYWORDS = [
    "diabetes",
    "hypertension",
    "blood pressure",
    "blood test",
    "cbc",
    "anemia",
    "cholesterol",
    "insulin",
    "medicine",
    "medication",
    "symptoms",
    "disease",
    "health",
    "treatment",
    "doctor",
    "patient"
]


HIGH_RISK_PATTERNS = [
    r"\bdiagnose\b",
    r"\bdiagnosis\b",
    r"\bprescribe\b",
    r"\bprescription\b",
    r"\bdosage\b",
    r"\bexact dose\b",
    r"\bwhich medicine should i take\b"
]


EMERGENCY_PATTERNS = [
    r"\boverdose\b",
    r"\btook too much\b",
    r"\bcan't breathe\b",
    r"\bcannot breathe\b",
    r"\blost consciousness\b",
    r"\bunconscious\b"
]


def contains_medical_keyword(text: str) -> bool:

    text = text.lower()

    return any(
        keyword in text
        for keyword in MEDICAL_KEYWORDS
    )


def classify_medical_risk(user_input: str):

    text = user_input.lower().strip()

    # -------------------------
    # Emergency
    # -------------------------

    for pattern in EMERGENCY_PATTERNS:

        if re.search(pattern, text):

            return {
                "domain": "medical",
                "risk_level": "critical",
                "action": "emergency_redirect",
                "reason": "Potential emergency situation detected"
            }

    # -------------------------
    # High risk
    # -------------------------

    for pattern in HIGH_RISK_PATTERNS:

        if re.search(pattern, text):

            return {
                "domain": "medical",
                "risk_level": "high",
                "action": "redirect",
                "reason": "Personalized medical advice requested"
            }

    # -------------------------
    # Medical domain
    # -------------------------

    if contains_medical_keyword(text):

        return {
            "domain": "medical",
            "risk_level": "low",
            "action": "allow",
            "reason": "General medical information"
        }

    # -------------------------
    # Outside domain
    # -------------------------

    return {
        "domain": "non_medical",
        "risk_level": "low",
        "action": "block",
        "reason": "Request is outside the medical chatbot domain"
    }

if __name__ == "__main__":

    test_cases = [

        "What is diabetes?",

        "What is hypertension?",

        "What does a CBC test measure?",

        "Diagnose my condition.",

        "Give me a prescription.",

        "What dosage should I take?",

        "I took too much medication.",

        "What is Python?",

    ]

    for query in test_cases:

        result = classify_medical_risk(query)

        print("\nQuery:", query)
        print("Result:", result)    