from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from backend.pipeline import (
    process_document,
    process_text,
    answer_question,
)

app = FastAPI()

# Store processed document data
document_chunks = None
document_index = None


class QueryRequest(BaseModel):
    query: str


class TextRequest(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "Smart Document Q&A API is running"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global document_chunks, document_index

    document_chunks, document_index = process_document(file.file)

    if document_chunks is None:
        return {
            "error": "This document appears to have no readable text."
        }

    return {
        "message": "PDF processed successfully",
        "chunks": len(document_chunks)
    }


@app.post("/paste-text")
def paste_text(request: TextRequest):
    global document_chunks, document_index

    document_chunks, document_index = process_text(request.text)

    if document_chunks is None:
        raise HTTPException(
            status_code=400,
            detail="Please enter some text."
        )

    return {
        "message": "Text processed successfully",
        "chunks": len(document_chunks)
    }


@app.post("/query")
def ask_question(request: QueryRequest):
    global document_chunks, document_index

    if document_chunks is None or document_index is None:
        return {
            "error": "Please upload a PDF or paste text first."
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