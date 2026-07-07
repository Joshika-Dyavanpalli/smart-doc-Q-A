from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from backend.pipeline import process_document, answer_question

app = FastAPI()

# Store processed document data
document_chunks = None
document_index = None


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def home():
    return {"message": "Smart Document Q&A API is running"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global document_chunks, document_index

    # Process PDF and create FAISS index
    document_chunks, document_index = process_document(file.file)

    return {
        "message": "PDF processed successfully",
        "chunks": len(document_chunks)
    }


@app.post("/query")
def ask_question(request: QueryRequest):
    global document_chunks, document_index

    if document_chunks is None or document_index is None:
        return {
            "error": "Please upload a PDF first."
        }

    answer, sources = answer_question(
        request.query,
        document_chunks,
        document_index
    )

    return {
    "query": request.query,
    "answer": answer,
    "pages": list(set(chunk["page"] for chunk in sources))
}