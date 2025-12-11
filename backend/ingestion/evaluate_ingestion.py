import os

TEXT_INPUT_PATH = "data/text"
CHUNKS_PATH = "data/chunks"

# Customize keywords here if needed
KEYWORDS = ["procédure", "facturation", "diagramme", "politique", "client"]


def load_all_text(path):
    """Concatenate all .txt files in a directory into one big string."""
    full = ""
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            with open(os.path.join(path, filename), "r", encoding="utf-8") as f:
                full += f.read() + "\n"
    return full


def check_keyword_presence(path, label):
    """Check if each keyword appears at least once in the text directory."""
    print(f"\n Searching keywords in {label}:")
    dir_text = load_all_text(path).lower()

    for kw in KEYWORDS:
        if kw.lower() in dir_text:
            print(f" - '{kw}': found")
        else:
            print(f" - '{kw}': NOT found")


def evaluate_coverage():
    """Compare total size of extracted text vs chunked text."""
    print("\n📏 Coverage Evaluation")
    original_text = load_all_text(TEXT_INPUT_PATH)
    chunks_text = load_all_text(CHUNKS_PATH)

    len_original = len(original_text)
    len_chunks = len(chunks_text)

    print(f"Original text length : {len_original}")
    print(f"Chunks text length   : {len_chunks}")

    if len_original == 0:
        print("No original text found in data/text. Check extraction.")
        return

    coverage = len_chunks / len_original
    print(f"Coverage ratio       : {coverage:.2f}")

    if coverage < 0.8:
        print("Warning: significant loss of text between extraction and chunking.")
    elif coverage > 1.3:
        print("Warning: chunks contain a LOT more text than original (too much overlap?).")
    else:
        print("Chunking coverage looks OK globally.")


if __name__ == "__main__":
    print("\n====================== INGESTION PIPELINE EVALUATION ======================")

    # 1) Keyword test
    check_keyword_presence(TEXT_INPUT_PATH, "EXTRACTED TEXT (data/text)")
    check_keyword_presence(CHUNKS_PATH, "CHUNKS (data/chunks)")

    # 2) Coverage test
    evaluate_coverage()

    print("\n==========================================================================\n")
