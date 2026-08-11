# System Architecture — Customer Support AI

> **The single source of truth for the system architecture.** Read this first when joining the project or resuming work.
>
> **Last updated:** 2026-08-11 (project initialization — target architecture)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           USER (Browser)                                │
│                      React Frontend (Vite)                              │
│                  http://localhost:5173 (dev)                             │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │ HTTP REST + WebSocket (SSE for streaming)
                               │
┌──────────────────────────────▼──────────────────────────────────────────┐
│                        FastAPI Backend                                   │
│                   http://localhost:8000 (dev)                            │
│                                                                         │
│  Routes:                                                                │
│    POST /api/v1/chat              → send message, get AI response       │
│    GET  /api/v1/conversations     → list conversations                  │
│    GET  /api/v1/conversations/:id → get conversation history            │
│    POST /api/v1/conversations     → create new conversation             │
│    DEL  /api/v1/conversations/:id → delete conversation                 │
│    WS   /ws/chat/:id              → real-time streaming (optional)      │
│    GET  /health                   → health check                        │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                        AIService                                 │   │
│  │  (Bridge between FastAPI routes and AI pipeline)                 │   │
│  │  - Receives user message + conversation_id                       │   │
│  │  - Calls orchestrator agent                                      │   │
│  │  - Returns structured response (reply, agent_used, sources)      │   │
│  └──────────────────────────┬───────────────────────────────────────┘   │
│                             │                                           │
│  ┌──────────────────────────▼───────────────────────────────────────┐   │
│  │                   🧠 ORCHESTRATOR AGENT                          │   │
│  │         (LangGraph StateGraph — intent classification)           │   │
│  │                                                                  │   │
│  │  Input: user message + conversation history                      │   │
│  │  Output: { intent: "billing"|"technical"|"general" }             │   │
│  │                                                                  │   │
│  │  Routes to:                                                      │   │
│  └───┬──────────────────────┬──────────────────────┬────────────┘   │   │
│      │                      │                      │                │   │
│  ┌───▼───┐            ┌─────▼─────┐          ┌────▼────┐          │   │
│  │Billing│            │ Technical │          │ General │          │   │
│  │ Agent │            │   Agent   │          │  Agent  │          │   │
│  │       │            │           │          │         │          │   │
│  │Prompts│            │  Prompts  │          │ Prompts │          │   │
│  │+ RAG  │            │  + RAG    │          │ + RAG   │          │   │
│  └───┬───┘            └─────┬─────┘          └────┬────┘          │   │
│      │                      │                     │               │   │
│  ┌───▼──────────────────────▼─────────────────────▼────────────┐  │   │
│  │              RAG Retrieval Pipeline                          │  │   │
│  │                                                             │  │   │
│  │  1. Embed user query (sentence-transformers, CPU)           │  │   │
│  │  2. Search ChromaDB (top-k=5 similar chunks)                │  │   │
│  │  3. Inject retrieved chunks into LLM prompt                 │  │   │
│  │  4. Generate response via LLM (Gemini → Groq → Ollama)     │  │   │
│  │  5. Return response + source citations                      │  │   │
│  └─────────────────────────────────────────────────────────────┘  │   │
│                                                                   │   │
│  ┌─────────────────────┐  ┌──────────────────────────┐           │   │
│  │   SQLite Database    │  │   ChromaDB (Vector DB)    │           │   │
│  │   (conversations,   │  │   (knowledge base         │           │   │
│  │    messages,         │  │    embeddings, 3           │           │   │
│  │    feedback)         │  │    collections:            │           │   │
│  │                      │  │    billing_kb,             │           │   │
│  │   File: app.db      │  │    technical_kb,           │           │   │
│  └─────────────────────┘  │    general_kb)             │           │   │
│                            │                            │           │   │
│                            │   Dir: ./chroma_data/      │           │   │
│                            └──────────────────────────┘           │   │
└───────────────────────────────────────────────────────────────────────┘

LLM Provider Chain (ADR-0001):
  1. Google Gemini API (free, 15 RPM, 1M context)   ← PRIMARY
  2. Groq API (free, 30 RPM, fast)                  ← FALLBACK
  3. Ollama local (phi4-mini, CPU)                   ← OFFLINE
```

---

## Data Flow (Single User Message)

```
1. User types "I was charged twice" in React chat UI
2. React sends POST /api/v1/chat { message, conversation_id }
3. FastAPI receives → saves user message to SQLite → calls AIService
4. AIService loads conversation history from SQLite (last 10 messages)
5. Orchestrator agent classifies intent → "billing"
6. Billing agent receives query + conversation history
7. RAG pipeline embeds query → searches billing_kb collection in ChromaDB
8. Top-5 relevant FAQ chunks retrieved
9. Prompt assembled: system prompt + retrieved chunks + conversation history + user query
10. Prompt sent to Gemini API (or Groq/Ollama fallback)
11. LLM generates response
12. Response + sources + agent_used returned to FastAPI
13. FastAPI saves AI message to SQLite → returns JSON to React
14. React renders the response with typing animation + source citations
```

---

## Key Design Decisions

| Decision | ADR | Impact |
|---|---|---|
| Gemini free tier primary | ADR-0001 | $0 cost, 1M context, 15 RPM limit |
| SQLite database | ADR-0002 | Zero setup, file-based, sufficient for portfolio |
| RAG over fine-tuning | ADR-0003 | No GPU needed, knowledge base is updatable without retraining |
| LangGraph orchestration | ADR-0004 | State machine for agent routing, built-in memory management |

---

## Tech Stack Summary

| Layer | Technology | Owner |
|---|---|---|
| Frontend | React + Vite + TypeScript + CSS | Software Engineer |
| Backend | FastAPI + SQLAlchemy + SQLite | Software Engineer |
| AI Pipeline | LangChain + LangGraph + ChromaDB | AI Engineer |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) | AI Engineer |
| LLM | Gemini / Groq / Ollama | AI Engineer |
| Package Mgmt | `uv` (Python), `npm` (JS) | Both |
| Deployment | Docker + Render (API) + Vercel (Web) | Software Engineer |
