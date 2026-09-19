from rag.retriever import retrieve


query = "What does HbA1c measure?"

results = retrieve(query, top_k=2)


for result in results:

    print("\nSOURCE:", result["source"])
    print("DISTANCE:", result["distance"])
    print("TEXT:")
    print(result["text"])