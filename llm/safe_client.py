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


# import ollama


# MODEL = "llama3.2"


# def generate(prompt):

#     try:

#         response = ollama.chat(
#             model=MODEL,
#             messages=[
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ]
#         )

#         content = response["message"]["content"]

#         if not content.strip():

#             return {
#                 "success": False,
#                 "response": None,
#                 "reason": "Empty LLM response"
#             }

#         return {
#             "success": True,
#             "response": content,
#             "reason": None
#         }

#     except Exception as e:

#         return {
#             "success": False,
#             "response": None,
#             "reason": "LLM service unavailable"
#         }        