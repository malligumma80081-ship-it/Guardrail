def llm_failure_response():

    return (
        "I'm unable to process this request right now "
        "because the medical information service is temporarily "
        "unavailable. Please try again later."
    )


def retrieval_failure_response():

    return (
        "I couldn't retrieve the required information from "
        "the trusted medical sources. I don't have enough "
        "verified information to answer this question safely."
    )


def validation_failure_response():

    return (
        "I couldn't safely validate the generated response. "
        "Please try again later."
    )


FAILURE_POLICY = {

    "pii_guard": "fail_closed",

    "injection_guard": "fail_closed",

    "medical_safety": "fail_closed",

    "retriever": "fail_closed",

    "llm": "fallback",

    "output_guard": "fail_closed",

    "analytics": "fail_open"
}