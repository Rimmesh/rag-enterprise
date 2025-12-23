from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from backend.vectordb.retriever import Retriever
from backend.llm.llm import generate_answer
from backend.auth import router as auth_router
from backend.upload import router as upload_router

# ---------------- APP ----------------
app = FastAPI()

# ---------------- CORS (REQUIRED FOR REACT) ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # React (Vite)
    ],
    allow_credentials=True,
    allow_methods=["*"],        # MUST allow OPTIONS
    allow_headers=["*"],
)

# ---------------- CORE OBJECTS ----------------
retriever = Retriever()

# ---------------- ROUTERS ----------------
app.include_router(auth_router)
app.include_router(upload_router)

# ---------------- MODELS ----------------
class Question(BaseModel):
    question: str

# ---------------- ENDPOINTS ----------------
@app.post("/ask")
def ask_api(payload: Question):
    question = payload.question

    # 1. Retrieve top chunks
    results = retriever.search(question, top_k=3)
    context = "\n\n".join([r["text"] for r in results])

    # 2. Generate answer
    answer = generate_answer(question, context)

    return {
        "answer": answer,
        "sources": results
    }
