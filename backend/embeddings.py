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