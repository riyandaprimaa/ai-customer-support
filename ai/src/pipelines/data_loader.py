"""
Data Loader module.
Handles fetching, cleaning, and categorizing customer support datasets.
"""

from typing import Any
from src.config import BILLING_INTENTS, TECHNICAL_INTENTS, DATASET_NAME


def categorize_intent(intent: str) -> str:
    """
    Classify an intent tag into one of three specialist domains:
    'billing', 'technical', or 'general'.
    """
    intent_lower = intent.lower().strip()
    if intent_lower in BILLING_INTENTS or any(
        kw in intent_lower for kw in ["refund", "billing", "invoice", "payment", "discount"]
    ):
        return "billing"
    elif intent_lower in TECHNICAL_INTENTS or any(
        kw in intent_lower for kw in ["account", "password", "bug", "technical", "login", "register"]
    ):
        return "technical"
    else:
        return "general"


def clean_record(raw_record: dict[str, Any]) -> dict[str, Any]:
    """
    Extract and standardize key fields from a dataset row into a clean dictionary.
    Supports Bitext schema (instruction/response/intent) as well as generic FAQ format.
    """
    query = raw_record.get("instruction") or raw_record.get("question") or raw_record.get("utterance") or ""
    response = raw_record.get("response") or raw_record.get("answer") or ""
    intent = raw_record.get("intent") or "general"
    category = categorize_intent(intent)

    return {
        "query": query.strip(),
        "response": response.strip(),
        "intent": intent.strip(),
        "category": category,
    }


def load_dataset_records(dataset_name: str = DATASET_NAME, limit: int = 1000) -> list[dict[str, Any]]:
    """
    Load dataset from HuggingFace datasets library.
    Falls back gracefully if network issue or offline mode.
    """
    try:
        from datasets import load_dataset  # type: ignore

        print(f"Loading dataset: {dataset_name} (limit={limit})...")
        dataset = load_dataset(dataset_name, split="train")
        records = []
        for i, row in enumerate(dataset):
            if limit and i >= limit:
                break
            cleaned = clean_record(row)
            if cleaned["query"] and cleaned["response"]:
                records.append(cleaned)
        print(f"Successfully loaded {len(records)} records from HuggingFace.")
        return records
    except Exception as e:
        print(f"Notice: HuggingFace dataset download fallback ({e}). Using built-in seed dataset.")
        return get_seed_dataset()


def categorize_records(records: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """
    Organize records by domain category: 'billing', 'technical', 'general'.
    """
    categorized: dict[str, list[dict[str, Any]]] = {
        "billing": [],
        "technical": [],
        "general": [],
    }
    for record in records:
        cat = record.get("category", "general")
        if cat in categorized:
            categorized[cat].append(record)
        else:
            categorized["general"].append(record)
    return categorized


def get_seed_dataset() -> list[dict[str, Any]]:
    """
    Fallback seed dataset covering core customer support FAQ scenarios.
    Used for local development, offline runs, and unit testing.
    """
    raw_seed = [
        # Billing
        {
            "instruction": "How do I request a refund for my subscription?",
            "response": "You can request a refund within 14 days of purchase by navigating to Billing Settings > Order History > Request Refund, or by contacting billing@support.com.",
            "intent": "get_refund",
        },
        {
            "instruction": "Where can I download my monthly invoice?",
            "response": "Invoices are available in your account under Billing > Invoices. Select the desired billing period and click 'Download PDF'.",
            "intent": "check_invoice",
        },
        {
            "instruction": "What payment methods do you accept?",
            "response": "We accept major credit cards (Visa, MasterCard, American Express), PayPal, and Apple Pay.",
            "intent": "check_payment_methods",
        },
        # Technical
        {
            "instruction": "How can I reset my account password?",
            "response": "Click 'Forgot Password' on the login page. Enter your registered email address and we will send a password reset link valid for 24 hours.",
            "intent": "recover_password",
        },
        {
            "instruction": "I am getting an error when logging into my account.",
            "response": "Please clear your browser cache and cookies, verify your login credentials, or try logging in via incognito mode. If issues persist, contact technical support.",
            "intent": "registration_problems",
        },
        {
            "instruction": "How do I delete my account data?",
            "response": "Navigate to Account Settings > Security & Privacy > Delete Account. Confirm your password to permanently delete your data.",
            "intent": "delete_account",
        },
        # General
        {
            "instruction": "How do I contact a human customer support agent?",
            "response": "Our support team is available 24/7 via live chat or email at support@company.com. Response times are typically under 1 hour.",
            "intent": "contact_human_agent",
        },
        {
            "instruction": "How can I track my package or order status?",
            "response": "You can track your order in real-time by entering your order ID on our Order Tracking page or checking the confirmation email link.",
            "intent": "track_order",
        },
        {
            "instruction": "Where can I leave feedback or a product review?",
            "response": "We appreciate your feedback! You can leave a review on the product page or fill out our feedback form in the Help Center.",
            "intent": "review",
        },
    ]

    return [clean_record(r) for r in raw_seed]
