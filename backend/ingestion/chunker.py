import os
from langchain_text_splitters import RecursiveCharacterTextSplitter


TEXT_INPUT_PATH = "data/text"
CHUNKS_OUTPUT_PATH = "data/chunks"

os.makedirs(CHUNKS_OUTPUT_PATH, exist_ok=True)

def chunk_documents():
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    for filename in os.listdir(TEXT_INPUT_PATH):
        if filename.endswith(".txt"):
            file_path = os.path.join(TEXT_INPUT_PATH, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            chunks = splitter.split_text(text)

            output_file = os.path.join(
                CHUNKS_OUTPUT_PATH,
                filename.replace(".txt", "_chunks.txt")
            )

            with open(output_file, "w", encoding="utf-8") as f:
                for chunk in chunks:
                    f.write(chunk + "\n---\n")

            print(f"Chunked: {filename}")

if __name__ == "__main__":
    chunk_documents()
