# Spec Index — Customer Support AI

> **The canonical tracker for every spec.** One row per spec; status, prerequisites, dependents, and mapped deliverable. Read this before opening any spec file.
>
> **First time resuming work?** Start with [`SPEC-CONTEXT.md`](./SPEC-CONTEXT.md) — the orientation, status snapshot, and process checklist.
>
> **Companion to:** [`../DELIVERY-PLAN.md`](../DELIVERY-PLAN.md) (what specs implement) · [`TEMPLATE.md`](./TEMPLATE.md) (how to write a spec)

**Snapshot date:** 2026-08-11 (ADR-0003 & ADR-0004 accepted)

---

## Legend

- **Status:** ⬜ not started · 🟨 in progress · 🟩 done · 🟥 blocked · ⏸️ deferred
- **Service codes:** `AI` ai pipeline · `API` backend · `WEB` frontend · `M` monorepo · `INT` integration · `EVAL` evaluation · `DEPLOY` deployment
- **D#:** deliverable from `DELIVERY-PLAN.md` (D1–D14). Blank = adjacent work.

---

## Architecture Decision Records (ADRs)

| # | Title | Status | Date | File |
|---|---|---|---|---|
| **ADR-0001** | Use Google Gemini Free Tier as Primary LLM | 🟩 Accepted | 2026-08-11 | [`../adr/0001-use-gemini-free-tier.md`](../adr/0001-use-gemini-free-tier.md) |
| **ADR-0002** | SQLite over Postgres for zero-overhead development | ⬜ To write (SWE) | — | — |
| **ADR-0003** | RAG over Fine-Tuning for Customer Support Knowledge Base | 🟩 Accepted | 2026-08-11 | [`../adr/0003-rag-over-finetuning.md`](../adr/0003-rag-over-finetuning.md) |
| **ADR-0004** | LangGraph for Multi-Agent Orchestration & Memory | 🟩 Accepted | 2026-08-11 | [`../adr/0004-langgraph-orchestration.md`](../adr/0004-langgraph-orchestration.md) |

---

## Spec List (authoring order = dependency order)

### Phase 0 — Foundations

| # | Code | Title | Status | Prereq | Unblocks | D# | Owner | File |
|---|---|---|---|---|---|---|---|---|
| 1 | **M1** | Monorepo setup + local dev environment | 🟩 | ADR-0001–0004 | AI-1, API-1, WEB-1 | D5 | Both | [`2026-08-11-spec-M1-monorepo-dev-environment.md`](./2026-08-11-spec-M1-monorepo-dev-environment.md) |

### Phase 1 — AI Pipeline

| # | Code | Title | Status | Prereq | Unblocks | D# | Owner | File |
|---|---|---|---|---|---|---|---|---|
| 2 | **AI-1** | Data ingestion + embeddings + ChromaDB | ⬜ | M1 | AI-2 | D6 | AI Eng | *to write* |
| 3 | **AI-2** | RAG retrieval pipeline | ⬜ | AI-1 | AI-3 | D7 | AI Eng | *to write* |
| 4 | **AI-3** | Orchestrator agent (intent classification) | ⬜ | AI-2 | AI-4 | D8 | AI Eng | *to write* |
| 5 | **AI-4** | 3 specialist agents + conversation memory | ⬜ | AI-3 | INT-1 | D9 | AI Eng | *to write* |

### Phase 1 — Backend + Frontend (parallel with AI)

| # | Code | Title | Status | Prereq | Unblocks | D# | Owner | File |
|---|---|---|---|---|---|---|---|---|
| 6 | **API-1** | FastAPI backend (chat API, WebSocket, SQLite) | ⬜ | M1 | INT-1 | D10 | SWE | *to write* |
| 7 | **WEB-1** | React chat UI (messages, streaming, dark mode) | ⬜ | M1 | INT-1 | D11 | SWE | *to write* |

### Phase 2 — Integration

| # | Code | Title | Status | Prereq | Unblocks | D# | Owner | File |
|---|---|---|---|---|---|---|---|---|
| 8 | **INT-1** | AI ↔ API integration (AIService, streaming, E2E) | ⬜ | AI-4, API-1, WEB-1 | EVAL-1, DEPLOY-1 | D12 | Both | *to write* |

### Phase 3 — Evaluation + Deployment

| # | Code | Title | Status | Prereq | Unblocks | D# | Owner | File |
|---|---|---|---|---|---|---|---|---|
| 9 | **EVAL-1** | Evaluation suite (RAGAS, intent accuracy, latency) | ⬜ | INT-1 | — | D13 | AI Eng | *to write* |
| 10 | **DEPLOY-1** | Production deploy (Docker, Render, Vercel, CI) | ⬜ | INT-1 | — | D14 | SWE | *to write* |

---

## Dependency Graph

```
ADR-0001 ─┐
ADR-0002 ─┤
ADR-0003 ─┼──▶ M1 (local dev setup)
ADR-0004 ─┘        │
                    ├──▶ AI-1 ──▶ AI-2 ──▶ AI-3 ──▶ AI-4 ──┐
                    │                                        │
                    ├──▶ API-1 ──────────────────────────────┤
                    │                                        ├──▶ INT-1 ──┬──▶ EVAL-1
                    └──▶ WEB-1 ──────────────────────────────┘            └──▶ DEPLOY-1
```
