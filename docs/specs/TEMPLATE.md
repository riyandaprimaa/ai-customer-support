# Spec Template

> **Purpose:** Unified template for all build / feature / refactor specs in `docs/specs/`.
> **Adapted from:** `sga-deploy-runbook/specs/TEMPLATE.md` (simplified for a greenfield project by fresh graduates).
> **Last updated:** 2026-08-11

---

## Naming Convention

File name: `YYYY-MM-DD-spec-[CODE][N]-[theme-slug].md`

- **Date prefix** — authoring date (ISO). Sorts chronologically.
- **CODE + N** — service code + sequence number (see codes below).
- **Theme slug** — short kebab-case description.

**Examples:**
- `2026-08-18-spec-ai1-data-ingestion-pipeline.md`
- `2026-08-18-spec-api1-fastapi-backend.md`
- `2026-08-25-spec-web1-react-chat-ui.md`

### Service Codes

| Code | Scope | Owner | Examples |
|---|---|---|---|
| `AI` | AI pipeline (`ai/`) | AI Engineer | data ingestion, RAG, agents, prompts, evaluation |
| `API` | Backend (`apps/api/`) | Software Engineer | routes, models, services, WebSocket, database |
| `WEB` | Frontend (`apps/web/`) | Software Engineer | components, pages, styling, state management |
| `M` | Monorepo / tooling (root) | Both | Makefile, env files, Docker, CI/CD |
| `INT` | Integration (AI ↔ API) | Both | AIService bridge, API contracts, streaming |
| `EVAL` | Evaluation | AI Engineer | RAGAS metrics, benchmarks, test datasets |
| `DEPLOY` | Deployment | Software Engineer | Docker, Render, Vercel, GitHub Actions |

> A spec should touch **one** service/scope only. Cross-scope work splits into separate specs coordinated via `SPEC-INDEX.md` prerequisites.

---

## Git Branching & Versioning Convention

Every spec follows an isolated feature branch lifecycle:

1. **Branch Naming:** `feature/<spec-code>-<theme-slug>`
   - Example: `feature/ai-1-data-pipeline`, `feature/api-1-fastapi-backend`
2. **Atomic Commits:** A feature branch must bundle the **code + unit tests + spec markdown updates + developer docs/notebooks** together.
3. **Branch Lifecycle:**
   - Create branch: `git checkout -b feature/<spec-code>-<theme-slug>` from updated `main`.
   - Implement, test (`uv run pytest` / `npm test`), and verify checklist.
   - Update `SPEC-INDEX.md` status (`🟩`) and `DELIVERY-STATUS.md`.
   - Push and open a Pull Request into `main`.
   - Merge and delete the feature branch.

> For complete details on Git conventions and commit formatting, see [`../GIT_WORKFLOW.md`](../GIT_WORKFLOW.md).

---

## Metadata Header

Every spec starts with this block:

```markdown
# [CODE][N]: [Theme Name]

> **Type:** feature | refactor | action
> **Service:** ai | api | web | monorepo | integration | evaluation | deployment
> **Owner:** AI Engineer | Software Engineer | Both
> **Maps to deliverable:** D# (from DELIVERY-PLAN.md)
> **Prerequisite:** [other spec or ADR that must complete first, or "none"]
> **Unblocks:** [specs that depend on this completing]
> **Status:** draft | ready | executing | done | blocked
> **Date:** YYYY-MM-DD
```

---

## 7 Required Sections

### 1. Problem Statement

**Purpose:** Explain *why* this spec exists. The gap, the need, the cost of inaction.

**Length:** 1–2 paragraphs + bulleted impact list (2–5 bullets).

---

### 2. Current State

**Purpose:** Document what exists today. For a greenfield project, this may simply be "nothing exists yet" with a note about what the prior spec delivered.

**For specs that modify existing code:** cite the file path and describe what's there.

---

### 3. Proposed Design

**Purpose:** Define the *target* state. Show the design with rationale.

**Include:**
- Code examples or pseudo-code showing the target pattern.
- API contracts (request/response shapes) if applicable.
- Architecture diagrams if the spec changes the system structure.
- Rationale for design choices (reference ADRs where applicable).

---

### 4. Build Plan

**Purpose:** Step-by-step execution plan. How to get from current state to target.

**Format:**

```markdown
### Phase 1: [Name] ([time estimate])

1. Step 1
2. Step 2

### Phase 2: [Name] ([time estimate])

1. Step 1
2. Step 2
```

**Time estimate guidance:**
- Trivial: 15–30 min
- Small: 30 min – 1 hour
- Medium: 1–2 hours
- Large: 2–4 hours
- Very large: 4+ hours (consider splitting the spec)

---

### 5. Verification Checklist

**Purpose:** Concrete, testable checks. When all items are checked, the spec is done.

**Format:** Markdown task list (`- [ ]`).

**Categories to include:**
- [ ] Code changes (files created, modified)
- [ ] Tests written and passing (with specific counts)
- [ ] Build succeeds (`uv run uvicorn ...` / `npm run dev`)
- [ ] Manual smoke tests (specific user flows)
- [ ] No regression (existing functionality still works)

**Be specific.** Bad: "Tests pass." Good: "All 12 tests in `tests/test_agents.py` pass; 3 new tests added for intent classification."

---

### 6. Out of Scope

**Purpose:** Explicitly list what this spec does *not* do. Prevents scope creep.

**Format:** Bulleted list with reason for each exclusion.

---

### 7. Cross-References

**Purpose:** Help readers navigate the spec ecosystem.

**Include:**
- **Prerequisite(s)** — specs/ADRs that must complete first (with paths).
- **Unblocks** — specs that depend on this.
- **Related specs** — adjacent work.
- **ADRs** — decisions that constrain this spec.

---

## Anti-Patterns to Avoid

1. **Vague problem statements** — "we need agents" is not a problem statement. "Users can't get routed to the correct support specialist" is.
2. **Build plans without time estimates** — always estimate phase duration.
3. **Verification without specifics** — "tests pass" is not enough. Specify test file, count, and what they cover.
4. **Out of scope without reason** — if something is excluded, say why.
5. **Specs that touch multiple services** — split into separate specs per service code.
6. **Phases without a clear deliverable** — each phase should produce a commit or a verified state.
