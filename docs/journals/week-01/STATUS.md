---
session: CS01
date: 2026-08-21
week: "01"
title: AI Foundations & RAG Retrieval Pipeline (Specs AI-1 & AI-2)
---

# CS01 — August 21, 2026: AI Pipeline Foundations & RAG Retrieval

## Goal
Build the core data ingestion pipeline, ChromaDB vector store, RAG retrieval engine, and multi-LLM fallback client, establishing the complete AI foundation for the Customer Support AI project.

## Outcome
- **Spec AI-1 Shipped (Deliverable D6):** Data ingestion pipeline with HuggingFace Bitext dataset, offline seed fallback, and 3 persistent ChromaDB collections (`billing_kb`, `technical_kb`, `general_kb`).
- **Spec AI-2 Shipped (Deliverable D7):** RAG retrieval pipeline with semantic similarity search, prompt assembly with specialist personas, and multi-LLM fallback client (Gemini ➔ Groq ➔ Offline).
- **16 / 16 Unit Tests Passing:** 100% automated test coverage across data loader, ChromaDB manager, LLM client, and RAG retriever.
- **Developer Experience:** Created `SETUP_GUIDE.md`, registered Jupyter kernel `Python (Customer Support AI)`, and standardized team Git workflow in `GIT_WORKFLOW.md`.

---

## What Was Done

### 1. Spec AI-1: Data Ingestion & ChromaDB Vector Store
- Created `ai/src/config.py`: Centralized configuration for ChromaDB paths, intent categorization mappings (`BILLING_INTENTS`, `TECHNICAL_INTENTS`, `GENERAL_INTENTS`), and embedding model settings.
- Created `ai/src/pipelines/data_loader.py`: Ingestion logic to stream and clean Bitext customer support dataset with an offline seed fallback (`get_seed_dataset()`).
- Created `ai/src/pipelines/embeddings.py`: Wrapped `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional dense vectors on CPU, 80MB footprint per ADR-0003).
- Created `ai/src/pipelines/knowledge_base.py`: ChromaDB `PersistentClient` maintaining `billing_kb`, `technical_kb`, and `general_kb`.
- Created `ai/src/scripts/ingest.py`: CLI ingestion tool (`uv run python -m src.scripts.ingest`).

### 2. Spec AI-2: RAG Retrieval Pipeline & Multi-LLM Fallback Client
- Created `ai/src/pipelines/llm_client.py`: Multi-provider fallback chain per ADR-0001 (Google Gemini Free Tier ➔ Groq API Llama 3 ➔ Offline deterministic fallback).
- Created `ai/src/pipelines/retriever.py`: `RAGRetriever` connecting user queries to domain ChromaDB collections, filtering by relevance score, formatting prompts with specialist personas & conversation history, and extracting structured source citations.

### 3. Testing & Tooling
- Fixed ChromaDB v0.5+ embedding function interface protocol and Windows SQLite temporary file locks in `ai/tests/test_knowledge_base.py`.
- Created comprehensive test suites in `ai/tests/test_data_loader.py`, `ai/tests/test_knowledge_base.py`, `ai/tests/test_llm_client.py`, and `ai/tests/test_retriever.py`.
- Configured `[tool.pytest.ini_options]` in `ai/pyproject.toml` with `pythonpath = ["."]` for seamless test discovery.

### 4. Documentation & Standards
- Created `docs/GIT_WORKFLOW.md` establishing team feature-branching lifecycle, atomic PR rules, and PR naming standards (`<type>(<scope>): [<spec-code>] <summary>`).
- Created `ai/SETUP_GUIDE.md` for virtual environment (`uv`), Jupyter kernel setup, and test execution.

---

## Files Changed

### AI Pipeline & Tests
- `ai/src/config.py` — Config & intent sets
- `ai/src/pipelines/__init__.py` — Package exports
- `ai/src/pipelines/data_loader.py` — Dataset ETL & domain categorizer
- `ai/src/pipelines/embeddings.py` — SentenceTransformer embedding wrapper
- `ai/src/pipelines/knowledge_base.py` — ChromaDB persistent manager
- `ai/src/pipelines/llm_client.py` — Multi-LLM fallback client (Gemini ➔ Groq ➔ Offline)
- `ai/src/pipelines/retriever.py` — RAG retrieval and citation engine
- `ai/src/scripts/ingest.py` — Ingestion CLI runner
- `ai/tests/test_data_loader.py` — Unit tests for data loader (6 tests)
- `ai/tests/test_knowledge_base.py` — Unit tests for vector store (2 tests)
- `ai/tests/test_llm_client.py` — Unit tests for LLM failover chain (4 tests)
- `ai/tests/test_retriever.py` — Unit tests for RAG retriever & citations (4 tests)
- `ai/SETUP_GUIDE.md` — Environment and Jupyter setup manual
- `ai/sandbox.ipynb` — Interactive developer exploration notebook
- `ai/pyproject.toml` & `ai/uv.lock` — Updated with pytest config & ipykernel

### Specs & Governance Docs
- `docs/specs/2026-08-11-spec-AI1-data-ingestion-pipeline.md` — Spec AI-1
- `docs/specs/2026-08-21-spec-AI2-rag-retrieval-pipeline.md` — Spec AI-2
- `docs/GIT_WORKFLOW.md` — Team Git branching and PR naming standards
- `docs/specs/SPEC-INDEX.md` — Updated progress (M1, AI-1, AI-2 done)
- `docs/specs/SPEC-CONTEXT.md` — Session resumption snapshot
- `docs/DELIVERY-STATUS.md` — Shipped Deliverables D5, D6, D7 (6 / 14 shipped)
- `docs/journals/week-01/STATUS.md` — This file

---

## References
- Spec AI-1: [`docs/specs/2026-08-11-spec-AI1-data-ingestion-pipeline.md`](../../specs/2026-08-11-spec-AI1-data-ingestion-pipeline.md)
- Spec AI-2: [`docs/specs/2026-08-21-spec-AI2-rag-retrieval-pipeline.md`](../../specs/2026-08-21-spec-AI2-rag-retrieval-pipeline.md)
- ADR-0001 (Gemini Free Tier): [`docs/adr/0001-use-gemini-free-tier.md`](../../adr/0001-use-gemini-free-tier.md)
- ADR-0003 (RAG Architecture): [`docs/adr/0003-rag-over-finetuning.md`](../../adr/0003-rag-over-finetuning.md)
- Delivery Plan: [`docs/DELIVERY-PLAN.md`](../../DELIVERY-PLAN.md)
