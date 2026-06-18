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

**How source attribution is surfaced in the response:**

---

## Example Responses

<!-- Provide at least 2 grounded responses (query + response + source attribution)
     and 1 out-of-scope query showing your system's refusal.
     All entries must be text — not screenshots. -->

**Grounded response 1**

Query:

Response:

Source attribution:

---

**Grounded response 2**

Query:

Response:

Source attribution:

---

**Out-of-scope query**

Query:

System response (refusal):

---

## Query Interface

<!-- Describe your query interface: what are the input fields, what does the output look like?
     Then provide a complete sample interaction transcript showing a real exchange. -->

**Input fields:**

**Output format:**

---

**Sample Interaction Transcript**

<!-- Show a complete query → response exchange as it actually appears in your interface.
     Must be text — not a screenshot. -->

> **User:** 

> **System:** 

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

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

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

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

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
