"""
Unit tests for ChromaDB knowledge base manager.
"""

import tempfile
import pytest
from src.pipelines.knowledge_base import KnowledgeBaseManager


@pytest.fixture
def temp_kb():
    with tempfile.TemporaryDirectory() as tmp_dir:
        kb = KnowledgeBaseManager(persist_directory=tmp_dir)
        yield kb


def test_knowledge_base_add_and_query(temp_kb):
    billing_records = [
        {
            "query": "How do I get a refund for my purchase?",
            "response": "Refunds can be requested via order history within 14 days.",
            "intent": "get_refund",
            "category": "billing",
        }
    ]

    added_count = temp_kb.add_records(category="billing", records=billing_records)
    assert added_count == 1

    # Query similarity
    results = temp_kb.query(query_text="I want a refund", category="billing", n_results=1)
    assert len(results) == 1
    assert "refund" in results[0]["response"].lower()
    assert results[0]["intent"] == "get_refund"


def test_knowledge_base_empty_query(temp_kb):
    results = temp_kb.query(query_text="Non existent topic", category="technical", n_results=1)
    assert len(results) == 0
