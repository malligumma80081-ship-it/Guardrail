import pickle
import faiss

from sentence_transformers import SentenceTransformer


INDEX_PATH = "vector_store/faiss_index/medical.index"
DOCUMENTS_PATH = "vector_store/faiss_index/documents.pkl"


model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

index = faiss.read_index(INDEX_PATH)

with open(DOCUMENTS_PATH, "rb") as f:
    documents = pickle.load(f)


def retrieve(query, top_k=2):

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    ).astype("float32")

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for distance, index_id in zip(
        distances[0],
        indices[0]
    ):

        if index_id == -1:
            continue

        results.append({
            "source": documents[index_id]["source"],
            "text": documents[index_id]["text"],
            "distance": float(distance)
        })

    return results

def safe_retrieve(query, top_k=3):

    try:

        results = retrieve(query, top_k)

        if not results:

            return {
                "success": False,
                "results": [],
                "reason": "No documents found"
            }

        return {
            "success": True,
            "results": results,
            "reason": None
        }

    except Exception as e:

        return {
            "success": False,
            "results": [],
            "reason": "Retriever failure"
        }