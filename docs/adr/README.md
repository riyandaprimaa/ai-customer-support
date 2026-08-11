# Architecture Decision Records (ADR)

> Records of architecturally significant decisions on the Customer Support AI project. Each ADR is a short, immutable document: once Accepted, it is not rewritten — it is superseded by a new ADR that references it. ADRs live alongside (not under) the spec system: specs implement work; ADRs record *why* a direction was chosen.

## Format

Every ADR follows this structure:

- **Status:** Proposed | Accepted | Superseded | Deprecated
- **Context:** what forces are at play (technical, budget, hardware, organizational)
- **Decision:** the chosen response, stated unambiguously
- **Consequences:** what becomes easier, harder, or possible as a result
- **Alternatives Considered:** the options rejected and why
- **Revisit Trigger:** the conditions that would cause this ADR to be revisited
- **References:** research, docs, links

## Naming

`NNNN-[theme-slug].md` — zero-padded sequence + kebab-case title. Date is encoded inside the document, not the filename, because ADRs are referenced by number.

## Index

| # | Title | Status | Date | File |
|---|---|---|---|---|
| [0001](./0001-use-gemini-free-tier.md) | Use Google Gemini Free Tier as Primary LLM | 🟩 Accepted | 2026-08-11 | [`./0001-use-gemini-free-tier.md`](./0001-use-gemini-free-tier.md) |
| 0002 | SQLite over Postgres for zero-overhead development | ⬜ To write (SWE) | — | — |
| [0003](./0003-rag-over-finetuning.md) | RAG over Fine-Tuning for Customer Support Knowledge Base | 🟩 Accepted | 2026-08-11 | [`./0003-rag-over-finetuning.md`](./0003-rag-over-finetuning.md) |
| [0004](./0004-langgraph-orchestration.md) | LangGraph for Multi-Agent Orchestration & Memory | 🟩 Accepted | 2026-08-11 | [`./0004-langgraph-orchestration.md`](./0004-langgraph-orchestration.md) |

## Relationship to Specs

- **ADR** = *why a direction was chosen* (immutable record; cited by specs).
- **Spec** = *how a piece of work is implemented* (mutable; iterates through draft → ready → done).

A spec should cite any ADR that constrains its design in its "Cross-References" section.
