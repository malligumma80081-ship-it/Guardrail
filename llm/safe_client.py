import ollama


def safe_llm_call(prompt):

    try:

        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response["message"]["content"]

        if not content.strip():

            return {
                "success": False,
                "content": None,
                "reason": "Empty LLM response"
            }

        return {
            "success": True,
            "content": content,
            "reason": None
        }

    except Exception as e:

        return {
            "success": False,
            "content": None,
            "reason": "LLM service failure"
        }