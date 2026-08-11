# ADR-0004: LangGraph for Multi-Agent Orchestration & Memory

> **Status:** Accepted
> **Date:** 2026-08-11
> **Decision makers:** AI Engineer (team consensus)

---

## Context

Our system requires routing incoming user messages between an Orchestrator Agent and three specialist agents (Billing, Technical, General), while maintaining multi-turn conversation history across a chat session.

Options evaluated:
1. **Single Monolithic Prompt:** A single giant prompt attempting to classify, retrieve, and answer all categories at once.
2. **Hardcoded Python Control Flow:** Custom `if/else` logic in Python using simple string matching or regex.
3. **LangGraph State Graph:** A framework for building stateful, multi-agent AI workflows using graph nodes and edges.

Forces at play:
- **Modularity:** We want dedicated prompts, system rules, and vector search collections for each specialist domain.
- **State Management:** Agents need access to conversation history, classification confidence, and retrieved documents across execution turns.
- **Portfolio Value:** LangGraph is the modern production standard for agentic AI architectures in industry.

---

## Decision

**Adopt LangGraph (StateGraph) for multi-agent intent routing, specialist agent execution, and conversation state management.**

Workflow Graph Structure:
```
[User Message] ──▶ (Orchestrator Node: Intent Classifier)
                        │
         ┌──────────────┼──────────────┐
         ▼              ▼              ▼
  [Billing Agent] [Technical Agent] [General Agent]
         │              │              │
         └──────────────┼──────────────┘
                        ▼
            [Return Response + Sources]
```

State Schema (`AgentState`):
- `messages`: List of conversation messages (user + assistant)
- `intent`: Classified domain (`billing` | `technical` | `general`)
- `retrieved_docs`: List of ChromaDB FAQ chunks
- `confidence`: Intent classification confidence score (0.0 - 1.0)

---

## Consequences

### What becomes easier
- **Modular Specialist Prompts:** Each specialist agent has an isolated prompt and knowledge base, preventing prompt bloat.
- **Stateful Memory:** LangGraph maintains clean conversation state across nodes.
- **Visual Debugging:** Graph execution steps can be logged and inspected per request.
- **Future Extensibility:** Adding a 4th specialist agent (e.g., Sales Agent) requires adding 1 graph node and 1 edge.

### What becomes harder
- **Slightly higher learning curve:** Requires understanding LangGraph state transitions and node handlers vs simple functions.

---

## References

- LangGraph Documentation (LangChain)
- ADR-0001 (Gemini Free Tier)
- ADR-0003 (RAG System)
