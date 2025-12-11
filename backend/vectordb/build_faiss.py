import os
import pickle
import numpy as np
import faiss
from embedder import embed_text

CHUNKS_PATH = "data/chunks"
FAISS_PATH = "data/faiss/index.faiss"
VECTORS_PATH = "data/faiss/vectors.pkl"
META_PATH = "data/faiss/metadata.pkl"


def build_faiss():
    all_chunks = []
    metadata = []

    print("Collecting chunks...")

    # Loop through chunked files
    for filename in os.listdir(CHUNKS_PATH):
        if filename.endswith("_chunks.txt"):
            filepath = os.path.join(CHUNKS_PATH, filename)

            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

            # Split by separator
            chunks = text.split("\n---\n")

            for i, chunk in enumerate(chunks):
                cleaned = chunk.strip()
                if cleaned == "":
                    continue

                all_chunks.append(cleaned)

                metadata.append({
                    "source_file": filename.replace("_chunks.txt", ".txt"),
                    "chunk_id": f"{filename}_chunk_{i}",
                    "index": len(metadata),
                    "text": cleaned  # ← VERY IMPORTANT
                })

    print(f"Total chunks collected: {len(all_chunks)}")

    # Embed all chunks
    print("Embedding chunks...")
    vectors = embed_text(all_chunks).astype("float32")

    # Build FAISS index
    print("Building FAISS index...")
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    # Save index + metadata + vectors
    faiss.write_index(index, FAISS_PATH)
    pickle.dump(vectors, open(VECTORS_PATH, "wb"))
    pickle.dump(metadata, open(META_PATH, "wb"))

    print("FAISS index built successfully!")
    print(f"→ Saved to: {FAISS_PATH}")


if __name__ == "__main__":
    build_faiss()
