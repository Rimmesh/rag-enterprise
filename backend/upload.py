from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import os
import shutil

from backend.ingestion.document_loader import extract_single_file
from backend.ingestion.chunker import chunk_documents
from backend.vectordb.build_faiss import build_faiss
from backend.auth import get_current_user

router = APIRouter(prefix="/upload", tags=["upload"])

RAW_DIR = os.path.join("data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

@router.post("/")
def upload_document(
    file: UploadFile = File(...),
    user=Depends(get_current_user),
):
    # 🔐 Admin-only
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    if not file.filename.lower().endswith((".pdf", ".txt", ".docx", ".pptx")):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    file_path = os.path.join(RAW_DIR, file.filename)

    # 1️⃣ Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2️⃣ Extract text → data/text
    extract_single_file(file_path, file.filename)

    # 3️⃣ Chunk documents (UNCHANGED chunker)
    chunk_documents()

    # 4️⃣ Rebuild FAISS index
    build_faiss()

    return {
        "status": "success",
        "filename": file.filename,
        "message": "Document indexed successfully",
        "next_step": "Ask a question explicitly related to this document"
    }
