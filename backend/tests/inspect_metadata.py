import pickle

with open("data/faiss/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

print("Total entries:", len(metadata))
print("\nFirst entry keys:", metadata[0].keys())
print("\nPreview:")
print({k: str(v)[:200] for k, v in metadata[0].items()})
