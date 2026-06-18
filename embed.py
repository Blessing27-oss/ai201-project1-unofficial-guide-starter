"""
Milestone 4: Embedding and retrieval pipeline.

Embeds all chunks from ingest.py using all-MiniLM-L6-v2 (sentence-transformers),
stores them in a persistent ChromaDB collection with source metadata,
and provides a retrieve() function for querying the vector store.
"""

import os
import chromadb
from sentence_transformers import SentenceTransformer
from ingest import build_corpus

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "housing_guide"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 5


def build_index(corpus: list[dict], persist_dir: str = CHROMA_DIR) -> chromadb.Collection:
    """
    Embed all chunks and upsert into a persistent ChromaDB collection.

    Each chunk is stored with:
      - document text  (the chunk content)
      - id             (source filename + chunk index, unique)
      - metadata       (source filename, chunk_index)

    Returns the ChromaDB collection.
    """
    print(f"Loading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)

    print(f"Embedding {len(corpus)} chunks...")
    texts = [item["text"] for item in corpus]
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=64)

    # Persistent client — stores index to disk so we don't re-embed every run
    client = chromadb.PersistentClient(path=persist_dir)

    # Delete and recreate collection so re-runs start clean
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},  # use cosine similarity
    )

    ids = [f"{item['source']}__chunk{item['chunk_index']}" for item in corpus]
    metadatas = [{"source": item["source"], "chunk_index": item["chunk_index"]} for item in corpus]

    collection.upsert(
        ids=ids,
        embeddings=embeddings.tolist(),
        documents=texts,
        metadatas=metadatas,
    )

    print(f"Index built: {collection.count()} chunks stored in {persist_dir}/")
    return collection


def load_collection(persist_dir: str = CHROMA_DIR) -> tuple[chromadb.Collection, SentenceTransformer]:
    """
    Load an existing ChromaDB collection and the embedding model for querying.
    Raises if the collection doesn't exist (run build_index first).
    """
    client = chromadb.PersistentClient(path=persist_dir)
    collection = client.get_collection(COLLECTION_NAME)
    model = SentenceTransformer(EMBEDDING_MODEL)
    return collection, model


def retrieve(query: str, collection: chromadb.Collection, model: SentenceTransformer, k: int = TOP_K) -> list[dict]:
    """
    Embed the query and return the top-k most similar chunks.

    Returns a list of dicts:
      {
        "text": str,          # chunk content
        "source": str,        # source filename
        "chunk_index": int,   # position in source document
        "distance": float,    # cosine distance (lower = more similar)
      }
    """
    query_embedding = model.encode([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for text, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({
            "text": text,
            "source": meta["source"],
            "chunk_index": meta["chunk_index"],
            "distance": round(dist, 4),
        })

    return chunks


# ---------------------------------------------------------------------------
# Main: build index and run 3 retrieval tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Build the index from scratch
    corpus = build_corpus("documents")
    collection = build_index(corpus)
    model = SentenceTransformer(EMBEDDING_MODEL)

    # Test queries from the evaluation plan
    test_queries = [
        "What should I look for when inspecting an apartment before signing a lease?",
        "Can a landlord keep my entire security deposit if I leave the apartment dirty?",
        "What utilities are typically not included in rent for student apartments?",
    ]

    print("\n" + "=" * 60)
    print("RETRIEVAL TESTS")
    print("=" * 60)

    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 50)
        results = retrieve(query, collection, model, k=TOP_K)
        for i, r in enumerate(results, 1):
            print(f"  [{i}] distance={r['distance']} | source={r['source']}")
            print(f"      {r['text'][:200].strip()}...")
        print()
