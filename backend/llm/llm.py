from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(question, context):
    prompt = f"""
You are an enterprise assistant. Answer based ONLY on the following context.

CONTEXT:
{context}

QUESTION:
{question}

If the answer is not in the documents, say: "Information not found in the knowledge base."
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt},
        ]
    )

    return response.choices[0].message.content
