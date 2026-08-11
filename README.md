# AI Customer Support System

> Multi-agent chatbot with RAG-powered knowledge base. Built by a 2-person team (AI Engineer + Software Engineer) using agentic vibe coding.

## Quick Links

| Doc | Purpose |
|---|---|
| [PROJECT_WALKTHROUGH.md](./PROJECT_WALKTHROUGH.md) | **Start here** — complete project guide (PDF-ready) |
| [docs/SYSTEM_ARCHITECTURE.md](./docs/SYSTEM_ARCHITECTURE.md) | System architecture source of truth |
| [docs/DELIVERY-PLAN.md](./docs/DELIVERY-PLAN.md) | 14 deliverables |
| [docs/DELIVERY-STATUS.md](./docs/DELIVERY-STATUS.md) | Live progress |
| [docs/specs/SPEC-INDEX.md](./docs/specs/SPEC-INDEX.md) | Master spec tracker |
| [docs/specs/SPEC-CONTEXT.md](./docs/specs/SPEC-CONTEXT.md) | AI agent session context |
| [docs/adr/README.md](./docs/adr/README.md) | Architecture decisions |

## Architecture

```
User (React) → FastAPI → Orchestrator Agent → {Billing|Technical|General} Agent → RAG (ChromaDB) → LLM (Gemini)
```

## Tech Stack

- **AI:** Python · LangChain · LangGraph · ChromaDB · Gemini API
- **Backend:** FastAPI · SQLAlchemy · SQLite
- **Frontend:** React · Vite · TypeScript
- **Tools:** uv · Docker · GitHub Actions
- **Hosting:** Render (API) · Vercel (Web)

## Getting Started

See [PROJECT_WALKTHROUGH.md § Getting Started](./PROJECT_WALKTHROUGH.md#9-getting-started-day-1).
