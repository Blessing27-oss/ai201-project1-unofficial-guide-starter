# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

**Off-campus student housing** — practical, experience-based knowledge about renting apartments, understanding leases, avoiding bad landlords, and managing the real costs of living independently as a student.

This knowledge is valuable because it directly affects thousands of dollars in rent decisions and legal obligations, yet it's almost impossible to find through official channels. University housing offices share sanitized listings and generic checklists; they don't publish candid landlord reviews, document common lease traps, or explain what happens when a roommate stops paying rent. The real knowledge — which complexes have chronic maintenance issues, what utilities are typically excluded from "utilities included" listings, how to fight an improper security deposit deduction — lives scattered across Reddit threads, anonymous reviews, and word-of-mouth that evaporates when students graduate.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Reddit r/offcampushousing | Reddit forum posts | https://www.reddit.com/r/offcampushousing/ |
| 2 | Reddit r/college — housing advice threads | Reddit forum posts | https://www.reddit.com/r/college/ |
| 3 | Reddit r/personalfinance — first apartment budgeting | Reddit forum posts | https://www.reddit.com/r/personalfinance/ |
| 4 | Reddit r/legaladvice — lease disputes and tenant issues | Reddit forum posts | https://www.reddit.com/r/legaladvice/ |
| 5 | Nolo.com — Tenant Rights and Responsibilities | Legal guide article | https://www.nolo.com/legal-encyclopedia/tenant-rights-responsibilities.html |
| 6 | Apartments.com Blog — Off-Campus Renting Tips | How-to article | https://www.apartments.com/blog/renting-off-campus-apartment-tips |
| 7 | Rent.com Blog — Off-Campus Housing Guide for Students | How-to article | https://www.rent.com/blog/off-campus-housing-guide-for-students/ |
| 8 | Zillow Learn — First-Time Renter Tips | How-to article | https://www.zillow.com/learn/first-time-renter-tips/ |
| 9 | The Balance Money — First Apartment Checklist | Checklist article | https://www.thebalancemoney.com/first-apartment-checklist-1289714 |
| 10 | ApartmentRatings.com — student complex reviews | Review aggregator | https://www.apartmentratings.com |
| 11 | Yelp — student apartment complex reviews | Review aggregator | https://www.yelp.com (apartments near campus) |
| 12 | MyApartmentMap.com — campus proximity reviews | Review aggregator | https://www.myapartmentmap.com |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 400 characters

**Overlap:** 80 characters

**Why these choices fit your documents:** The corpus mixes two document types. Short Reddit/Yelp reviews are typically 1–4 sentences (100–300 characters), so a 400-character chunk fits one complete review without merging it with an unrelated one. Longer guide articles (Nolo, Apartments.com, Zillow) have paragraphs of 200–500 characters, so 400 characters captures roughly one logical point — e.g., "how to inspect for mold" or "what landlords can deduct from deposits" — without diluting the embedding with multiple unrelated topics. The 80-character overlap ensures that a key fact split at a chunk boundary (e.g., a legal rule split across two chunks) still appears in at least one complete chunk. Pre-processing: HTML tags removed, HTML entities decoded, consecutive blank lines collapsed, leading/trailing whitespace stripped per line.

**Final chunk count:** 176 chunks across 13 documents (12–16 chunks per document)

---

## Sample Chunks

<!-- Paste 5 representative chunks from your document collection after running your ingestion pipeline.
     For each chunk, note which source document it came from.
     These must be actual text — not screenshots. -->

