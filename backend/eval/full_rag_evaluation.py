# ================= STANDARD LIBS =================
import os
import json
import time

# ================= SCIENTIFIC LIBS =================
import numpy as np
import matplotlib.pyplot as plt

# ================= NLP / RAG =================
from sentence_transformers import SentenceTransformer, util

# ================= PROJECT IMPORTS =================
from backend.vectordb.retriever import Retriever
from backend.llm.llm import generate_answer


# ==================================================
# PATH CONFIGURATION (ROBUST & PROFESSIONAL)
# ==================================================
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

EVAL_FILE = os.path.join(BASE_DIR, "backend", "eval", "rag_eval.json")

TOP_K = 3


# ==================================================
# INITIALIZATION
# ==================================================
print("🔹 Initializing retriever...")
retriever = Retriever()

print("🔹 Loading embedding model...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")


# ==================================================
# HELPER FUNCTIONS
# ==================================================
def semantic_similarity(a: str, b: str) -> float:
    """Compute cosine similarity between two texts."""
    emb_a = embedder.encode(a, convert_to_tensor=True)
    emb_b = embedder.encode(b, convert_to_tensor=True)
    return float(util.cos_sim(emb_a, emb_b))


def is_grounded(answer: str, context: str) -> bool:
    """Simple groundedness check (string inclusion)."""
    return answer.strip().lower() in context.lower()


# ==================================================
# EVALUATION PIPELINE
# ==================================================
def run_evaluation():
    if not os.path.exists(EVAL_FILE):
        raise FileNotFoundError(f"Evaluation file not found: {EVAL_FILE}")

    with open(EVAL_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    recall_hits = 0
    mrr_total = 0.0
    similarities = []
    grounded_count = 0
    latencies = []

    print(f"🔹 Running evaluation on {len(data)} queries...\n")

    for item in data:
        question = item["question"]
        expected_doc = item["source_doc"]
        reference_answer = item["answer"]

        start_time = time.time()

        # ---------- RETRIEVAL ----------
        retrieved_docs = retriever.search(question, top_k=TOP_K)

        context = "\n".join([doc["text"] for doc in retrieved_docs])

        # ---------- GENERATION ----------
        answer = generate_answer(question, context)

        end_time = time.time()
        latencies.append(end_time - start_time)

        # ---------- RETRIEVAL METRICS ----------
        found = False
        for rank, doc in enumerate(retrieved_docs, start=1):
            if expected_doc.lower() in doc["source"].lower():
                recall_hits += 1
                mrr_total += 1 / rank
                found = True
                break

        if not found:
            mrr_total += 0

        # ---------- ANSWER METRICS ----------
        if answer.strip():
            sim = semantic_similarity(answer, reference_answer)
            similarities.append(sim)

            if is_grounded(answer, context):
                grounded_count += 1

    results = {
        "Recall@K": recall_hits / len(data),
        "MRR": mrr_total / len(data),
        "Avg Semantic Similarity": float(np.mean(similarities)),
        "Groundedness Rate": grounded_count / len(data),
        "Avg Latency (s)": float(np.mean(latencies)),
    }

    return results, similarities, latencies


# ==================================================
# VISUALIZATION
# ==================================================
def plot_results(similarities, latencies):
    plt.figure()
    plt.hist(similarities, bins=10)
    plt.title("Semantic Similarity Distribution")
    plt.xlabel("Cosine Similarity")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

    plt.figure()
    plt.hist(latencies, bins=10)
    plt.title("Response Latency Distribution")
    plt.xlabel("Seconds")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()


# ==================================================
# MAIN
# ==================================================
if __name__ == "__main__":
    metrics, sims, lats = run_evaluation()

    print("\n===== RAG EVALUATION RESULTS =====")
    for metric, value in metrics.items():
        print(f"{metric}: {value:.3f}")

    plot_results(sims, lats)
