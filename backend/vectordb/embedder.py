from sentence_transformers import SentenceTransformer

# Load only once
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed_text(text_list):
    """
    Takes a list of chunks -> returns list of embeddings
    """
    embeddings = model.encode(text_list, convert_to_numpy=True)
    return embeddings