| # | Source document | Chunk text |
|---|----------------|------------|
| 1 | `apartments_com_student_guide.txt` | Don't apply to five apartments at once unless you're prepared to lose $200 in fees. Prioritize and apply to your top two choices first. --- Renters insurance is not optional: Your landlord's property insurance covers the building's structure, not your belongings. If there's a fire, a burst pipe, or a break-in, you get nothing for your laptop, TV, or clothes without renters insurance. Policies ty... |
| 2 | `myapartmentmap_reviews.txt` | I could hear my upstairs neighbor's alarm clock every morning. If noise sensitivity is a concern, ask to see a unit that isn't on the ground floor or directly below another unit. Parking is $95/month extra. Management is professional and responds within a day or two. --- Birchwood Apartments — 4/5 Best-kept secret near campus. A 15-minute bike ride from the main buildings, but the lower rent mor... |
| 3 | `reddit_college_housing.txt` | Budget for this. --- Ask about noise before you move in. Apartments above bars or near fraternity houses can be loud on weekends. Ask current tenants (knock on a neighbor's door) what noise is like, not just the landlord. The landlord will always say it's quiet. --- Internet is the most commonly forgotten utility for students. Most apartments don't include it. Budget $50-80/month for a reliabl... |
| 4 | `reddit_legaladvice_lease.txt` | Mold that affects habitability is a landlord's responsibility to remediate. Document it: photographs with timestamps, written requests to the landlord, the landlord's written or verbal responses. If the landlord ignores written requests, you may be able to: withhold rent (escrow it while the dispute is pending), file a complaint with your local housing authority, or in some states, break the leas... |
| 5 | `reddit_offcampus_tips.txt` | That means if your roommate stops paying rent, you're on the hook for their share too. The landlord doesn't have to chase your roommate first — they can come straight to you. Have a roommate agreement that covers who pays what and what happens if someone needs to leave early. --- Renter's insurance is cheap ($10-20/month) and almost everyone skips it. Your landlord's property insurance covers t... |

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers` (runs locally, no API key required)

**Production tradeoff reflection:** `all-MiniLM-L6-v2` is fast, free, and runs entirely on-device, which makes it ideal for a student project with no budget. For a real deployment I would weigh several tradeoffs. First, domain accuracy: this model was trained on general English text, not student housing jargon — a model fine-tuned on informal review corpora (Yelp, Reddit) would better understand phrases like "management is garbage" or "the AC dies every August." Second, context length: `all-MiniLM-L6-v2` truncates at 256 tokens, which is fine for 400-character chunks but would drop content in longer chunks; `all-mpnet-base-v2` handles 512 tokens. Third, latency vs. accuracy: OpenAI's `text-embedding-3-small` produces higher-quality embeddings but adds API latency and cost per query. For a high-traffic student tool, the local model's zero marginal cost would outweigh the marginal accuracy gain.

---

## Retrieval Test Results

<!-- Run these 3 queries through your retrieval system and record the top returned chunks.
     For at least 2 of the 3, explain why the returned chunks are relevant to the query.
     Results must be text — not screenshots. -->

**Query 1:** What should I look for when inspecting an apartment before signing a lease?

Top returned chunks:
- `apartments_com_student_guide.txt` (distance 0.31) — "What to look for in a lease before signing: Read the entire lease, not just the rent amount. Key sections to review: lease term and end date, rent amount and due date, late fee amount and grace period..."
- `reddit_offcampus_tips.txt` (distance 0.39) — "Red flag: if the landlord pressures you to sign the same day you tour, walk away. A legitimate landlord will give you at least 24-48 hours to review the lease..."
- `first_apartment_checklist.txt` (distance 0.41) — "BEFORE YOU SIGN THE LEASE — Budget check, Utility confirmation, Lease review..."

Relevance explanation: All three chunks directly address pre-signing inspection and lease review. The top result covers what sections of a lease to examine; the second adds behavioral red flags during a tour; the third provides a room-by-room checklist. Together they give a complete picture. The 0.31 distance on the top result indicates a strong semantic match despite the query not using the exact phrase "what to look for."

---

**Query 2:** Can a landlord keep my entire security deposit if I leave the apartment dirty?

Top returned chunks:
- `tenant_rights_guide.txt` (distance 0.35) — "Security deposits: Most states cap security deposits at one to two months' rent. Landlords must return the deposit within a legally specified window... they must provide an itemized written statement of any deductions."
- `reddit_offcampus_tips.txt` (distance 0.37) — "My landlord tried to keep my entire $1,200 deposit because I left a nail hole in the wall. My state's tenant law says nail holes are considered normal wear and tear..."
- `apartments_com_student_guide.txt` (distance 0.42) — "After you move out, your landlord must return your deposit within the state-mandated timeframe (usually 14-30 days) with an itemized statement of any deductions..."

Relevance explanation: The top result from the legal guide directly answers the question: landlords must itemize deductions and can only charge for damage beyond normal wear and tear, not for ordinary dirtiness. The second result is a first-person account of exactly this scenario (deposit dispute over normal wear). Both are highly on-target. Distance scores around 0.35–0.42 confirm strong matches.

---

**Query 3:** What utilities are typically not included in rent for student apartments?

Top returned chunks:
- `reddit_offcampus_tips.txt` (distance 0.27) — "Don't sign a lease that doesn't specify who pays which utilities. I've seen leases that say 'tenant pays utilities' but don't clarify water, trash, gas, or common-area electricity..."
- `apartments_com_student_guide.txt` (distance 0.35) — "Always ask specifically whether these are included or excluded from rent: electricity, gas/heat, water, sewer, trash collection, internet, parking, laundry..."
- `yelp_apartment_reviews.txt` (distance 0.39) — "Northgate Student Housing — 1 star: The 'all utilities included' in the listing was a lie. Water and trash were included. Electricity had a cap of $75/month..."

Relevance explanation: This query got the strongest retrieval of the three (top distance 0.27). The first result is a direct Reddit warning about vague utility clauses; the second lists every common utility category and its typical inclusion status; the third is a real student review documenting a utility cap trap. The system retrieved from three different source types (forum, guide, review), demonstrating that the embeddings are finding semantically similar content across varied document structures.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

The system prompt passed to the LLM before every query:

> "You are a helpful assistant for students researching off-campus housing.
> STRICT RULES — follow these exactly:
> 1. Answer ONLY using information explicitly stated in the CONTEXT DOCUMENTS below.
> 2. Do NOT use your general training knowledge. If the context does not contain enough information to answer the question, respond with: 'I don't have enough information in my documents to answer that.'
> 3. After your answer, list the source documents you drew from under a line that reads 'Sources:'. Use the exact filenames provided in each document's header.
> 4. Keep your answer focused and practical. Students are making real housing decisions."

The user message then injects the retrieved chunks formatted as labeled sections (`[Document 1: filename.txt]`) before the question, making the boundary between context and question explicit.

**How source attribution is surfaced in the response:**

Two mechanisms work together. The LLM is instructed to list source filenames at the end of every response under a "Sources:" heading. Additionally, `query.py` programmatically collects unique source filenames from the retrieved chunks and returns them in the result dict — so even if the model omits a citation, the interface can display all retrieved sources. Both are shown to the user in the Gradio interface.

---

## Example Responses

<!-- Provide at least 2 grounded responses (query + response + source attribution)
     and 1 out-of-scope query showing your system's refusal.
     All entries must be text — not screenshots. -->

**Grounded response 1**

Query: What should I look for when inspecting an apartment before signing a lease?

Response: When inspecting an apartment before signing a lease, you should check the kitchen to ensure that the stove burners and oven work at all settings, the refrigerator maintains temperature and has intact door seals, and the dishwasher runs a full cycle without leaking. You should also check that the garbage disposal works, look under the sink for signs of water damage or mold, and verify that outlets near the sink are GFCI-protected. Additionally, you should check the bathroom to ensure that hot water reaches adequate temperature within 60 seconds, the shower pressure is acceptable, the toilet flushes and refills completely without running, and there is no mold visible in grout, caulk, or ceiling corners. In the bedroom and living areas, you should test all outlets, ensure windows open, close, and lock properly, and check that closet doors open and close without sticking. You should also look for any stains on the carpet or damage on hardwood floors, and make sure there are no holes or large marks on the walls beyond minor scuffs. Before you sign, you should also review the entire lease and check for red flags such as a landlord who pressures you to sign the same day you tour.

Sources:
first_apartment_checklist.txt

Source attribution: LLM cited `first_apartment_checklist.txt`; programmatic sources also include `apartments_com_student_guide.txt`, `reddit_offcampus_tips.txt`, `rent_com_offcampus_guide.txt`.

---

**Grounded response 2**

Query: What utilities are typically not included in rent for student apartments?

Response: Based on the context documents, utilities that are typically not included in rent for student apartments include electricity, gas/heat, internet, and sometimes water and trash (although these may be included in some cases). Additionally, other utilities such as sewer, parking, laundry, and common-area maintenance fees may also not be included in rent. It is important to always ask specifically whether these are included or excluded from rent, as not all apartment listings are transparent about utilities. Students should be aware that "some utilities included" in a listing can be misleading, and it is important to get the specific list of included utilities in writing.

Sources:
reddit_offcampus_tips.txt
apartments_com_student_guide.txt
apartment_ratings_reviews.txt
yelp_apartment_reviews.txt

Source attribution: LLM cited all four source files; programmatic sources match exactly.

---

**Out-of-scope query**

Query: What is the best restaurant in Paris?

System response (refusal): I don't have enough information in my documents to answer that.

Sources:
myapartmentmap_reviews.txt
rent_com_offcampus_guide.txt
apartments_com_student_guide.txt
yelp_apartment_reviews.txt

---

## Query Interface

<!-- Describe your query interface: what are the input fields, what does the output look like?
     Then provide a complete sample interaction transcript showing a real exchange. -->

**Input fields:** A single text box labeled "Your question" where the student types a free-form housing question. A primary "Ask" button submits the query. Five pre-loaded example question buttons let users click directly without typing. Pressing Enter in the text box also triggers a query.

**Output format:** Two read-only text areas below the input. The first, labeled "Answer," displays the LLM's grounded response (typically 3–8 sentences). The second, labeled "Retrieved from," lists the source document filenames the answer drew from, one per line with a bullet prefix.

---

**Sample Interaction Transcript**

> **User:** How do I get my security deposit back after moving out?

> **System:** To get your security deposit back after moving out, you should follow these steps. Before moving out, make sure to provide the required notice as specified in your lease (typically 30-60 days). Clean the unit to the standard it was in when you moved in, as landlords can only charge for cleaning if the unit was left in a condition requiring it — dirtier than when you moved in, accounting for normal use. Request a final walkthrough with your landlord before you leave the keys, as this gives both parties a chance to identify any issues and agree on their status. Provide your landlord with a forwarding address in writing so they can return your deposit by mail. After moving out, your landlord must return your deposit within the state-mandated timeframe (usually 14-30 days) with an itemized statement of any deductions. Keep copies of all maintenance requests you submitted and compare them against any claimed damage. If you believe deductions are improper, you can dispute them in small claims court.
>
> Sources:
> • first_apartment_checklist.txt
> • apartments_com_student_guide.txt
> • tenant_rights_guide.txt

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What should I look for when inspecting an apartment before signing a lease? | Checks for mold, water damage, working locks, functioning appliances, pest evidence, document with photos | Covered kitchen checklist (stove, fridge, dishwasher, outlets) but omitted bathroom, bedroom checks, and red flags like landlord pressure. Cited only one source despite 4 being retrieved. | Relevant | Partially accurate |
| 2 | Can a landlord keep my entire security deposit if I leave the apartment dirty? | Landlord can deduct cleaning costs but must itemize; cannot keep full deposit for normal wear and tear | Returned "I don't have enough information in my documents to answer that." — despite the relevant legal rule existing in tenant_rights_guide.txt | Partially relevant | Inaccurate |
| 3 | What utilities are typically not included in rent for student apartments? | Electricity, internet, renter's insurance commonly excluded; water/trash sometimes included; ask explicitly | Correctly listed electricity, gas/heat, internet, sewer, parking, laundry. Noted water/trash may be included. Cited 4 sources. | Relevant | Accurate |
| 4 | What are common red flags when touring an apartment? | Unresponsive landlord, water damage signs, pressure to sign immediately, unusually low rent, no written lease | Only named one red flag (pressure to sign same day). Retrieved chunks contained more but LLM synthesized a narrow response. | Relevant | Partially accurate |
| 5 | How much of my monthly income should I budget for rent as a student? | 30% rule, note students often need roommates or farther locations to stay within budget | Correctly stated the 30% rule and noted it is a guideline. Cited 3 sources. Did not mention roommates or distance trade-off. | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

"Can a landlord keep my entire security deposit if I leave the apartment dirty?"

**What the system returned:**

"I don't have enough information in my documents to answer that." — despite `tenant_rights_guide.txt` containing this directly: *"Normal wear and tear vs. damage: Landlords can deduct from a deposit for damage beyond normal wear and tear, but not for ordinary use. Normal wear and tear includes minor scuffs, small nail holes, carpet wear from regular foot traffic."*

**Root cause (tied to a specific pipeline stage):**

The failure is at the **retrieval stage**, caused by a vocabulary mismatch between the query and the relevant chunk. The query uses the word "dirty," but the key document (`tenant_rights_guide.txt`) uses the legal term "normal wear and tear" to describe the same concept. The `all-MiniLM-L6-v2` embedding model maps these phrases to different regions of the vector space — "dirty apartment" is semantically closer to cleaning and mess, while "normal wear and tear" is legal/contractual language. The chunk that directly answers the question (the normal wear and tear section) ranked outside the top 5 results, so the model never received the relevant context. The retrieved chunks covered security deposits generally (deposit return timelines, itemization requirements) but didn't include the specific rule about what landlords can and cannot deduct for a dirty unit. With no directly relevant chunk in its context window, the model correctly refused to answer — the grounding worked as intended, but retrieval failed to surface the right content.

**What you would change to fix it:**

Two targeted fixes: (1) **Query expansion** — before embedding the query, rephrase it with synonyms: "dirty apartment" → "normal wear and tear OR cleaning fees OR deposit deduction for cleanliness." This broadens the semantic search to catch legal-register documents. (2) **Increase top-k** — raising k from 5 to 8 would bring more chunks into context, increasing the probability that the wear-and-tear chunk appears. The tradeoff is more noise in the context window, but for a domain with consistent vocabulary mismatches between informal queries and formal document language, broader retrieval is preferable to narrow precision.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

The Evaluation Plan in `planning.md` was the most valuable part of the spec. Writing 5 specific test questions before building anything forced me to think about what "works" means concretely. When Q2 (the security deposit/dirty apartment question) returned a refusal, I immediately knew it was a failure because I had a written expected answer to compare against — the system should have cited the normal wear and tear rule. Without a pre-written evaluation plan, I might have accepted the refusal as reasonable behavior and moved on. The spec also made the failure diagnosable: because I had identified the specific relevant information in advance, I could trace exactly which chunk was missing from retrieval and why.

**One way your implementation diverged from the spec, and why:**

The spec called for `chunk_size = 400 characters` with `overlap = 80 characters`, and I implemented exactly that. However, the failure on Q2 revealed that fixed-character chunking has a structural weakness: it doesn't respect logical boundaries in the source documents. The `tenant_rights_guide.txt` has entries separated by blank lines, each covering a distinct legal concept. A character-based chunker splits across these boundaries regardless of meaning, which is why the "normal wear and tear" rule ended up split between two chunks — neither of which contained enough context to match a query about "dirty apartments." If I were rebuilding, I would use paragraph-based chunking (split on double newlines) for structured guide documents, reserving character-based chunking for the review files where paragraph boundaries are inconsistent. The spec did not anticipate this distinction because I hadn't read the documents closely enough when writing it.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* The Chunking Strategy section from `planning.md` (chunk_size=400 chars, overlap=80 chars, two document types: short reviews and long guides), the Documents section listing 12 `.txt` files, and asked Claude to implement `load_documents(folder_path)` and `chunk_text(text, chunk_size, overlap)` functions for `ingest.py`.
- *What it produced:* A `load_documents()` function that reads `.txt` files and returns `{text, source}` dicts, and a `chunk_text()` function using a sliding window with character-based splitting. It also included a `clean_text()` function that stripped HTML tags and decoded HTML entities, which I hadn't explicitly asked for but was clearly needed given that some source text might contain web-copy artifacts.
- *What I changed or overrode:* The generated `chunk_text()` function used `text[start:end]` without calling `.strip()` on the result, which left leading/trailing whitespace on some chunks. I added `.strip()` to the chunk before appending it, and added a `len(chunk) > 0` guard to prevent empty chunks from entering the corpus. I also added the overlap verification section to `__main__` to test that adjacent chunks actually share text, which the original code did not include.

**Instance 2**

- *What I gave the AI:* The Retrieval Approach section from `planning.md` (all-MiniLM-L6-v2, top-k=5, cosine similarity), the Architecture ASCII diagram labeling ChromaDB as the vector store, and asked Claude to implement `build_index(corpus)` and `retrieve(query, collection, model, k)` functions for `embed.py`.
- *What it produced:* A complete `build_index()` function that embedded chunks using `SentenceTransformer`, created a ChromaDB persistent collection with cosine similarity, and upserted all chunks with metadata. The `retrieve()` function embedded the query and called `collection.query()`, returning documents, metadata, and distances.
- *What I changed or overrode:* The generated code used ChromaDB's default L2 (Euclidean) distance metric. I overrode this by explicitly setting `metadata={"hnsw:space": "cosine"}` on collection creation, because cosine similarity is more appropriate for text embeddings — it measures directional similarity rather than magnitude, which is what matters when comparing meaning. I also added a `delete_collection` call before `create_collection` so that re-running the script rebuilds the index cleanly rather than accumulating duplicate entries.
