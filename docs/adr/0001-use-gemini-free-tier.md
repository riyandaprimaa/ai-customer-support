# ADR-0001: Use Google Gemini Free Tier as Primary LLM

> **Status:** Accepted
> **Date:** 2026-08-11
> **Decision makers:** AI Engineer, Software Engineer (team consensus)

---

## Context

We are building a multi-agent customer support chatbot as a portfolio project by two fresh graduates. The project requires a capable Large Language Model (LLM) for:

1. **Intent classification** — routing user queries to the correct specialist agent (billing, technical, general).
2. **Response generation** — generating accurate, contextual answers grounded in a knowledge base (RAG).
3. **Conversation memory** — maintaining multi-turn context across a support session.

Forces at play:

1. **Zero budget.** Neither team member can afford paid API subscriptions. The LLM must be available on a permanent free tier — not a trial credit that expires.
2. **Limited hardware.** Both team members use local PCs with ≤16 GB RAM and no dedicated GPU. Running large local models (7B+ parameters) is too slow for interactive chat during development.
3. **Quality requirement.** The portfolio project must produce coherent, professional-sounding customer support responses. A model that generates nonsensical or low-quality replies defeats the purpose.
4. **Rate limits matter.** During development, we'll make frequent API calls for testing and prompt iteration. During demos, we need reliable uptime — a rate limit of 2 RPM would make the app unusable.
5. **Context window size.** Our RAG pipeline injects retrieved knowledge base chunks (500+ tokens each) plus conversation history into each prompt. A small context window (4K tokens) would truncate critical context.

---

## Decision

**Use Google Gemini API (free tier via Google AI Studio) as the primary LLM, with Groq API (free tier) as fallback, and Ollama (local) for offline development.**

The provider priority chain:

```
1. Google Gemini (gemini-2.0-flash)  ← PRIMARY
   - Free tier: ~15 RPM, generous daily limits
   - 1M token context window (largest free tier available)
   - No credit card required
   - Sign up: https://aistudio.google.com/

2. Groq (llama-3.3-70b-versatile)    ← FALLBACK (on Gemini 429)
   - Free tier: ~30 RPM, 14,400 requests/day
   - Extremely fast inference (LPU hardware)
   - OpenAI-compatible API
   - Sign up: https://console.groq.com/

3. Ollama (phi4-mini / qwen3:4b)     ← OFFLINE / LOCAL DEV
   - Fully local, no internet required
   - Runs on CPU with 8 GB RAM (3-4B models)
   - Slower than cloud APIs but privacy-safe
   - Install: https://ollama.com/
```

Implementation pattern:

```python
# ai/utils/llm_provider.py
async def get_llm_response(prompt: str) -> str:
    """Try Gemini first, fall back to Groq, then Ollama."""
    try:
        return await call_gemini(prompt)
    except RateLimitError:
        logger.warning("Gemini rate limited, falling back to Groq")
        try:
            return await call_groq(prompt)
        except RateLimitError:
            logger.warning("Groq rate limited, falling back to Ollama")
            return await call_ollama(prompt)
```

---

## Consequences

### What becomes easier

- **$0 cost** throughout the entire development lifecycle. No billing surprises.
- **1M token context window** (Gemini) eliminates the need to aggressively truncate conversation history or retrieval context.
- **Triple redundancy** — if one provider is down or rate-limited, we automatically fall back. The app never hard-fails due to LLM unavailability.
- **Ollama enables offline development** — both team members can work on trains, planes, or cafés without internet.

### What becomes harder

- **Rate-limited demos.** If multiple people test the app simultaneously during a portfolio review, we may hit Gemini's 15 RPM limit. Mitigation: implement response caching for identical queries.
- **No fine-tuning.** Free-tier APIs do not support model fine-tuning. Our quality improvement lever is limited to prompt engineering + RAG context quality. This is acceptable — see ADR-0003 (RAG over fine-tuning).
- **Data privacy.** Free-tier Gemini may use prompts to improve Google's models. For a portfolio project with synthetic/public datasets, this is acceptable. For a production app with real customer data, we would need to revisit.

### What stays the same

- Code structure. LangChain abstracts the LLM provider behind a unified interface (`ChatGoogleGenerativeAI`, `ChatGroq`, `ChatOllama`). Switching providers requires changing one line of config, not rewriting application logic.

---

## Alternatives Considered

### 1. OpenAI API (GPT-4o / GPT-4o-mini)

- **Rejected because:** No permanent free tier. Offers $5–$18 trial credits that expire. Once exhausted, the app stops working. Unacceptable for a portfolio project that must be demoable at any time.
- **Would reconsider if:** OpenAI introduces a permanent free tier comparable to Gemini's.

### 2. Run Llama 3.3 8B locally via Ollama (primary)

- **Rejected because:** 8B models on CPU-only hardware produce 2–5 tokens/second. A typical customer support response (200 tokens) would take 40–100 seconds — far too slow for interactive chat. User experience would be unacceptable for portfolio demos.
- **Would reconsider if:** Either team member acquires a GPU with ≥12 GB VRAM.

### 3. Anthropic Claude (free tier)

- **Rejected because:** Anthropic does not offer a permanent free API tier as of August 2026. The free access is limited to the Claude.ai web interface, which cannot be called programmatically.
- **Would reconsider if:** Anthropic launches a developer free tier.

### 4. OpenRouter (aggregator)

- **Considered but deferred.** OpenRouter provides a single API key for 20+ free models. Useful for benchmarking which model works best. We may use OpenRouter during the evaluation phase (EVAL-1) to compare model quality, but for production we prefer direct provider APIs for more predictable rate limits.

---

## Revisit Trigger

This ADR should be revisited if any of the following occur:

1. **Google removes or significantly degrades the Gemini free tier** (e.g., drops below 5 RPM or adds a credit card requirement).
2. **A team member acquires a GPU** (≥12 GB VRAM), making local 8B+ models viable as primary.
3. **The project transitions from portfolio to production** with real customer data, requiring a paid tier with data privacy guarantees.
4. **A new provider launches** with a significantly more generous free tier (e.g., 100+ RPM, larger context).

---

## References

- [Google AI Studio — Free Tier](https://aistudio.google.com/) — sign up for API key
- [Groq Console — Free Tier](https://console.groq.com/) — sign up for API key
- [Ollama — Local LLM](https://ollama.com/) — download for local development
- [LangChain — Chat Model Integrations](https://python.langchain.com/docs/integrations/chat/) — provider abstraction layer
- ADR-0003 (RAG over fine-tuning) — explains why prompt engineering + RAG is sufficient without fine-tuning
- ADR-0004 (LangGraph orchestration) — the agent framework that consumes this LLM layer
