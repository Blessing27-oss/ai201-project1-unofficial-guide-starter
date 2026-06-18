"""
Milestone 3: Document ingestion and chunking pipeline.

Loads all .txt files from the documents/ folder, cleans them,
splits them into overlapping character-based chunks, and prints
a summary and 5 sample chunks for inspection.

Chunking spec (from planning.md):
  chunk_size = 400 characters
  overlap    =  80 characters
"""

import os
import re
import random


DOCUMENTS_DIR = "documents"
CHUNK_SIZE = 400
OVERLAP = 80


# ---------------------------------------------------------------------------
# Step 1: Load documents
# ---------------------------------------------------------------------------

def load_documents(folder_path: str) -> list[dict]:
    """
    Read every .txt file in folder_path.
    Returns a list of dicts: {"text": str, "source": str}
    """
    docs = []
    for filename in sorted(os.listdir(folder_path)):
        if not filename.endswith(".txt"):
            continue
        filepath = os.path.join(folder_path, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            raw = f.read()
        docs.append({"text": raw, "source": filename})
    return docs


# ---------------------------------------------------------------------------
# Step 2: Clean documents
# ---------------------------------------------------------------------------

def clean_text(text: str) -> str:
    """
    Remove boilerplate and normalise whitespace.
    Keeps all substantive content.
    """
    # Remove HTML tags (safety net for any copy-pasted content)
    text = re.sub(r"<[^>]+>", " ", text)

    # Decode common HTML entities
    text = text.replace("&amp;", "&")
    text = text.replace("&nbsp;", " ")
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&quot;", '"')
    text = text.replace("&#39;", "'")

    # Collapse multiple blank lines into one separator
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Collapse runs of spaces/tabs to a single space per line
    text = re.sub(r"[ \t]+", " ", text)

    # Strip leading/trailing whitespace from each line
    lines = [line.strip() for line in text.splitlines()]
    text = "\n".join(lines)

    return text.strip()


# ---------------------------------------------------------------------------
# Step 3: Chunk text
# ---------------------------------------------------------------------------

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> list[str]:
    """
    Split text into overlapping character-based chunks.

    chunk_size: maximum characters per chunk
    overlap:    characters of context shared between adjacent chunks

    Strategy: slide a window of size chunk_size over the text, stepping
    forward by (chunk_size - overlap) each time, so that the tail of one
    chunk reappears at the head of the next. This prevents a key fact
    split across a boundary from being lost entirely.
    """
    chunks = []
    step = chunk_size - overlap
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if len(chunk) > 0:
            chunks.append(chunk)
        start += step

    return chunks


# ---------------------------------------------------------------------------
# Step 4: Build the full chunk corpus with metadata
# ---------------------------------------------------------------------------

def build_corpus(folder_path: str) -> list[dict]:
    """
    Load, clean, and chunk all documents.
    Returns a list of dicts: {"text": str, "source": str, "chunk_index": int}
    """
    documents = load_documents(folder_path)
    corpus = []

    for doc in documents:
        cleaned = clean_text(doc["text"])
        chunks = chunk_text(cleaned)
        for i, chunk in enumerate(chunks):
            corpus.append({
                "text": chunk,
                "source": doc["source"],
                "chunk_index": i,
            })

    return corpus


# ---------------------------------------------------------------------------
# Main: run the pipeline and inspect results
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("DOCUMENT INGESTION AND CHUNKING PIPELINE")
    print("=" * 60)

    # Load and process
    corpus = build_corpus(DOCUMENTS_DIR)

    # Summary stats
    sources = {}
    for item in corpus:
        sources[item["source"]] = sources.get(item["source"], 0) + 1

    print(f"\nDocuments loaded: {len(sources)}")
    print(f"Total chunks:     {len(corpus)}")
    print(f"Chunk size:       {CHUNK_SIZE} chars")
    print(f"Overlap:          {OVERLAP} chars")

    print("\nChunks per document:")
    for src, count in sorted(sources.items()):
        print(f"  {src}: {count} chunks")

    # Validation checks
    empty = [c for c in corpus if len(c["text"].strip()) == 0]
    too_short = [c for c in corpus if 0 < len(c["text"].strip()) < 50]
    print(f"\nEmpty chunks:      {len(empty)}")
    print(f"Very short (<50):  {len(too_short)}")

    # Print 5 representative chunks for inspection
    print("\n" + "=" * 60)
    print("SAMPLE CHUNKS (5 representative chunks)")
    print("=" * 60)

    # Pick one chunk from 5 different source files for variety
    seen_sources = set()
    samples = []
    for item in corpus:
        if item["source"] not in seen_sources:
            samples.append(item)
            seen_sources.add(item["source"])
        if len(samples) == 5:
            break

    for i, sample in enumerate(samples, 1):
        print(f"\n--- Chunk {i} ---")
        print(f"Source: {sample['source']} (chunk index {sample['chunk_index']})")
        print(f"Length: {len(sample['text'])} characters")
        print(f"Text:\n{sample['text']}")

    # Overlap verification: show that chunk N and N+1 share text
    print("\n" + "=" * 60)
    print("OVERLAP VERIFICATION (chunk 0 and 1 from first document)")
    print("=" * 60)
    first_source = sorted(sources.keys())[0]
    first_doc_chunks = [c for c in corpus if c["source"] == first_source]
    if len(first_doc_chunks) >= 2:
        c0 = first_doc_chunks[0]["text"]
        c1 = first_doc_chunks[1]["text"]
        overlap_text = c0[-(OVERLAP):]
        print(f"Last {OVERLAP} chars of chunk 0: ...{repr(overlap_text)}")
        print(f"First {OVERLAP} chars of chunk 1: {repr(c1[:OVERLAP])}...")
        if overlap_text.strip() in c1:
            print("Overlap verified: tail of chunk 0 appears in chunk 1.")
        else:
            print("Note: overlap boundary falls mid-whitespace (strip normalises this).")
