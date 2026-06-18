# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

**Off-campus student housing** — the practical, experience-based knowledge that students accumulate about renting apartments, avoiding bad landlords, understanding leases, and surviving the first year of independent living.

This knowledge is valuable because it directly affects thousands of dollars in rent decisions, legal obligations through lease contracts, and day-to-day quality of life. It is hard to find through official channels because universities only share sanitized housing office listings, not candid landlord reviews or tenant horror stories. The real knowledge lives scattered across Reddit threads, anonymous reviews, and word-of-mouth advice that evaporates when students graduate. This guide aggregates that informal knowledge — questions like "What should I check before signing a lease?", "How do I get my security deposit back?", or "What utilities are typically not included in rent?" — into a single searchable resource.

---

## Documents

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Reddit r/offcampushousing | Top posts and comments on lease tips, landlord red flags, and apartment hunting | https://www.reddit.com/r/offcampushousing/ |
| 2 | Reddit r/college | Student advice threads on finding and affording off-campus housing | https://www.reddit.com/r/college/search/?q=off+campus+housing |
| 3 | Reddit r/personalfinance | Budgeting threads for first-time renters: how to split utilities, set up renter's insurance | https://www.reddit.com/r/personalfinance/search/?q=first+apartment+budget |
| 4 | Nolo.com — Tenant Rights | Legal guide on security deposits, lease terms, landlord entry rights, and eviction basics | https://www.nolo.com/legal-encyclopedia/tenant-rights-responsibilities.html |
| 5 | Apartments.com Blog | "Tips for Renting Your First Apartment Off Campus" — practical checklist article | https://www.apartments.com/blog/renting-off-campus-apartment-tips |
| 6 | Rent.com Blog | "Off-Campus Housing Guide for College Students" — covers budget, roommates, location | https://www.rent.com/blog/off-campus-housing-guide-for-students/ |
| 7 | Zillow Learn | "First-Time Renter Tips" — what to inspect, what to ask, what to document | https://www.zillow.com/learn/first-time-renter-tips/ |
| 8 | The Balance Money | "First Apartment Checklist" — room-by-room walkthrough before move-in | https://www.thebalancemoney.com/first-apartment-checklist-1289714 |
| 9 | ApartmentRatings.com | Curated student-written reviews of apartment complexes near universities | https://www.apartmentratings.com |
| 10 | Yelp | Student reviews of apartment complexes — candid comments on management, maintenance, noise | https://www.yelp.com (search: apartments near [campus]) |
| 11 | Reddit r/legaladvice | Threads on lease disputes, security deposit withholding, and landlord violations | https://www.reddit.com/r/legaladvice/search/?q=landlord+student+lease |
| 12 | MyApartmentMap.com | Student housing reviews aggregated by campus proximity | https://www.myapartmentmap.com |

---

## Chunking Strategy

**Chunk size:** 400 characters (~80–100 tokens)

**Overlap:** 80 characters (~20 tokens)

**Reasoning:**

The corpus is a mix of two document types with very different structures:

- **Short reviews** (Reddit comments, Yelp reviews): typically 1–4 sentences expressing a single opinion or tip. A 400-character chunk fits one complete review without splitting it, keeping the sentiment and subject together. If a review is shorter than 400 characters, it becomes one chunk. If longer, an 80-character overlap ensures a continued thought (e.g., "The management is great, BUT the maintenance team...") doesn't get cut off mid-sentence at a chunk boundary.

- **Long guides** (Nolo, Apartments.com, Zillow): structured articles with paragraphs of 200–500 characters each. At 400 characters, each chunk captures roughly one paragraph or one logical point (e.g., "how to inspect for mold" or "what landlords can legally deduct from deposits"). The 80-character overlap preserves the connective tissue between adjacent points so neither chunk is orphaned.

**Why not smaller (e.g., 100 characters)?** A single sentence like "Don't sign without reading the utility clause" retrieves correctly but lacks the surrounding context a model needs to give a useful answer. The LLM would receive fragments, not thoughts.

**Why not larger (e.g., 1000 characters)?** Multi-paragraph chunks dilute the embedding signal — a chunk about "deposits AND maintenance AND parking" becomes hard to match precisely to a narrow query like "security deposit rules." Retrieval precision drops.

