from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from backend.vectordb.retriever import Retriever
from backend.llm.llm import generate_answer
from backend.auth import router as auth_router, get_current_user, UserOut
from backend.upload import router as upload_router
from backend.chat_history import add_message, get_history

# ---------------- APP ----------------
app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- CORE OBJECTS ----------------
def get_retriever():
    return Retriever()


# ---------------- ROUTERS ----------------
app.include_router(auth_router)
app.include_router(upload_router)

# ---------------- MODELS ----------------
class Question(BaseModel):
    question: str

# ---------------- ENDPOINTS ----------------
@app.post("/ask")
def ask_api(
    payload: Question,
    current_user: UserOut = Depends(get_current_user)
):
    question = payload.question

    # Save user question
    add_message(current_user.email, "user", question)

    # Retrieve context
    results = get_retriever().search(question, top_k=3)
    context = "\n\n".join([r["text"] for r in results])

    # Generate answer
    answer = generate_answer(question, context)

    # Save assistant answer
    add_message(current_user.email, "assistant", answer)

    return {
        "answer": answer,
        "sources": results
    }


@app.get("/history")
def read_history(current_user: UserOut = Depends(get_current_user)):
    return get_history(current_user.email)
