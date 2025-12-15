from fastapi import FastAPI
from pydantic import BaseModel
from backend.vectordb.retriever import Retriever
from backend.llm.llm import generate_answer
from backend.auth import router as auth_router

app = FastAPI()
retriever = Retriever()

# include auth router
app.include_router(auth_router)


class Question(BaseModel):
    question: str   


@app.post("/ask")
def ask_api(payload: Question):
    question = payload.question

    # 1. Retrieve top chunks
    results = retriever.search(question, top_k=3)
    context = "\n\n".join([r["text"] for r in results])

    # 2. Generate answer
    answer = generate_answer(question, context)

    return {"answer": answer, "sources": results}
