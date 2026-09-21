from pydantic import BaseModel, Field


class MedicalResponse(BaseModel):

    answer: str

    risk_level: str

    grounded: bool

    sources: list[str] = Field(default_factory=list)

def validate_structured_output(data):

    try:

        result = MedicalResponse.model_validate(data)

        return {
            "success": True,
            "data": result
        }

    except Exception:

        return {
            "success": False,
            "data": None
        }   