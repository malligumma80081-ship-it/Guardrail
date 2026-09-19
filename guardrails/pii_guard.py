import re

PII_PATTERNS = {
    "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "PHONE": r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)",
    "PATIENT_ID": r"\bP\d{5,10}\b",
    "DATE": (
        r"\b(?:"
        r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
        r"|"
        r"\d{4}[/-]\d{1,2}[/-]\d{1,2}"
        r")\b"
    ),
}

MASK_VALUES = {
    "EMAIL": "[EMAIL]",
    "PHONE": "[PHONE]",
    "PATIENT_ID": "[PATIENT_ID]",
    "DATE": "[DATE]",
}

PII_POLICY = {
    "EMAIL": "mask",
    "PHONE": "mask",
    "PATIENT_ID": "mask",
    "DATE": "mask",
    "GOVERNMENT_ID": "redact",
    "BANK_ACCOUNT": "block",
}


def get_action(entity_type):
    return PII_POLICY.get(entity_type, "mask")


def detect_pii(text: str):
    entities = []

    for entity_type, pattern in PII_PATTERNS.items():
        flags = re.IGNORECASE if entity_type == "PATIENT_ID" else 0
        for match in re.finditer(pattern, text, flags):
            entities.append({
                "type": entity_type,
                "value": match.group(),
                "start": match.start(),
                "end": match.end()
            })

    if not entities:
        return {
            "contains_pii": False,
            "risk_level": "low",
            "action": "allow",
            "entities": []
        }

    return {
        "contains_pii": True,
        "risk_level": "high",
        "action": get_action(entities[0]["type"]),
        "entities": entities
    }


def mask_pii(text: str):
    masked_text = text

    for entity_type, pattern in PII_PATTERNS.items():
        flags = re.IGNORECASE if entity_type == "PATIENT_ID" else 0
        masked_text = re.sub(pattern, MASK_VALUES[entity_type], masked_text, flags=flags)

    return masked_text


def redact_pii(text: str):
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", "[EMAIL]", text)
    text = re.sub(r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)", "[PHONE]", text)
    text = re.sub(r"\bP\d{5,10}\b", "[PATIENT_ID]", text, flags=re.IGNORECASE)
    text = re.sub(
        r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2})\b",
        "[DATE]",
        text
    )
    return text


def detect_unsafe_output(text: str):
    unsafe_reasons = []

    if re.search(r"\b(?:diagnos(?:e|is)|you definitely have|you have diabetes|you have [a-z]+)\b", text, re.IGNORECASE):
        unsafe_reasons.append("diagnosis")

    if re.search(r"\b(?:increase.*dose|take.*insulin|prescrib|dosage|prescription)\b", text, re.IGNORECASE):
        unsafe_reasons.append("unsafe")

    if re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", text):
        unsafe_reasons.append("pii")

    if not unsafe_reasons:
        return {"safe": True, "issues": [], "action": "allow"}

    return {"safe": False, "issues": unsafe_reasons, "action": "block"}


def validate_and_sanitize_output(text: str):
    result = detect_unsafe_output(text)

    if result["action"] == "allow":
        return {"action": "allow", "text": text}

    # sanitize PII in output
    sanitized = redact_pii(text)

    if "unsafe" in result["issues"] or "diagnosis" in result["issues"]:
        return {
            "action": "block",
            "text": "I can't provide diagnosis or treatment instructions. Please consult a qualified healthcare professional."
        }

    if "pii" in result["issues"]:
        return {"action": "mask", "text": sanitized}

    return {"action": "block", "text": sanitized}