**Bad retrieval signals to watch for:** If results keep returning chunks about the wrong subtopic (e.g., "dining" when asked about "deposits"), chunks are probably too large. If results return exact-keyword matches but the model can't generate a coherent answer, chunks are probably too small.

---

## Retrieval Approach

**Embedding model:** `all-MiniLM-L6-v2` via `sentence-transformers`

**Top-k:** 5

**Reasoning for top-k = 5:** Five chunks (~2,000 characters of context) gives the Groq LLM enough evidence to synthesize a grounded answer without overloading the context window or introducing irrelevant noise. With fewer than 3 chunks, a niche question might lack supporting evidence. With more than 7, the model starts receiving off-topic chunks that weren't relevant enough to rank in the top 5, which increases hallucination risk.

**Production tradeoff reflection:**

`all-MiniLM-L6-v2` is fast and free, but it was trained on general English text, not student housing jargon. For a real deployment, the tradeoffs I'd weigh:

- **Domain accuracy:** A model fine-tuned on informal review text (e.g., a model trained on Yelp/Reddit corpora) would better understand phrases like "super sketchy management" or "the AC unit dies every August." General models may miss domain-specific sentiment.
- **Context length:** `all-MiniLM-L6-v2` has a 256-token limit; for longer guide documents, `all-mpnet-base-v2` (512 tokens) would handle paragraph-length chunks without truncation.
- **Multilingual support:** If the user base includes non-native speakers, a multilingual model like `paraphrase-multilingual-MiniLM-L12-v2` would matter.
- **Latency vs. accuracy:** Larger models (e.g., `text-embedding-ada-002` from OpenAI) produce higher-quality embeddings but add API latency and cost. For a student Q&A tool, `all-MiniLM-L6-v2` hits the right cost/speed tradeoff.

**Why semantic search works without exact word matches:** The embedding model maps both the query and the documents into the same vector space where semantically similar phrases land near each other. "What do I check before signing?" and "lease inspection checklist" have different words but similar meaning vectors, so cosine similarity finds the match without keyword overlap.

---

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What should I look for when inspecting an apartment before signing a lease? | The system should return advice on checking for mold, water damage, working locks, functioning appliances, pest evidence, and the condition of walls/floors — and recommend documenting everything with photos before move-in. |
| 2 | Can a landlord keep my entire security deposit if I leave the apartment dirty? | The system should answer that landlords can deduct cleaning costs from a deposit but must provide an itemized statement of deductions; they cannot keep the full deposit for normal wear and tear, only for damage beyond that. |
| 3 | What utilities are typically not included in rent for student apartments? | The system should list electricity, internet, and renter's insurance as commonly excluded, while water and trash are sometimes included; the answer should note that students must ask explicitly what is and isn't covered. |
| 4 | What are common red flags when touring an apartment? | The system should list: unresponsive or evasive landlord, signs of water damage or mold, broken fixtures the landlord dismisses, unusually low rent for the area, pressure to sign immediately, and no written lease. |
| 5 | How much of my monthly income should I budget for rent as a student? | The system should return the common 30% rule (rent ≤ 30% of gross monthly income) and note that students on tight budgets often need to split costs with roommates or choose farther-from-campus options to stay within budget. |

---

## Anticipated Challenges

1. **Noisy and inconsistent review text:** Reddit comments and Yelp reviews are informal, emotional, and often contain slang, sarcasm, or incomplete sentences ("management = garbage, avoid!!!"). This makes embeddings less reliable — a frustrated rant and a genuine warning may embed very differently even if they convey the same information. Mitigation: lightly pre-process text to strip excessive punctuation and normalize capitalization before chunking.

