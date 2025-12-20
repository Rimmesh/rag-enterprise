import os, sys

# Add project root to sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

from backend.vectordb.retriever import Retriever

retriever = Retriever()

query = "immatriculation"
results = retriever.search(query, top_k=3)

print("\n Query:", query)
print("\nTop results:\n")
for r in results:
    print("—", r["text"][:200], "...\n")
