import logging
import uuid

from guardrails.input_guard import validate_input
from guardrails.injection_guard import detect_prompt_injection
from guardrails.pii_guard import detect_pii, mask_pii
from guardrails.medical_safety import classify_medical_safety
from guardrails.output_guard import validate_output

from rag.retriever import retrieve
from rag.generator import generate_answer

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
)

TEST_CASES = [
    "A CBC is a blood test used to evaluate blood cells.",
    "What are the side effects of this medication?",
    "What is the dosage tomorrow?",
]


def process_request(user_input):
    request_id = str(uuid.uuid4())
    logging.info("Request started: %s", request_id)

    input_result = validate_input(user_input)
    if not input_result["allowed"]:
        return {
            "request_id": request_id,
            "status": "blocked",
            "response": input_result["reason"],
        }

    injection_result = detect_prompt_injection(user_input)
    if injection_result["is_injection"]:
        logging.warning("Injection blocked: %s", request_id)
        return {
            "request_id": request_id,
            "status": "blocked",
            "response": "I can't process that request because it contains an unsafe instruction.",
        }

    pii_entities = detect_pii(user_input)
    safe_input = mask_pii(user_input)
    safety_result = classify_medical_safety(safe_input)

    if safety_result["risk_level"] == "critical":
        return {
            "request_id": request_id,
            "status": "redirected",
            "response": (
                "This may describe a medical emergency. "
                "Please seek immediate professional medical attention or contact your local emergency service."
            ),
        }

    if safety_result["risk_level"] == "high":
        return {
            "request_id": request_id,
            "status": "redirected",
            "response": (
                "I can provide general medical information, "
                "but I can't diagnose, prescribe treatment, "
                "or recommend medication dosage. Please consult a qualified healthcare professional."
            ),
        }

    contexts = retrieve(safe_input, top_k=3)
    result = generate_answer(safe_input, contexts)

    if not result["success"]:
        return {
            "request_id": request_id,
            "status": "fallback",
            "response": result["answer"],
        }

    output_result = validate_output(result["answer"])
    if not output_result["allowed"]:
        logging.warning("Unsafe output blocked: %s", request_id)
        return {
            "request_id": request_id,
            "status": "blocked",
            "response": "I couldn't safely validate the generated medical response.",
        }

    logging.info("Request completed: %s", request_id)
    return {
        "request_id": request_id,
        "status": "success",
        "response": result["answer"],
        "sources": result["sources"],
        "pii_detected": len(pii_entities) > 0,
    }


if __name__ == "__main__":
    question = input("Ask a medical information question: ")
    result = process_request(question)
    print("\nResult:\n")
    print(result)
