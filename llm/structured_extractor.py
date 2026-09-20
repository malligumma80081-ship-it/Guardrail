import json
from typing import Any

import ollama
from pydantic import ValidationError

from schemas.medical import MedicalReport


def extract_medical_report(text):
    prompt = f"""
Extract medical test results from the text.

Return ONLY valid JSON.

Required structure:

{{
    "tests": [
        {{
            "name": "string",
            "value": 0.0,
            "unit": "string",
            "reference_range": null
        }}
    ]
}}

Do not invent missing values.

INPUT:
{text}
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    raw_output = response["message"]["content"]
    return raw_output


def parse_medical_report(raw_output):
    data = json.loads(raw_output)
    report = MedicalReport(**data)
    return report


def validate_medical_output(raw_output):
    try:
        data = json.loads(raw_output)
        report = MedicalReport(**data)

        return {
            "valid": True,
            "data": report
        }

    except json.JSONDecodeError as e:
        return {
            "valid": False,
            "error_type": "invalid_json",
            "error": str(e)
        }

    except ValidationError as e:
        return {
            "valid": False,
            "error_type": "schema_validation",
            "error": str(e)
        }


def extract_with_retry(text):
    for attempt in range(3):
        raw_output = extract_medical_report(text)
        result = validate_medical_output(raw_output)

        if result["valid"]:
            return result

        print(
            f"Attempt {attempt + 1} failed: {result['error_type']}"
        )

    return {
        "valid": False,
        "error_type": "max_retries_exceeded"
    }


if __name__ == "__main__":
    report_text = "HbA1c: 8.2 %"

    result = extract_with_retry(report_text)

    if result["valid"]:
        print(result["data"])
    else:
        print(result["error_type"])