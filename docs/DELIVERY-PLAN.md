# Delivery Plan of Customer Support AI

> The active delivery plan for the multi-agent customer support chatbot. Live progress: [`DELIVERY-STATUS.md`](./DELIVERY-STATUS.md). Spec tracker: [`specs/SPEC-INDEX.md`](./specs/SPEC-INDEX.md).

## Goal

Deliver a **working multi-agent customer support chatbot** with 3 specialist agents (Billing, Technical, General), verified **locally end-to-end**, deployed to **free hosting** (Render + Vercel), within **8 weeks** — at **$0 cost**.

## Team

| Role                  | Responsibilities                                                        |
| --------------------- | ----------------------------------------------------------------------- |
| **AI Engineer**       | Data pipeline, RAG, agents, prompts, evaluation, LLM integration        |
| **Software Engineer** | FastAPI backend, React frontend, database, WebSocket, deployment, CI/CD |

## Scope (in)

- Multi-agent routing (orchestrator → 3 specialists)
- RAG-powered knowledge base (Bitext dataset → ChromaDB)
- Real-time chat UI with streaming responses
- Conversation memory (sliding window)
- LLM fallback chain (Gemini → Groq → Ollama)
- Source citation display
- Dark/light mode
- Admin dashboard (basic)
- Free-tier cloud deployment

## Scope (out / deferred)

- **Fine-tuning** — out (no GPU; see ADR-0003).
- **User authentication** — deferred to v2 (portfolio demos don't need login).
- **Multi-language support** — deferred (English only for v1).
- **Payment integration** — out of scope entirely.

## Deliverables

| #   | Deliverable                                  | Owner  | Spec     | Phase |
| --- | -------------------------------------------- | ------ | -------- | ----- |
| D1  | ADR — Gemini free tier as primary LLM        | AI Eng | ADR-0001 | 0     |
| D2  | ADR — SQLite over Postgres                   | SWE    | ADR-0002 | 0     |
| D3  | ADR — RAG over fine-tuning                   | AI Eng | ADR-0003 | 0     |
| D4  | ADR — LangGraph for orchestration            | AI Eng | ADR-0004 | 0     |
| D5  | Monorepo setup + local dev environment       | Both   | M1       | 0     |
| D6  | Data ingestion pipeline (dataset → ChromaDB) | AI Eng | AI-1     | 1     |
| D7  | RAG retrieval pipeline                       | AI Eng | AI-2     | 1     |
| D8  | Orchestrator agent (intent classification)   | AI Eng | AI-3     | 1     |
| D9  | 3 specialist agents + conversation memory    | AI Eng | AI-4     | 1     |
| D10 | FastAPI backend (chat API, WebSocket, DB)    | SWE    | API-1    | 1     |
| D11 | React chat UI                                | SWE    | WEB-1    | 1     |
| D12 | AI ↔ API integration                         | Both   | INT-1    | 2     |
| D13 | Evaluation suite (metrics + benchmarks)      | AI Eng | EVAL-1   | 3     |
| D14 | Production deployment (Docker, cloud, CI)    | SWE    | DEPLOY-1 | 3     |

## Sequencing (8 weeks)

| Week   | Milestone                                                                                   |
| ------ | ------------------------------------------------------------------------------------------- |
| Week 1 | ADR-0001 through ADR-0004 accepted. M1 executed. Both repos initialized, local dev working. |
| Week 2 | AI-1 (data pipeline) + API-1 (backend) started in parallel.                                 |
| Week 3 | AI-2 (RAG) + AI-3 (orchestrator). API-1 continues. WEB-1 starts.                            |
| Week 4 | AI-4 (specialists). WEB-1 continues.                                                        |
| Week 5 | AI-4 complete. WEB-1 complete.                                                              |
| Week 6 | INT-1 (integration). Full E2E testing.                                                      |
| Week 7 | EVAL-1 (metrics). Bug fixes. Polish.                                                        |
| Week 8 | DEPLOY-1 (Docker + cloud). README. Demo video. Portfolio polish.                            |

## Risks

| Risk                                  | Mitigation                                                  |
| ------------------------------------- | ----------------------------------------------------------- |
| Gemini rate limits during demos       | Groq fallback + response caching (ADR-0001)                 |
| ChromaDB performance on large dataset | Limit to 5,000 chunks; use `all-MiniLM-L6-v2` (small, fast) |
| Teammate availability drops           | Specs are independent per role; either can continue solo    |
| Render free tier cold starts          | Acceptable for portfolio; document in README                |
