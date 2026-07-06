def chunk_text(pages, chunk_size=1000, chunk_overlap=200):

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size.")

    chunks = []
    chunk_id = 1
    step = chunk_size - chunk_overlap

    for page in pages:

        page_num = page["page"]
        page_text = page["text"]

        start = 0

        while start < len(page_text):

            chunk = page_text[start:start + chunk_size]

            if chunk.strip():
                chunks.append({
                    "page": page_num,
                    "chunk_id": chunk_id,
                    "text": chunk
                })

            chunk_id += 1
            start += step

    return chunks