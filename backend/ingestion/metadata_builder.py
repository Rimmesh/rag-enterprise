import os
import json

TEXT_INPUT_PATH = "data/text"
CHUNKS_INPUT_PATH = "data/chunks"
METADATA_OUTPUT_PATH = "data/metadata"

os.makedirs(METADATA_OUTPUT_PATH, exist_ok=True)

def build_metadata():
    metadata_list = []

    for filename in os.listdir(TEXT_INPUT_PATH):
        if filename.endswith(".txt"):

            # TEXT file path
            text_file = os.path.join(TEXT_INPUT_PATH, filename)

            # CHUNKED version path
            chunk_file = os.path.join(
                CHUNKS_INPUT_PATH,
                filename.replace(".txt", "_chunks.txt")
            )

            if not os.path.exists(chunk_file):
                print(f"No chunks found for {filename}")
                continue

            # Read all chunks
            with open(chunk_file, "r", encoding="utf-8") as f:
                raw = f.read().split("---\n")

            # Build metadata per chunk
            for i, chunk in enumerate(raw):
                entry = {
                    "document_name": filename,
                    "chunk_id": f"{filename}_chunk_{i}",
                    "index": i,
                    "source_path": text_file,
                    "chunk_length": len(chunk),
                }
                metadata_list.append(entry)

    # Save metadata JSON
    output_file = os.path.join(METADATA_OUTPUT_PATH, "metadata.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(metadata_list, f, indent=4, ensure_ascii=False)

    print(f"Metadata saved → {output_file}")
    print(f"Total chunks indexed: {len(metadata_list)}")


if __name__ == "__main__":
    build_metadata()
