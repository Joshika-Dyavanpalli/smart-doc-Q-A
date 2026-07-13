from .pdfreader import read_pdf
from .chunking import chunk_text
from .embeddings import generate_embeddings, build_faiss_index
from .retrieval import retrieve_chunks
from .prompt import build_context, build_prompt
from .llm import get_answer


def process_document(pdf_file):
    """
    Reads the PDF, chunks it, generates embeddings,
    and builds the FAISS index.
    """

    full_text, pages = read_pdf(pdf_file)

    chunks = chunk_text(pages)

    # Empty PDF handling
    if not chunks:
        return None, None

    chunks = generate_embeddings(chunks)

    index = build_faiss_index(chunks)

    return chunks, index


def process_text(text):
    """
    Processes pasted text.
    """

    if not text.strip():
        return None, None

    pages = [
    {
        "page": 1,
        "text": text
    }
    ]

    chunks = chunk_text(pages)

    if not chunks:
        return None, None

    chunks = generate_embeddings(chunks)

    index = build_faiss_index(chunks)

    return chunks, index


def answer_question(query, chunks, index):
    """
    Answers a question using the processed document.
    """

    top_chunks = retrieve_chunks(query, chunks, index)

    # Retrieval threshold
    if top_chunks is None:
        return "Information not found in the document.", []

    context = build_context(top_chunks)

    prompt = build_prompt(context, query)

    answer = get_answer(prompt)

    return answer, top_chunks