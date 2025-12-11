import os
import pickle
import faiss
import numpy as np
from backend.vectordb.embedder import embed_text

# GO TO PROJECT ROOT
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BACKEND_DIR)

FAISS_PATH = os.path.join(ROOT_DIR, "data", "faiss", "index.faiss")
VECTORS_PATH = os.path.join(ROOT_DIR, "data", "faiss", "vectors.pkl")
META_PATH   = os.path.join(ROOT_DIR, "data", "faiss", "metadata.pkl")

class Retriever:
    def __init__(self):
        print("Loading FAISS index...")
        self.index = faiss.read_index(FAISS_PATH)

        print("Loading metadata...")
        with open(META_PATH, "rb") as f:
            self.metadata = pickle.load(f)

    def search(self, query, top_k=5):
        query_vec = embed_text([query])
        query_vec = np.array(query_vec).astype("float32")

        distances, indices = self.index.search(query_vec, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])

        return results
