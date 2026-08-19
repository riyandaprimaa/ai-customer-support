"""
Ingestion CLI script.
Entry point to execute end-to-end data loading, embedding generation, and ChromaDB vector indexing.

Usage:
    uv run python -m src.scripts.ingest [--limit 100] [--reset]
"""

import argparse
import sys
from src.pipelines.data_loader import load_dataset_records, categorize_records
from src.pipelines.knowledge_base import KnowledgeBaseManager


def run_ingestion(limit: int = 500, reset: bool = False) -> None:
    """
    Execute the data ingestion pipeline.
    """
    print("=" * 60)
    print("Customer Support AI — Data Ingestion Pipeline (Spec AI-1)")
    print("=" * 60)

    kb = KnowledgeBaseManager()

    if reset:
        print("Reset flag detected. Clearing existing vector store collections...")
        kb.reset_all_collections()

    print(f"\nStep 1/3: Loading dataset records (limit={limit})...")
    records = load_dataset_records(limit=limit)

    print("\nStep 2/3: Categorizing records into domain categories...")
    categorized = categorize_records(records)
    for category, items in categorized.items():
        print(f"  - Category '{category}': {len(items)} records")

    print("\nStep 3/3: Embedding records and populating ChromaDB persistent collections...")
    total_added = 0
    for category, items in categorized.items():
        if items:
            added = kb.add_records(category=category, records=items)
            total_added += added

    print("\n" + "=" * 60)
    print(f"Ingestion Complete! Total records added across all collections: {total_added}")
    print("=" * 60)


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest customer support FAQ dataset into ChromaDB.")
    parser.add_argument("--limit", type=int, default=100, help="Maximum number of dataset records to ingest.")
    parser.add_argument("--reset", action="store_true", help="Reset existing vector collections before ingesting.")
    args = parser.parse_args()

    run_ingestion(limit=args.limit, reset=args.reset)


if __name__ == "__main__":
    main()
