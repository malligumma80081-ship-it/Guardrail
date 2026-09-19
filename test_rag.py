from rag.generator import generate_grounded_answer

query = "What does HbA1c measure?"

result = generate_grounded_answer(query)

print("\nANSWER:")
print(result["answer"])

print("\nSOURCES:")
for source in result["sources"]:
    print("-", source)