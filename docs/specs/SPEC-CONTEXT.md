# Spec Authoring — Context for Session Resumption

> **Purpose:** The single file a future session (human or AI agent) reads to resume work where the last session left off. Read this first; then drill into linked files for grounding. Keep this file evergreen — update it at the end of every coding session.
>
> **Snapshot date:** 2026-08-11 (project initialization)
> **Maintained by:** Whomever is driving spec authoring. This is a living document, not an archive.

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

### In progress

*Nothing yet — project just initialized.*

### What was learned

*Update this section as you discover gotchas, bugs, or important decisions during execution.*

---

## 3. Locked decisions that constrain every spec

| # | Decision (ADR) | Affects |
|---|---|---|
| ADR-0001 | Gemini free tier as primary LLM; Groq fallback; Ollama offline | All AI-* specs |
| ADR-0002 | SQLite over Postgres (zero overhead) | API-1, any DB-touching specs |
| ADR-0003 | RAG over fine-tuning (no GPU) | AI-1, AI-2, EVAL-1 |
| ADR-0004 | LangGraph for multi-agent orchestration | AI-3, AI-4 |

---

## 4. Process for the AI agent (one spec per turn)

1. **Read this file** end-to-end.
2. **Read `SPEC-INDEX.md`** — check current state of every spec row.
3. **Read `DELIVERY-STATUS.md`** — confirm no deliverables shifted status externally.
4. **Identify the next spec** per the dependency graph in SPEC-INDEX.
5. **Discuss scope** before drafting (use Antigravity chat to lock decisions).
6. **Draft the spec** at `docs/specs/YYYY-MM-DD-spec-[CODE][N]-[theme].md` following `TEMPLATE.md`.
7. **Update `SPEC-INDEX.md`** — flip status to 🟨.
8. **Execute the spec** — write code per the build plan.
9. **Run the verification checklist** — all items must be checked.
10. **Update this file** — refresh §2 status snapshot.
11. **Update `DELIVERY-STATUS.md`** if a deliverable shipped.
12. **Commit** with a clear message identifying the spec code.

---

## 5. Gotchas (things that will bite you if you don't know them)

### Gemini rate limits
- Free tier is ~15 RPM. During heavy testing, you WILL hit 429 errors. The fallback to Groq (ADR-0001) handles this automatically.
- Rate limits are per Google Cloud project, not per API key.

### ChromaDB persistence
- By default, ChromaDB stores data in memory. You MUST configure `persist_directory` to save embeddings to disk, or you'll lose the entire knowledge base on restart.

### uv virtual environment
- `uv venv` creates `.venv/` (dot prefix), not `venv/`. Activation on Windows: `.\.venv\Scripts\activate`.
- `uv run <script>` automatically uses the virtual environment — no need to activate first.

### SQLite concurrency
- SQLite supports only one writer at a time. For our portfolio project this is fine, but if you test with multiple simultaneous users, you may see "database is locked" errors. This is expected and acceptable.

---

## 6. Resumption checklist (when picking up after a break)

1. **Read this file** end-to-end (you're here).
2. **Read `SPEC-INDEX.md`** — check current state of every spec row.
3. **`git pull`** — sync any changes from your teammate.
4. **Check the dependency graph** — identify the next spec to work on.
5. **Check if your API keys still work** — test with a simple Gemini API call.
6. **Identify the next spec** and begin the process from §4.

---

## 7. What this file is NOT

- Not a spec — it has no 7-section structure. It's a session-resumption aid.
- Not a replacement for `SPEC-INDEX.md` — that file is the master tracker.
- Not a project README — `../../README.md` is the canonical entry point.
- Not static — update §2 at the end of every coding session.
