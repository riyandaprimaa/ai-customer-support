"""
RAG Retriever & Response Generation Pipeline.
Connects domain knowledge from ChromaDB collections with multi-LLM generation and source citations.
"""

from typing import Any
from src.pipelines.knowledge_base import KnowledgeBaseManager
from src.pipelines.llm_client import LLMClient


class RAGRetriever:
    """
    Retrieval-Augmented Generation (RAG) engine for Customer Support AI.
    - Performs semantic vector search on domain ChromaDB collections
    - Filters by minimum relevance threshold
    - Injects grounded FAQ context into LLM prompts
    - Extracts structured source citations
    """

    SYSTEM_PERSONAS = {
        "billing": (
            "You are a helpful, empathetic Billing Support Specialist. "
            "Answer the customer's question accurately based ONLY on the provided FAQ context and policies. "
            "If the context does not contain the answer, politely advise the user on how to contact human billing support."
        ),
        "technical": (
            "You are an expert Technical Support Specialist. "
            "Provide clear, step-by-step troubleshooting instructions based on the provided technical context. "
            "Keep instructions structured and easy to follow."
        ),
        "general": (
            "You are a friendly, professional General Customer Support Specialist. "
            "Assist the customer warmly using the provided FAQ context."
        ),
    }

    def __init__(
        self,
        kb_manager: KnowledgeBaseManager | None = None,
        llm_client: LLMClient | None = None,
        min_relevance_score: float = 0.35,
    ):
        self.kb_manager = kb_manager or KnowledgeBaseManager()
        self.llm_client = llm_client or LLMClient()
        self.min_relevance_score = min_relevance_score

    def retrieve_context(
        self, query: str, category: str, top_k: int = 3
    ) -> tuple[str, list[dict[str, Any]]]:
        """
        Query ChromaDB domain collection and format retrieved chunks into context string.
        Returns: (formatted_context_str, list_of_filtered_sources)
        """
        raw_matches = self.kb_manager.query(
            query_text=query,
            category=category,
            n_results=top_k,
        )

        filtered_sources: list[dict[str, Any]] = []
        context_blocks: list[str] = []

        for i, match in enumerate(raw_matches, 1):
            score = match.get("relevance_score", 0.0)
            if score >= self.min_relevance_score:
                faq_query = match.get("query", "")
                faq_response = match.get("response", "")
                intent = match.get("intent", "general")

                context_blocks.append(
                    f"[FAQ #{i} - Intent: {intent}]\nQ: {faq_query}\nA: {faq_response}"
                )

                filtered_sources.append(
                    {
                        "source_id": f"{category}_kb_doc_{i}",
                        "category": category,
                        "intent": intent,
                        "query": faq_query,
                        "response": faq_response,
                        "relevance_score": round(score, 3),
                    }
                )

        if context_blocks:
            formatted_context = "\n\n".join(context_blocks)
        else:
            formatted_context = "No specific FAQ entries matched this query above the confidence threshold."

        return formatted_context, filtered_sources

    def format_prompt(
        self,
        query: str,
        category: str,
        context: str,
        history: list[dict[str, str]] | None = None,
    ) -> str:
        """
        Assemble the final prompt with context, conversation history, and user query.
        """
        prompt_parts: list[str] = []

        prompt_parts.append(f"Domain Area: {category.upper()} SUPPORT\n")
        prompt_parts.append("Context Information:\n" + context + "\n")

        if history:
            history_blocks = []
            for msg in history[-6:]:  # Last 6 messages sliding window
                role = msg.get("role", "user").capitalize()
                content = msg.get("content", "")
                history_blocks.append(f"{role}: {content}")
            prompt_parts.append("Recent Conversation History:\n" + "\n".join(history_blocks) + "\n")

        prompt_parts.append(f"User Question: {query}\n")
        prompt_parts.append("Please provide a helpful, concise, and grounded response:")

        return "\n".join(prompt_parts)

    def answer(
        self,
        query: str,
        category: str = "general",
        history: list[dict[str, str]] | None = None,
        top_k: int = 3,
    ) -> dict[str, Any]:
        """
        Full end-to-end RAG answer pipeline.
        Returns: { reply, sources, provider_used, has_context, category }
        """
        context_str, sources = self.retrieve_context(
            query=query,
            category=category,
            top_k=top_k,
        )

        has_context = len(sources) > 0
        system_persona = self.SYSTEM_PERSONAS.get(category.lower(), self.SYSTEM_PERSONAS["general"])

        prompt = self.format_prompt(
            query=query,
            category=category,
            context=context_str,
            history=history,
        )

        reply, provider_used = self.llm_client.invoke(
            prompt=prompt,
            system_message=system_persona,
        )

        return {
            "reply": reply,
            "sources": sources,
            "provider_used": provider_used,
            "has_context": has_context,
            "category": category,
        }
