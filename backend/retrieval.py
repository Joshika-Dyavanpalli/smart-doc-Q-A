import numpy as np
from sentence_transformers import SentenceTransformer

# Load once
model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_chunks(query, chunks, index, top_k=3):
    """
    Retrieves the most relevant chunks using FAISS.
    """

    query_embedding = model.encode([query]).astype(np.float32)

    distances, indices = index.search(query_embedding, top_k)

    top_chunks = []

    for distance, idx in zip(distances[0], indices[0]):
        chunk = chunks[idx].copy()

        # Smaller L2 distance means more similar
        chunk["distance"] = float(distance)

        top_chunks.append(chunk)

    return top_chunks