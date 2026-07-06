def build_context(top_chunks):
    """
    Combines the retrieved chunks into a single context string.
    """

    return "\n\n".join(chunk["text"] for chunk in top_chunks)


def build_prompt(context, query):
    """
    Creates the prompt for the language model.
    """

    prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the information provided in the context.

Rules:
- Do NOT use outside knowledge.
- Do NOT guess.
- If the answer is not explicitly present in the context, reply exactly:
"Information not found in the document."

Context:
{context}

Question:
{query}

Answer:
"""

    return prompt