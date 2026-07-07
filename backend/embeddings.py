import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the model once when the module is imported
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(chunks):
    """
    Generates embeddings for each chunk and stores them
    inside the chunk dictionary.
    """

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(texts)

    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding

    return chunks


def build_faiss_index(chunks):
    """
    Builds a FAISS index from the generated embeddings.
    """

    embeddings = np.array(
        [chunk["embedding"] for chunk in chunks],
        dtype=np.float32
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index