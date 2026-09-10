from guardrails.input_guard import check_input
from llm.ollama_client import ask_llama


def medical_chatbot(user_input):

    # Step 1: Input Guardrail
    guardrail_result = check_input(user_input)

    if not guardrail_result["allowed"]:

        return (
            "I can't help with that request. "
            "I can provide general medical information "
            "and educational guidance."
        )

    # Step 2: Send safe request to Llama
    prompt = f"""
You are a medical education assistant.

You provide general health information.

You must not:
- diagnose a patient
- prescribe medication
- provide personalized dosage instructions
- claim to replace a healthcare professional

User question:

{user_input}

Provide a clear educational answer.
"""

    response = ask_llama(prompt)

    # If the Ollama client returned an error string, provide a safe local fallback
    if isinstance(response, str) and response.startswith("Error:"):
        return _local_fallback(user_input)

    return response


def _local_fallback(user_input: str) -> str:
    """Return a short, general educational answer for a few common topics.

    This fallback is intentionally conservative and non-diagnostic.
    Expand the mapping as needed.
    """
    q = user_input.lower()

    if "hypert" in q or "high blood pressure" in q:
        return (
            "Hypertension (high blood pressure) means the force of blood against the "
            "artery walls is consistently too high. Lifestyle changes like reducing "
            "salt intake, maintaining a healthy weight, exercising, and limiting alcohol "
            "can help. Follow-up with a healthcare professional for diagnosis and treatment."
        )

    if "diabet" in q:
        return (
            "Diabetes is a condition where the body cannot properly regulate blood sugar. "
            "Management includes diet, exercise, blood glucose monitoring, and sometimes "
            "medication. For personalized care, consult a healthcare professional."
        )

    # Generic conservative fallback
    return (
        "Sorry — the language model backend is currently unavailable. "
        "I can provide general educational information but cannot diagnose or treat. "
        "Please rephrase your question or consult a healthcare professional for personal advice."
    )


if __name__ == "__main__":

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            break

        response = medical_chatbot(user_input)

        print("\nAssistant:", response)