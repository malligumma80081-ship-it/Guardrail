import re


EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

PHONE_PATTERN = r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)"

PATIENT_ID_PATTERN = r"\bP\d{5,10}\b"

DOB_PATTERN = (
    r"\b(?:"
    r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
    r"|"
    r"\d{4}[/-]\d{1,2}[/-]\d{1,2}"
    r")\b"
)


def detect_pii(text: str):
    entities = []

    # Email
    for match in re.finditer(EMAIL_PATTERN, text):
        entities.append({
            "type": "EMAIL",
            "value": match.group(),
            "start": match.start(),
            "end": match.end()
        })

    # Phone
    for match in re.finditer(PHONE_PATTERN, text):
        entities.append({
            "type": "PHONE",
            "value": match.group(),
            "start": match.start(),
            "end": match.end()
        })

    # Patient ID
    for match in re.finditer(PATIENT_ID_PATTERN, text, re.IGNORECASE):
        entities.append({
            "type": "PATIENT_ID",
            "value": match.group(),
            "start": match.start(),
            "end": match.end()
        })

    # Date
    for match in re.finditer(DOB_PATTERN, text):
        entities.append({
            "type": "DATE",
            "value": match.group(),
            "start": match.start(),
            "end": match.end()
        })

    if entities:
        return {
            "contains_pii": True,
            "risk_level": "high",
            "action": "mask",
            "entities": entities
        }

    return {
        "contains_pii": False,
        "risk_level": "low",
        "action": "allow",
        "entities": []
    }

def mask_pii(text: str):

    masked_text = text

    masked_text = re.sub(
        EMAIL_PATTERN,
        "[EMAIL]",
        masked_text
    )

    masked_text = re.sub(
        PHONE_PATTERN,
        "[PHONE]",
        masked_text
    )

    masked_text = re.sub(
        PATIENT_ID_PATTERN,
        "[PATIENT_ID]",
        masked_text,
        flags=re.IGNORECASE
    )

    masked_text = re.sub(
        DOB_PATTERN,
        "[DATE]",
        masked_text
    )

    return masked_text    