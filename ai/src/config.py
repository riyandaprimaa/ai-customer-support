"""
Configuration module for the AI pipeline.
Manages environment variables, default paths, and intent categorization mappings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from repository root .env or local .env
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DB_DIR = os.getenv("CHROMADB_PATH", str(BASE_DIR / "chroma_data"))
DATASET_NAME = os.getenv(
    "DATASET_NAME", "bitext/Bitext-customer-support-llm-chatbot-training-dataset"
)

# Embedding Settings (ADR-0003: sentence-transformers/all-MiniLM-L6-v2)
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Intent Mappings
BILLING_INTENTS = {
    "get_refund",
    "check_refund_policy",
    "check_invoice",
    "check_payment_methods",
    "check_cancellation_fee",
    "get_discounts",
    "track_refund",
    "payment_issue",
    "billing",
    "invoice",
    "refund",
}

TECHNICAL_INTENTS = {
    "create_account",
    "delete_account",
    "edit_account",
    "recover_password",
    "registration_problems",
    "switch_account",
    "technical_support",
    "account_issue",
    "login_problem",
    "bug_report",
}

GENERAL_INTENTS = {
    "cancel_order",
    "change_order",
    "change_shipping_address",
    "complaint",
    "contact_customer_service",
    "contact_human_agent",
    "newsletter_subscription",
    "place_order",
    "review",
    "set_up_shipping_address",
    "track_order",
    "general",
    "feedback",
}
