"""
Unit tests for data loader pipeline.
"""

from src.pipelines.data_loader import (
    categorize_intent,
    clean_record,
    categorize_records,
    get_seed_dataset,
)


def test_categorize_intent_billing():
    assert categorize_intent("get_refund") == "billing"
    assert categorize_intent("check_invoice") == "billing"
    assert categorize_intent("payment_issue") == "billing"


def test_categorize_intent_technical():
    assert categorize_intent("recover_password") == "technical"
    assert categorize_intent("delete_account") == "technical"
    assert categorize_intent("registration_problems") == "technical"


def test_categorize_intent_general():
    assert categorize_intent("contact_human_agent") == "general"
    assert categorize_intent("track_order") == "general"
    assert categorize_intent("unknown_custom_tag") == "general"


def test_clean_record():
    raw = {
        "instruction": " How do I reset password? ",
        "response": " Go to login page. ",
        "intent": "recover_password",
    }
    cleaned = clean_record(raw)
    assert cleaned["query"] == "How do I reset password?"
    assert cleaned["response"] == "Go to login page."
    assert cleaned["intent"] == "recover_password"
    assert cleaned["category"] == "technical"


def test_categorize_records():
    records = [
        {"query": "q1", "response": "a1", "category": "billing"},
        {"query": "q2", "response": "a2", "category": "technical"},
        {"query": "q3", "response": "a3", "category": "general"},
    ]
    result = categorize_records(records)
    assert len(result["billing"]) == 1
    assert len(result["technical"]) == 1
    assert len(result["general"]) == 1


def test_get_seed_dataset():
    seed = get_seed_dataset()
    assert len(seed) >= 9
    categories = {r["category"] for r in seed}
    assert "billing" in categories
    assert "technical" in categories
    assert "general" in categories
