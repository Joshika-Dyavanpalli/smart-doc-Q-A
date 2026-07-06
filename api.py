from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from backend.pipeline import process_document, answer_question

app = FastAPI()

# temporary in-memory storage (for now)
document_chunks = None


# --------- 1. Upload PDF ----------
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global document_chunks

    pdf_bytes = await file.read()

    # process document
    document_chunks = process_document(pdf_bytes)

    return {"message": "PDF processed successfully", "chunks": len(document_chunks)}


# --------- 2. Ask Question ----------
class QueryRequest(BaseModel):
    query: str


@app.post("/query")
def ask_question(request: QueryRequest):

    global document_chunks

    if document_chunks is None:
        return {"error": "No document uploaded yet"}

    answer, sources = answer_question(request.query, document_chunks)

    return {
        "query": request.query,
        "answer": answer,
        "sources_used": len(sources)
    }