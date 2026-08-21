"""
Unit tests for RAGRetriever pipeline.
"""

import tempfile
import pytest
from src.pipelines.knowledge_base import KnowledgeBaseManager
from src.pipelines.retriever import RAGRetriever
from src.pipelines.llm_client import LLMClient


@pytest.fixture
def seeded_retriever():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
        kb = KnowledgeBaseManager(persist_directory=tmp_dir)

        # Seed sample FAQ records across domains
        billing_faqs = [
            {
                "query": "How do I request a refund for my subscription?",
                "response": "You can request a refund in Billing Settings within 14 days.",
                "intent": "get_refund",
                "category": "billing",
            },
            {
                "query": "Where can I download my invoice?",
                "response": "Invoices are available under Billing > Invoices as PDF.",
                "intent": "check_invoice",
                "category": "billing",
            },
        ]
        kb.add_records(category="billing", records=billing_faqs)

        llm = LLMClient()
        # Force offline mode for deterministic unit test assertions
        llm.gemini_api_key = ""
        llm.groq_api_key = ""

        retriever = RAGRetriever(kb_manager=kb, llm_client=llm, min_relevance_score=0.2)
        yield retriever


def test_retriever_retrieve_context_matching(seeded_retriever):
    context_str, sources = seeded_retriever.retrieve_context(
        query="I want to refund my subscription",
        category="billing",
        top_k=2,
    )

    assert len(sources) >= 1
    assert sources[0]["category"] == "billing"
    assert sources[0]["intent"] == "get_refund"
    assert "refund" in context_str.lower()
    assert "relevance_score" in sources[0]


def test_retriever_retrieve_context_empty(seeded_retriever):
    context_str, sources = seeded_retriever.retrieve_context(
        query="Unrelated query about spaceships",
        category="technical",
        top_k=2,
    )
    # Technical collection is empty
    assert len(sources) == 0
    assert "No specific FAQ entries matched" in context_str


def test_retriever_format_prompt_with_history(seeded_retriever):
    history = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi! How can I help you today?"},
    ]
    prompt = seeded_retriever.format_prompt(
        query="Can I get a refund?",
        category="billing",
        context="[FAQ #1]\nQ: Refund info\nA: Refund steps",
        history=history,
    )

    assert "Domain Area: BILLING SUPPORT" in prompt
    assert "Recent Conversation History:" in prompt
    assert "User: Hello" in prompt
    assert "User Question: Can I get a refund?" in prompt


def test_retriever_answer_end_to_end(seeded_retriever):
    result = seeded_retriever.answer(
        query="How do I get my money back?",
        category="billing",
    )

    assert isinstance(result, dict)
    assert "reply" in result
    assert "sources" in result
    assert "provider_used" in result
    assert "has_context" in result
    assert result["has_context"] is True
    assert result["category"] == "billing"
    assert len(result["sources"]) >= 1
