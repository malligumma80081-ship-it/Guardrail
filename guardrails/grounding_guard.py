def validate_grounding(answer, context):

    if not answer.strip():
        return {
            "grounded": False,
            "action": "block",
            "reason": "Empty response"
        }

    if "I don't have enough information" in answer:
        return {
            "grounded": True,
            "action": "allow",
            "reason": "Model abstained because context was insufficient"
        }

    if not context.strip():
        return {
            "grounded": False,
            "action": "block",
            "reason": "No grounding context available"
        }

    return {
        "grounded": True,
        "action": "allow",
        "reason": "Basic context validation passed"
    }