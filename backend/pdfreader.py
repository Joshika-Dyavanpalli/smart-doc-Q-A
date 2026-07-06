from pypdf import PdfReader


def read_pdf(pdf_file):
    """
    Reads a PDF file and returns:
    1. Full document text
    2. Text page by page
    """

    reader = PdfReader(pdf_file)

    full_text = ""
    pages = []

    for page_num, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()

        if page_text:
            full_text += page_text + "\n"

            pages.append({
                "page": page_num,
                "text": page_text
            })
        if not full_text.strip():
          raise ValueError("No readable text found in the document.")

    return full_text, pages