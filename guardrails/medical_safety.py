# guardrails/medical_safety.py

import re


EMERGENCY_PATTERNS = [
    r"\bcan't breathe\b",
    r"\bcannot breathe\b",
    r"\bsevere breathing\b",
    r"\bunconscious\b",
    r"\bpassed out\b",
    r"\boverdosed\b",
    r"\bdrug overdose\b",
    r"\bsevere chest pain\b",
    r"\bnot breathing\b",
]


HIGH_RISK_PATTERNS = [
    r"\bdiagnose me\b",
    r"\bwhat disease do i have\b",
    r"\bwhat illness do i have\b",
    r"\bwhat medicine should i take\b",
    r"\bwhich medicine should i take\b",
    r"\bwhat medication should i take\b",
    r"\bwhat dosage should i take\b",
    r"\bhow much .* should i take\b",
    r"\bprescribe\b",
    r"\bshould i stop .* medication\b",
    r"\bshould i stop .* medicine\b",
]


MEDIUM_RISK_PATTERNS = [
    r"\bwhat should i do about\b",
    r"\bwhat can i do about\b",
    r"\bshould i worry about\b",
    r"\bwhy am i feeling\b",
]


def classify_medical_safety(text: str):

    text = text.lower().strip()

    # Critical / Emergency
    for pattern in EMERGENCY_PATTERNS:

        if re.search(pattern, text):

            return {
                "risk_level": "critical",
                "action": "emergency_redirect",
                "reason": "Potential medical emergency"
            }

    # High risk
    for pattern in HIGH_RISK_PATTERNS:

        if re.search(pattern, text):

            return {
                "risk_level": "high",
                "action": "redirect",
                "reason": "Personalized diagnosis, treatment, prescription, or dosage request"
            }

    # Medium risk
    for pattern in MEDIUM_RISK_PATTERNS:

        if re.search(pattern, text):

            return {
                "risk_level": "medium",
                "action": "cautious_answer",
                "reason": "Potentially personalized medical guidance"
            }

    # Low risk
    return {
        "risk_level": "low",
        "action": "allow",
        "reason": "General medical information"
    }

def get_safe_response(action):

    if action == "emergency_redirect":

        return (
            "This may be an emergency situation. "
            "Please seek immediate medical attention or contact "
            "your local emergency services. "
            "I can't safely manage an emergency through this chatbot."
        )

    if action == "redirect":

        return (
            "I can provide general medical information, "
            "but I can't provide a personalized diagnosis, "
            "prescription, or medication dosage. "
            "Please consult a qualified healthcare professional."
        )

    if action == "cautious_answer":

        return (
            "I can provide general medical information, "
            "but I can't determine the cause of your symptoms "
            "or provide a personalized treatment plan."
        )

    return None