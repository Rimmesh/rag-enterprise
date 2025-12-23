import os
import pickle
import numpy as np
import faiss
from backend.vectordb.embedder import embed_text

CHUNKS_PATH = "data/chunks"
FAISS_DIR = "data/faiss"
FAISS_PATH = os.path.join(FAISS_DIR, "index.faiss")
VECTORS_PATH = os.path.join(FAISS_DIR, "vectors.pkl")
META_PATH = os.path.join(FAISS_DIR, "metadata.pkl")

os.makedirs(FAISS_DIR, exist_ok=True)


def build_faiss():
    all_chunks = []
    metadata = []

    print("📦 Collecting chunks...")

    for filename in os.listdir(CHUNKS_PATH):
        if not filename.endswith("_chunks.txt"):
            continue

        filepath = os.path.join(CHUNKS_PATH, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = text.split("\n---\n")

        source_name = filename.replace("_chunks.txt", "")

        for i, chunk in enumerate(chunks):
            cleaned = chunk.strip()
            if not cleaned:
                continue

            all_chunks.append(cleaned)

            metadata.append({
                "text": cleaned,
                "source": source_name,
                "page": i + 1
            })

    print(f"✅ Total chunks: {len(all_chunks)}")

    if not all_chunks:
        raise RuntimeError("❌ No chunks found. Check ingestion pipeline.")

    print("🧠 Embedding chunks...")
    vectors = np.array(embed_text(all_chunks)).astype("float32")

    print("📐 Building FAISS index...")
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    faiss.write_index(index, FAISS_PATH)
    pickle.dump(vectors, open(VECTORS_PATH, "wb"))
    pickle.dump(metadata, open(META_PATH, "wb"))

    print("🚀 FAISS index rebuilt successfully")
    print(f"→ {FAISS_PATH}")
    print(f"→ {META_PATH}")


if __name__ == "__main__":
    build_faiss()