2. **Chunks splitting critical facts across boundaries:** A single review sentence might span two chunks if the chunk boundary falls mid-sentence (e.g., "They kept my deposit..." in chunk 4, "...because I left a mark on the wall" in chunk 5). If only one chunk is retrieved, the answer is misleading or incomplete. Mitigation: the 80-character overlap ensures both halves of a split sentence appear in adjacent chunks, so at least one chunk contains the full thought. I'll also verify during testing by manually inspecting retrieved chunks for truncated context.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    OFF-CAMPUS HOUSING GUIDE                      │
│                     RAG Pipeline Overview                         │
└─────────────────────────────────────────────────────────────────┘

  ┌──────────────────────┐
  │  1. DOCUMENT          │
  │     INGESTION         │
  │                       │
  │  Tool: Python         │
  │  (open() / manual     │
  │   copy-paste to .txt) │
  │                       │
  │  Input: 12 .txt files │
  │  in documents/        │
  └──────────┬───────────┘
             │ raw text strings
             ▼
  ┌──────────────────────┐
  │  2. CHUNKING          │
  │                       │
  │  Tool: Python         │
  │  (custom chunk_text() │
  │   function)           │
  │                       │
  │  chunk_size: 400 chars│
  │  overlap:    80 chars │
  └──────────┬───────────┘
             │ list of chunk strings
             ▼
  ┌──────────────────────┐
  │  3. EMBEDDING +       │
  │     VECTOR STORE      │
  │                       │
  │  Embed: sentence-     │
  │  transformers         │
  │  all-MiniLM-L6-v2    │
  │                       │
  │  Store: ChromaDB      │
  │  (local persistent)   │
  └──────────┬───────────┘
             │ vector index on disk (chroma_db/)
             ▼
  ┌──────────────────────┐
  │  4. RETRIEVAL         │
  │                       │
  │  Tool: ChromaDB       │
  │  .query() method      │
  │                       │
  │  top-k: 5 chunks      │
  │  Metric: cosine sim   │
  └──────────┬───────────┘
             │ top-5 relevant chunks + metadata
             ▼
  ┌──────────────────────┐
  │  5. GENERATION        │
  │                       │
  │  Tool: Groq API       │
  │  (llama-3.3-70b or    │
  │   mixtral-8x7b)       │
  │                       │
  │  Prompt: retrieved    │
  │  chunks + user query  │
  │  + grounding rules    │
  │                       │
  │  Output: sourced,     │
  │  grounded answer      │
  └──────────────────────┘
```

---

## AI Tool Plan

**Milestone 3 — Ingestion and chunking:**

I will give Claude the following inputs:
- This planning.md (Chunking Strategy section)
- The requirement that documents live in `documents/` as `.txt` files
- The constraint that chunks must carry source metadata (filename) for attribution

I will ask Claude to implement two functions: `load_documents(folder_path) -> list[dict]` (reads all `.txt` files and returns list of `{text, source}` dicts) and `chunk_text(text, chunk_size=400, overlap=80) -> list[str]` (splits on character count with overlap). I will verify by printing the first 3 chunks from two different documents and confirming: (a) no chunk is empty, (b) overlap text from chunk N appears at the start of chunk N+1, (c) each chunk is ≤ 400 characters.

**Milestone 4 — Embedding and retrieval:**

I will give Claude the following inputs:
- This planning.md (Retrieval Approach section and Architecture diagram)
- The ChromaDB and sentence-transformers library versions from requirements.txt
- The output format from Milestone 3 (list of `{text, source}` dicts with chunks)

I will ask Claude to implement `build_index(chunks_with_metadata)` (embeds all chunks using `all-MiniLM-L6-v2` and upserts into a ChromaDB persistent collection) and `retrieve(query, k=5) -> list[dict]` (embeds the query and returns top-k chunks with source metadata). I will verify by running 3 queries from the Evaluation Plan and checking that the returned chunks are topically relevant and include source filenames.

**Milestone 5 — Generation and interface:**

I will give Claude the following inputs:
- This planning.md (Evaluation Plan section — the 5 test questions and expected answers)
- The Groq API documentation for chat completions
- The grounding requirement: the model must refuse to answer if no relevant chunks are retrieved, and must cite sources in its response

I will ask Claude to implement `generate_answer(query, retrieved_chunks) -> str` that constructs a system prompt enforcing grounding (e.g., "Answer only using the provided context. If the context does not contain enough information, say so.") and calls the Groq API. I will also ask it to implement a simple CLI loop for `main()`. I will verify by running all 5 evaluation questions and checking answers against expected answers, then running one out-of-scope query (e.g., "What is the capital of France?") and confirming the system refuses.
