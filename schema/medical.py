from dataclasses import dataclass, field
from typing import Any, Optional
from enum import Enum
from pydantic import BaseModel, Field, ValidationError

@dataclass
class MedicalTest:
    """Simple dataclass replacement for pydantic.BaseModel."""

    name: str = field(metadata={"description": "Name of the medical test"})
    value: float = field(metadata={"description": "Numeric test result"})
    unit: str = field(metadata={"description": "Unit of measurement"})
    interpretation: str = field(metadata={"description": "Interpretation of the test result"})
    normal_range: tuple = field(metadata={"description": "Normal range of the test result"})
    status: str = field(metadata={"description": "Status of the test result"})

class Status(str, Enum):

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    UNKNOWN = "unknown"

class MedicalTest(BaseModel):

    name: str
    value: float
    unit: str
    status: Status

class MedicalReport(BaseModel):

    tests: list[MedicalTest]

test = MedicalTest(
    name="HbA1c",
    value=8.2,
    unit="%",
    interpretation="Based on the provided source...",
    normal_range=(4.0, 6.0),
    status="very_bad",
)

print(test)

test_dict = {"name": "HbA1c", "value": 8.2, "unit": "%", "status": "high"}

print(test_dict)

data = {
    "name": "HbA1c",
    "value": "wrong",
    "unit": "%"
}

print(data)

report = MedicalReport(
    tests=[
        {
            "name": "HbA1c",
            "value": 8.2,
            "unit": "%"
        },
        {
            "name": "Hemoglobin",
            "value": 13.5,
            "unit": "g/dL"
        }
    ]
)

print(report)

try:

    test = MedicalTest(**data)

    print("Valid output")
    print(test)

except ValidationError as e:

    print("Invalid output")
    print(e)

