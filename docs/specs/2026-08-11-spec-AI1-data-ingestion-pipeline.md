# AI-1: Data Ingestion + Embeddings + ChromaDB Pipeline

> **Type:** feature
> **Service:** ai
> **Owner:** AI Engineer
> **Maps to deliverable:** D6 (from DELIVERY-PLAN.md)
> **Prerequisite:** Spec M1
> **Unblocks:** AI-2 (RAG Retrieval Pipeline)
> **Status:** done
> **Date:** 2026-08-11

---

## 1. Problem Statement

To provide accurate customer support responses via RAG (Retrieval-Augmented Generation), our multi-agent chatbot requires a clean, structured, and searchable knowledge base of domain-specific customer support FAQs.

Without a dedicated data ingestion pipeline, domain knowledge remains unindexed, preventing vector similarity search and forcing specialist agents to rely solely on base LLM knowledge.

Spec AI-1 builds the data pipeline that ingests the Bitext customer support dataset, categorizes records into agent domains (`billing`, `technical`, `general`), computes embeddings using `sentence-transformers/all-MiniLM-L6-v2`, and populates persistent vector collections in **ChromaDB**.

---

## 2. Current State

- Spec M1 established the Python environment in `ai/` using `uv` with `sentence-transformers`, `chromadb`, `datasets`, and `pytest`.
- Monorepo directory structure is established (`ai/`, `apps/api/`, `apps/web/`, `.env.example`).
- Spec AI-1 built `ai/src/config.py`, `ai/src/pipelines/data_loader.py`, `ai/src/pipelines/embeddings.py`, `ai/src/pipelines/knowledge_base.py`, and `ai/src/scripts/ingest.py`.

---

## 3. Proposed Design

### Pipeline Architecture

```
[Bitext HF Dataset] 
       │
       ▼
[data_loader.py] ──▶ Categorize intents: {billing, technical, general}
       │
       ▼
[embeddings.py] ──▶ Encode text via all-MiniLM-L6-v2 (CPU, 384-dim)
       │
       ▼
[knowledge_base.py] ──▶ Store vectors in ChromaDB persistent collections
                         (billing_kb, technical_kb, general_kb)
```

### Categorization Mapping

- **Billing (`billing_kb`):** intents related to payment, refund, invoice, subscription, order status, pricing.
- **Technical (`technical_kb`):** intents related to account setup, bugs, password reset, error messages, compatibility.
- **General (`general_kb`):** intents related to greetings, feedback, general inquiries, store hours, contact info.

---

## 4. Build Plan

### Phase 1: Pipeline Module Architecture (Small, ~45 min)

1. Create `ai/src/config.py` for persistent settings (`CHROMADB_PATH`, model name, intent mappings).
2. Create `ai/src/pipelines/data_loader.py` to fetch, clean, and split dataset into 3 domain categories.
3. Create `ai/src/pipelines/embeddings.py` wrapping SentenceTransformers (`all-MiniLM-L6-v2`).
4. Create `ai/src/pipelines/knowledge_base.py` wrapping ChromaDB persistent client and collection management.

### Phase 2: Ingestion CLI Script & Unit Tests (Small, ~30 min)

1. Create `ai/src/scripts/ingest.py` entry point (`uv run python -m src.scripts.ingest`).
2. Write unit tests in `ai/tests/test_data_loader.py` and `ai/tests/test_knowledge_base.py`.
3. Verify test suite and execute ingestion pipeline.

---

## 5. Verification Checklist

- [x] `ai/src/config.py` configured with default environment paths.
- [x] `ai/src/pipelines/data_loader.py` correctly splits dataset into 3 domain categories.
- [x] `ai/src/pipelines/knowledge_base.py` initializes ChromaDB persistent storage.
- [x] Unit tests in `ai/tests/test_data_loader.py` and `ai/tests/test_knowledge_base.py`.
- [x] Ingestion script `uv run python -m src.scripts.ingest` created and ready to run.
- [x] ChromaDB collections (`billing_kb`, `technical_kb`, `general_kb`) persistent configuration ready.

---

## 6. Out of Scope

- **RAG similarity search query function** — implemented in `AI-2`.
- **LangGraph agent nodes** — implemented in `AI-3` & `AI-4`.
- **FastAPI database integration** — implemented in `API-1`.

---

## 7. Cross-References

- **Prerequisite(s):** [`2026-08-11-spec-M1-monorepo-dev-environment.md`](./2026-08-11-spec-M1-monorepo-dev-environment.md)
- **Unblocks:** [`AI-2 (RAG Retrieval Pipeline)`](./SPEC-INDEX.md#L45)
- **ADRs:** [`ADR-0003 (RAG over Fine-Tuning)`](../adr/0003-rag-over-finetuning.md)
