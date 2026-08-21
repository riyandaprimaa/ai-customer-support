# AI-2: RAG Retrieval Pipeline & Multi-LLM Fallback Client

> **Type:** feature
> **Service:** ai
> **Owner:** AI Engineer
> **Maps to deliverable:** D7 (from DELIVERY-PLAN.md)
> **Prerequisite:** Spec AI-1
> **Unblocks:** AI-3 (Orchestrator Agent)
> **Status:** done
> **Date:** 2026-08-21

---

## 1. Problem Statement

With Spec AI-1 completed, our domain customer support FAQ data is indexed into 3 persistent ChromaDB collections (`billing_kb`, `technical_kb`, `general_kb`). However, there is no retrieval service or LLM integration to answer user queries with grounded context.

Without Spec AI-2:
1. Agents cannot retrieve domain-specific context from ChromaDB with relevance filtering and formatted citations.
2. Single-provider LLM API calls are vulnerable to rate limits (e.g. Gemini Free Tier 15 RPM cap during live demos), leading to service downtime.

Spec AI-2 establishes:
- The **RAG Retrieval Engine** with similarity thresholding, top-$k$ document ranking, and source citation extraction.
- The **Multi-LLM Fallback Client** implementing ADR-0001 (Google Gemini Free Tier ➔ Groq Llama 3 ➔ Ollama Local Offline).

---

## 2. Current State

- **ChromaDB Vector Store:** Populated with `billing_kb`, `technical_kb`, `general_kb` collections using `all-MiniLM-L6-v2` embeddings (`ai/src/pipelines/knowledge_base.py`).
- **Dependencies Installed:** `langchain`, `langchain-google-genai`, `langchain-groq`, `sentence-transformers`, `chromadb` in `ai/pyproject.toml`.
- **Environment:** Configured in `ai/src/config.py` with `.env` path resolution.

---

## 3. Proposed Design

### Pipeline Architecture

```
User Query + Category ("billing" | "technical" | "general")
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. RAG Retriever (retriever.py)                             │
│    - Queries ChromaDB collection for top-k chunks           │
│    - Filters out low-confidence results (score < min_score) │
│    - Extracts structured source citations                   │
└──────────────────────────────┬──────────────────────────────┘
                               │ (Context String + Citations)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Prompt Assembly (prompts.py)                             │
│    - System Persona (Customer Support Specialist)           │
│    - Retrieved Context (FAQ Question & Answer pairs)        │
│    - Conversation History (sliding window)                  │
│    - User Question                                          │
└──────────────────────────────┬──────────────────────────────┘
                               │ (Formatted Prompt)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Multi-LLM Fallback Client (llm_client.py) [ADR-0001]     │
│                                                             │
│    [1. Google Gemini 1.5/2.0 Flash] (Primary)               │
│          │ (fail / rate limit 429)                          │
│          ▼                                                  │
│    [2. Groq API — Llama 3 70B/8B] (Fallback 1)              │
│          │ (fail / offline)                                 │
│          ▼                                                  │
│    [3. Ollama / Static Fallback] (Offline Fallback 2)       │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
{ "reply": "...", "sources": [...], "provider": "gemini", "confidence": 0.92 }
```

### Return Shape Specification

```python
{
    "reply": str,                     # Generated LLM answer grounded in context
    "sources": list[dict[str, Any]],  # [{ "query": str, "response": str, "score": float, "category": str }]
    "provider_used": str,             # "gemini" | "groq" | "ollama" | "fallback"
    "has_context": bool               # True if relevant context was found in ChromaDB
}
```

---

## 4. Build Plan

### Phase 1: Multi-LLM Provider Client (`ai/src/pipelines/llm_client.py`) (45 min)
1. Implement `LLMClient` with fallback chain logic:
   - Primary: `ChatGoogleGenerativeAI(model="gemini-1.5-flash")` or `gemini-2.0-flash`.
   - Fallback 1: `ChatGroq(model="llama-3.1-8b-instant" / "llama3-70b-8192")`.
   - Fallback 2: Local Ollama or deterministic rule-based template if offline.
2. Support configurable temperature, streaming flag, and timeout handling.

### Phase 2: RAG Retriever & Prompt Assembly (`ai/src/pipelines/retriever.py`) (45 min)
1. Implement `RAGRetriever`:
   - `retrieve_context(query, category, top_k=3, min_score=0.4)`
   - `format_prompt(query, context_chunks, conversation_history, system_instruction)`
   - `answer_query(query, category, conversation_history=None)`
2. Add structured source citation formatting.

### Phase 3: Unit Tests & Verification (`ai/tests/test_retriever.py`, `test_llm_client.py`) (30 min)
1. Write mock and live unit tests for LLM provider failover.
2. Write unit tests for RAG retrieval relevance scoring and citation outputs.
3. Verify test suite passes with `uv run pytest -v`.

---

## 5. Verification Checklist

- [x] `ai/src/pipelines/llm_client.py` implements the triple fallback chain (Gemini ➔ Groq ➔ Offline).
- [x] `ai/src/pipelines/retriever.py` correctly retrieves and formats domain context from ChromaDB.
- [x] Source citations are properly extracted with relevance scores.
- [x] Unit tests written in `ai/tests/test_retriever.py` and `ai/tests/test_llm_client.py`.
- [x] All 16 unit tests pass cleanly with `uv run pytest -v`.

---

## 6. Out of Scope

- **Intent classification routing (Orchestrator Agent)** — Handled in `AI-3`.
- **LangGraph multi-agent state graph** — Handled in `AI-4`.
- **FastAPI HTTP REST & SSE streaming endpoints** — Handled in `API-1` & `INT-1`.

---

## 7. Cross-References

- **Prerequisite(s):** [`2026-08-11-spec-AI1-data-ingestion-pipeline.md`](./2026-08-11-spec-AI1-data-ingestion-pipeline.md)
- **Unblocks:** [`AI-3 (Orchestrator Agent)`](./SPEC-INDEX.md#L46)
- **ADRs:** [`ADR-0001 (Gemini Free Tier & Fallbacks)`](../adr/0001-use-gemini-free-tier.md), [`ADR-0003 (RAG Architecture)`](../adr/0003-rag-over-finetuning.md)
