from pathlib import Path

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.rag.memory import (get_history,add_message)

from app.rag.loader import load_pdf
from app.rag.chunker import split_text
from app.rag.ingest import ingest_chunks
from app.rag.chain import (ask_question,stream_question)
from fastapi.responses import StreamingResponse
from app.rag.vectorstore import get_vectorstore


app = FastAPI()

# ----------------------------------
# CORS
# ----------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------
# Upload Directory
# ----------------------------------

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# ----------------------------------
# Request Models
# ----------------------------------

class ChatRequest(BaseModel):
    session_id: str
    message: str

# ----------------------------------
# Health Check APIs
# ----------------------------------

@app.get("/")
def home():
    return {
        "message": "RAG Backend Running"
    }


@app.get("/test")
def test():
    return {
        "response": "Hello from Backend"
    }

# ----------------------------------
# Upload + Ingest PDF
# ----------------------------------

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # Allow only PDFs
    if not file.filename.endswith(".pdf"):
        return {
            "error": "Only PDF files are allowed"
        }

    file_path = UPLOAD_DIR / file.filename

    # Save PDF
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Load PDF
    text = load_pdf(str(file_path))

    # Create Chunks
    chunks = split_text(text)

    # Store in Vector DB
    chunks_stored = ingest_chunks(
        chunks,
        file.filename
    )

    return {
        "message": "PDF uploaded and indexed successfully",
        "filename": file.filename,
        "chunks_stored": chunks_stored
    }

# ----------------------------------
# List Uploaded PDFs
# ----------------------------------

@app.get("/documents")
def get_documents():

    vectorstore = get_vectorstore()
    data = vectorstore.get()

    files = {}

    for meta in data["metadatas"]:

        if meta is None:
            continue

        source = meta.get("source")

        if not source:
            continue

        if source not in files:
            files[source] = {
                "filename": source,
                "chunks": 0
            }

        files[source]["chunks"] += 1

    return list(files.values())




# ----------------------------------
# Delete PDF
# ----------------------------------

@app.delete("/documents/{filename}")
def delete_document(filename: str):

    vectorstore = get_vectorstore()

    data = vectorstore.get()

    ids_to_delete = []

    for idx, meta in enumerate(data["metadatas"]):

        if meta.get("source") == filename:
            ids_to_delete.append(
                data["ids"][idx]
            )

    if ids_to_delete:
        vectorstore.delete(ids=ids_to_delete)

    return {
        "message": f"{filename} deleted"
    }
# ----------------------------------
# Chat Test Endpoint
# ----------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    return {
        "answer": f"You said: {request.message}"
    }

# ----------------------------------
# RAG Query Endpoint
# ----------------------------------

@app.post("/query")
async def query(request: ChatRequest):

    response = ask_question(
        question=request.message,
        session_id=request.session_id
    )

    return response

@app.post("/query-stream")
async def query_stream(
    request: ChatRequest
):

    return StreamingResponse(
        stream_question(
            question=request.message,
            session_id=request.session_id
        ),
        media_type="text/plain"
    )