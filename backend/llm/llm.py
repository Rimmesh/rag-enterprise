from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(question, context):
    if not context.strip():
        return "Information not found in the knowledge base."

    prompt = f"""
You are a STRICT enterprise RAG system.

CRITICAL RULES (MUST FOLLOW):
- Use ONLY the information explicitly present in CONTEXT.
- Do NOT rephrase using your own knowledge.
- Do NOT invent steps, phases, names, or structure.
- If the answer is not explicitly stated word-for-word in CONTEXT,
  respond EXACTLY with:
  "Information not found in the knowledge base."

TASK:
Extract and summarize ONLY what is written.

CONTEXT:
----------------
{context}
----------------

QUESTION:
{question}

ANSWER (only from context):
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a strict extractive RAG assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0
    )

    return response.choices[0].message.content.strip()
