import numpy as np
from sentence_transformers import SentenceTransformer
print("Retrieval module loaded")
# Load once
model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_chunks(query, chunks, index, top_k=3, distance_threshold=1.8):
    print("retrieve_chunks() called")
    """
    Retrieves the most relevant chunks using FAISS.
    Returns None if no relevant chunk is found.
    """

    query_embedding = model.encode([query]).astype(np.float32)

    distances, indices = index.search(query_embedding, top_k)

    print("Distances:", distances)

    # If the closest chunk is still too far away,
    # the query is probably unrelated to the document.
    if distances[0][0] > distance_threshold:
        return None

    top_chunks = []

    for distance, idx in zip(distances[0], indices[0]):

        chunk = chunks[idx].copy()
        chunk["distance"] = float(distance)

        top_chunks.append(chunk)

    return top_chunks