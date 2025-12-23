from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(question, context):
    if not context.strip():
        return "Information not found in the knowledge base."

    prompt = f"""
You are a strict enterprise RAG assistant.

RULES:
- Answer ONLY using the provided context.
- If the answer is not explicitly stated, reply exactly:
  "Information not found in the knowledge base."
- Do NOT use external knowledge.
- Do NOT make assumptions.

CONTEXT:
{context}

QUESTION:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a retrieval-grounded assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0
    )

    return response.choices[0].message.content.strip()

