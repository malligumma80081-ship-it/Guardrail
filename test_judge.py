from evaluation.judge import judge_answer

question = "What does HbA1c measure?"

context = """
HbA1c is a blood test that reflects average blood
glucose levels over approximately the previous 2–3 months.
"""

answer = """
HbA1c reflects average blood glucose levels over
approximately the previous 2–3 months.
"""

result = judge_answer(question, context, answer)
print(result)