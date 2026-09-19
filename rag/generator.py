import ollama

from rag.retriever import retrieve


def generate_grounded_answer(query):

    results = retrieve(query, top_k=2)

    if not results:
        return {
            "answer": (
                "I don't have enough information in the "
                "provided medical sources to answer this question."
            ),
            "sources": []
        }

    context_parts = []

    for result in results:

        context_parts.append(
            f"[Source: {result['source']}]\n"
            f"{result['text']}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are a medical information assistant.

Answer ONLY using the information provided in CONTEXT.

Do not invent medical facts.

If the answer is not supported by CONTEXT,
say:

"I don't have enough information in the provided sources."

Do not provide personalized diagnosis, prescriptions,
or medication dosage instructions.

CONTEXT:
{context}

QUESTION:
{query}

Answer with the relevant source names.
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

    return {
        "answer": response["message"]["content"],
        "sources": [
            result["source"]
            for result in results
        ]
    }