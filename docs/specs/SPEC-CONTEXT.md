# Spec Authoring — Context for Session Resumption

> **Purpose:** The single file a future session (human or AI agent) reads to resume work where the last session left off. Read this first; then drill into linked files for grounding. Keep this file evergreen — update it at the end of every coding session.
>
> **Snapshot date:** 2026-08-11 (ADR-0003 & ADR-0004 completed on branch `feature/ai-phase0-adrs`)
> **Maintained by:** AI Engineer

---

## 0. The 60-second orientation

**Customer Support AI** is a multi-agent chatbot for customer support. Architecture:

```
User (React) → FastAPI Backend → Orchestrator Agent → {Billing | Technical | General} Agent
                                                     → RAG Knowledge Base (ChromaDB)
                                                     → LLM (Gemini free tier)
```

**Team:** 2 fresh graduates — AI Engineer + Software Engineer.
**Budget:** $0 — all tools are free or open-source.
**Hardware:** Local PCs, no GPU.
**IDE:** Antigravity (agentic coding).
**Goal:** Working portfolio project with live deployment.

---

## 1. Where to find things (read these first)

| File | Read it for |
|---|---|
| [`../DELIVERY-PLAN.md`](../DELIVERY-PLAN.md) | The delivery plan + deliverables (D1–D14) |
| [`../DELIVERY-STATUS.md`](../DELIVERY-STATUS.md) | Live progress checklist |
| [`SPEC-INDEX.md`](./SPEC-INDEX.md) | **Master spec tracker.** One row per spec: status, prereqs, deliverable |
| [`TEMPLATE.md`](./TEMPLATE.md) | How to write a spec (7 required sections) |
| [`../SYSTEM_ARCHITECTURE.md`](../SYSTEM_ARCHITECTURE.md) | The system architecture source of truth |
| [`../adr/README.md`](../adr/README.md) | ADR index — all architectural decisions |
| [`../integrations/api-contract.md`](../integrations/api-contract.md) | API contract between AI pipeline and backend |

---

## 2. Status snapshot (update after every session)

### Done

| Item | Status | Date |
|---|---|---|
| Project initialization (runbook scaffolding) | 🟩 | 2026-08-11 |
| ADR-0001 — Use Gemini free tier | 🟩 | 2026-08-11 |
| ADR-0003 — RAG over Fine-Tuning | 🟩 | 2026-08-11 |
| ADR-0004 — LangGraph for Multi-Agent Orchestration | 🟩 | 2026-08-11 |

### In progress

- Branch `feature/ai-phase0-adrs` active — ready to push and open Pull Request for D3 & D4.

### What was learned

- **AI Phase 0 ADRs complete:** Gemini API (ADR-0001), RAG with ChromaDB (ADR-0003), and LangGraph StateGraph (ADR-0004) lock the AI engineering architecture.
- **RAG embedding choice:** `sentence-transformers/all-MiniLM-L6-v2` chosen for 80MB lightweight CPU footprint.

---

## 3. Locked decisions that constrain every spec

| # | Decision (ADR) | Affects |
|---|---|---|
| ADR-0001 | Gemini free tier as primary LLM; Groq fallback; Ollama offline | All AI-* specs |
| ADR-0002 | SQLite over Postgres (zero overhead) | API-1, any DB-touching specs |
| ADR-0003 | RAG over fine-tuning (no GPU, ChromaDB vector store) | AI-1, AI-2, EVAL-1 |
| ADR-0004 | LangGraph StateGraph for multi-agent routing & memory | AI-3, AI-4 |

---

## 4. Process for the AI agent (one spec per turn)

1. **Read this file** end-to-end.
2. **Read `SPEC-INDEX.md`** — check current state of every spec row.
3. **Read `DELIVERY-STATUS.md`** — confirm no deliverables shifted status externally.
4. **Identify the next spec** per the dependency graph in SPEC-INDEX.
5. **Draft the spec** at `docs/specs/YYYY-MM-DD-spec-[CODE][N]-[theme].md` following `TEMPLATE.md`.
6. **Update `SPEC-INDEX.md`** — flip status to 🟨.
7. **Execute the spec** — write code per the build plan.
8. **Run the verification checklist** — all items must be checked.
9. **Update this file** — refresh §2 status snapshot.
10. **Update `DELIVERY-STATUS.md`** if a deliverable shipped.
11. **Commit** with a clear message identifying the spec code.
