# M1: Monorepo Setup + Local Dev Environment

> **Type:** action
> **Service:** monorepo
> **Owner:** Both (AI Engineer & Software Engineer)
> **Maps to deliverable:** D5 (from DELIVERY-PLAN.md)
> **Prerequisite:** ADR-0001, ADR-0003, ADR-0004
> **Unblocks:** AI-1, API-1, WEB-1
> **Status:** done
> **Date:** 2026-08-11

---

## 1. Problem Statement

Without a clear monorepo structure and unified environment configuration, the AI Engineer and Software Engineer cannot work in parallel without risk of merge conflicts, missing environment variables, or mismatched directory conventions.

Spec M1 establishes the foundational monorepo layout (`ai/`, `apps/api/`, `apps/web/`, `docs/`), root environment templates (`.env.example`), and validates the Python development toolchain (`uv`) to unblock parallel development across AI, backend, and frontend streams.

---

## 2. Current State

- `ai/` folder exists with `pyproject.toml` and `uv.lock` configured for Python 3.11+ using `uv`. Core dependencies (`langchain`, `langchain-google-genai`, `langgraph`, `chromadb`, `sentence-transformers`, `ragas`, `pytest`, `python-dotenv`) are installed in `.venv`.
- `docs/` contains specs, ADRs (`0001`, `0003`, `0004`), and delivery planning documents.
- Root `.env.example` does not exist yet.
- `apps/api/` (FastAPI) and `apps/web/` (React) directories do not exist yet.

---

## 3. Proposed Design

### Target Monorepo Structure

```
ai-customer-support/
├── .env.example            # Centralized environment variable template
├── README.md               # Root README with project overview & quickstart
├── ai/                     # AI Pipeline (Python + uv)
│   ├── pyproject.toml
│   ├── uv.lock
│   └── README.md
├── apps/
│   ├── api/                # Backend API (FastAPI + SQLite placeholder)
│   │   └── README.md
│   └── web/                # Frontend UI (React + Tailwind placeholder)
│       └── README.md
└── docs/                   # Documentation, specs, and ADRs
    ├── adr/
    ├── specs/
    └── DELIVERY-PLAN.md
```

### Environment Configuration (`.env.example`)

```bash
# LLM Provider Keys
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here

# Vector DB & Data Paths
CHROMADB_PATH=./ai/chroma_db
DATASET_PATH=./ai/data

# Backend & Server Settings
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
DATABASE_URL=sqlite:///./apps/api/app.db
```

---

## 4. Build Plan

### Phase 1: Environment Template & Directory Structure (15 min)

1. Create `.env.example` at the repository root with standard variable keys for LLMs, ChromaDB, and backend services.
2. Create `apps/api/README.md` placeholder to establish the backend workspace directory.
3. Create `apps/web/README.md` placeholder to establish the frontend workspace directory.

### Phase 2: Python Environment Verification & Test Setup (15 min)

1. Verify Python virtual environment setup using `uv sync` inside `ai/`.
2. Execute initial `pytest` run in `ai/` to verify test suite readiness.

---

## 5. Verification Checklist

- [x] `.env.example` created at repository root.
- [x] `apps/api/` directory established with initial `README.md`.
- [x] `apps/web/` directory established with initial `README.md`.
- [x] Python `uv` environment verified in `ai/` (`uv sync`).
- [x] `pytest` verified working in `ai/`.
- [x] `SPEC-INDEX.md` updated to mark Spec M1 as done.
- [x] `DELIVERY-STATUS.md` updated to mark D5 as shipped.

---

## 6. Out of Scope

- **FastAPI route implementation** — handled in `API-1`.
- **React frontend initialization** — handled in `WEB-1`.
- **SQLite schema creation** — handled in `API-1` / `ADR-0002`.

---

## 7. Cross-References

- **Prerequisite(s):** [`ADR-0001`](../adr/0001-use-gemini-free-tier.md), [`ADR-0003`](../adr/0003-rag-over-finetuning.md), [`ADR-0004`](../adr/0004-langgraph-orchestration.md)
- **Unblocks:** [`AI-1`](./SPEC-INDEX.md#L44), [`API-1`](./SPEC-INDEX.md#L53), [`WEB-1`](./SPEC-INDEX.md#L54)
- **Mapped Deliverable:** D5 from [`DELIVERY-PLAN.md`](../DELIVERY-PLAN.md#L43)
