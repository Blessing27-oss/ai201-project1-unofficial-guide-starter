"""
Milestone 5: Grounded generation using Groq LLM.

Wires together:
  1. Retrieval  — top-k chunks from ChromaDB (embed.py)
  2. Generation — Groq llama-3.3-70b-versatile with a grounding prompt

The system prompt explicitly prevents the model from drawing on
training knowledge: it must answer only from the provided context,
and must name the source documents it used. If the context is
insufficient, it must say so rather than improvising.
"""

import os
from groq import Groq
from dotenv import load_dotenv
from embed import load_collection, retrieve
from sentence_transformers import SentenceTransformer

load_dotenv()

GROQ_MODEL = "llama-3.3-70b-versatile"
TOP_K = 5

# ---------------------------------------------------------------------------
# System prompt — grounding instruction
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are a helpful assistant for students researching off-campus housing.

STRICT RULES — follow these exactly:
1. Answer ONLY using information explicitly stated in the CONTEXT DOCUMENTS below.
2. Do NOT use your general training knowledge. If the context does not contain enough information to answer the question, respond with: "I don't have enough information in my documents to answer that."
3. After your answer, list the source documents you drew from under a line that reads "Sources:". Use the exact filenames provided in each document's header.
4. Keep your answer focused and practical. Students are making real housing decisions.
"""

# ---------------------------------------------------------------------------
# Core ask() function
# ---------------------------------------------------------------------------

_collection = None
_model = None


def _get_retrieval_components():
    """Lazy-load the ChromaDB collection and embedding model once."""
    global _collection, _model
    if _collection is None:
        _collection, _model = load_collection()
    return _collection, _model


def ask(question: str, k: int = TOP_K) -> dict:
    """
    End-to-end RAG: retrieve relevant chunks, generate a grounded answer.

    Returns:
        {
            "answer": str,          # LLM-generated answer grounded in context
            "sources": list[str],   # unique source filenames used
            "chunks": list[dict],   # raw retrieved chunks (for debugging)
        }
    """
    collection, model = _get_retrieval_components()

    # Step 1: Retrieve
    chunks = retrieve(question, collection, model, k=k)

    # Step 2: Build context block for the prompt
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        context_parts.append(
            f"[Document {i}: {chunk['source']}]\n{chunk['text']}"
        )
    context_block = "\n\n".join(context_parts)

    # Step 3: Build the user message
    user_message = f"""CONTEXT DOCUMENTS:
{context_block}

QUESTION: {question}

Remember: answer only from the context documents above. If they don't contain the answer, say so."""

    # Step 4: Call Groq
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,   # low temperature for factual, consistent answers
        max_tokens=600,
    )

    answer = response.choices[0].message.content.strip()

    # Step 5: Programmatically collect sources (guaranteed, not left to the LLM)
    sources = list(dict.fromkeys(chunk["source"] for chunk in chunks))

    return {
        "answer": answer,
        "sources": sources,
        "chunks": chunks,
    }


# ---------------------------------------------------------------------------
# CLI test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    test_queries = [
        "What should I look for when inspecting an apartment before signing a lease?",
        "Can a landlord keep my entire security deposit if I leave the apartment dirty?",
        "What utilities are typically not included in rent for student apartments?",
        "What is the best restaurant in Paris?",   # out-of-scope — should refuse
    ]

    for query in test_queries:
        print("\n" + "=" * 60)
        print(f"QUERY: {query}")
        print("=" * 60)
        result = ask(query)
        print(result["answer"])
        print("\nSources (programmatic):", result["sources"])
