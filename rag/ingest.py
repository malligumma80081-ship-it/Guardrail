from pathlib import Path
import pickle

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


DOCS_DIR = Path("data/medical_docs")
INDEX_DIR = Path("vector_store/faiss_index")

INDEX_DIR.mkdir(parents=True, exist_ok=True)

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


documents = []

for file_path in DOCS_DIR.glob("*.txt"):

    text = file_path.read_text(encoding="utf-8")

    documents.append({
        "text": text,
        "source": file_path.name
    })


texts = [doc["text"] for doc in documents]

embeddings = embedding_model.encode(
    texts,
    convert_to_numpy=True
)

embeddings = embeddings.astype("float32")

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)


faiss.write_index(
    index,
    str(INDEX_DIR / "medical.index")
)


with open(
    INDEX_DIR / "documents.pkl",
    "wb"
) as f:

    pickle.dump(documents, f)


print(f"Indexed {len(documents)} documents.")