# ADR-0003: RAG over Fine-Tuning for Customer Support Knowledge Base

> **Status:** Accepted
> **Date:** 2026-08-11
> **Decision makers:** AI Engineer (team consensus)

---

## Context

We are building the knowledge retrieval engine for a multi-agent customer support AI system. The AI needs to answer questions accurately based on company FAQs, policies, and product guides (using the Bitext customer support dataset).

We evaluated two technical approaches:
1. **Fine-Tuning:** Training a custom open-weight LLM (e.g., Llama 3 / Mistral 7B) on the customer support dataset.
2. **Retrieval-Augmented Generation (RAG):** Embedding the FAQ dataset into a vector database (ChromaDB) and retrieving relevant chunks at query time to feed into LLM prompts (Gemini 2.0 Flash / Groq).

Forces at play:
- **Hardware constraints:** Neither team member has a dedicated GPU. Fine-tuning a 7B LLM requires significant GPU VRAM and hours of compute.
- **Knowledge updates:** Customer support FAQs change frequently (pricing, return policies, feature updates). Fine-tuning requires re-training the whole model every time a policy changes.
- **Hallucinations:** Fine-tuned LLMs can fabricate non-existent policies when uncertain. RAG grounds responses in exact retrieved documents with verifiable source citations.
- **Cost:** Fine-tuning on cloud GPUs (RunPod/Lambda) costs money, violating our $0 budget constraint.

---

## Decision

**Use RAG (Retrieval-Augmented Generation) with ChromaDB and `all-MiniLM-L6-v2` embeddings as the knowledge retrieval system, rather than fine-tuning a custom LLM.**

Our RAG stack architecture:
- **Vector DB:** ChromaDB (persistent local vector store in `./chroma_data/`)
- **Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2` (runs on CPU, only 80MB, 384 dimensions)
- **Chunking Strategy:** Recursive character text splitter (~500 tokens per chunk with 50-token overlap)
- **Collections:** 3 domain-isolated collections (`billing_kb`, `technical_kb`, `general_kb`)
- **Retrieval:** Top-k=5 similarity search with relevance scoring
- **LLM Generator:** Gemini 2.0 Flash (primary) / Groq Llama 3.3 (fallback)

---

## Consequences

### What becomes easier
- **$0 compute cost:** Generating embeddings for 25,000+ FAQ items on CPU takes ~2 minutes.
- **Instant knowledge updates:** Updating an FAQ item is a simple DB insert/update in ChromaDB — zero retraining time.
- **Source Citations:** Users can see exact source documents below every AI reply.
- **Reduced Hallucinations:** Prompts instruct the LLM to answer ONLY using retrieved context.

### What becomes harder
- **Retrieval Quality Dependency:** If ChromaDB fails to retrieve the correct FAQ chunk, the LLM cannot answer properly. Mitigation: tune chunk size (500 tokens) and top-k parameter (k=5), and add fallback handling.

---

## References

- HuggingFace `sentence-transformers/all-MiniLM-L6-v2`
- ChromaDB Documentation
- ADR-0001 (Gemini Free Tier)
- ADR-0004 (LangGraph Orchestration)
