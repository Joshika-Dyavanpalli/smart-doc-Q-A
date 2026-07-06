import numpy as np

from sentence_transformers import SentenceTransformer

# Load once
model = SentenceTransformer("all-MiniLM-L6-v2")


def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (
        np.linalg.norm(vec1) * np.linalg.norm(vec2)
    )


def retrieve_chunks(query, chunks, top_k=3):
    """
    Retrieves the most relevant chunks for a query.
    """

    query_embedding = model.encode(query)

    scores = []

    for chunk in chunks:
        score = cosine_similarity(
            query_embedding,
            chunk["embedding"]
        )
        scores.append(score)

    top_indices = np.argsort(scores)[::-1][:top_k]

    top_chunks = []

    for idx in top_indices:
        top_chunks.append(chunks[idx])

    return top_chunks