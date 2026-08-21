"""
Pipelines subpackage.
Exports core pipeline classes: DataLoader, Embeddings, KnowledgeBase, LLMClient, RAGRetriever.
"""

from src.pipelines.data_loader import (
    categorize_intent,
    clean_record,
    load_dataset_records,
    categorize_records,
    get_seed_dataset,
)
from src.pipelines.embeddings import get_embedding_function, SentenceTransformerEmbeddingFunction
from src.pipelines.knowledge_base import KnowledgeBaseManager
from src.pipelines.llm_client import LLMClient
from src.pipelines.retriever import RAGRetriever

__all__ = [
    "categorize_intent",
    "clean_record",
    "load_dataset_records",
    "categorize_records",
    "get_seed_dataset",
    "get_embedding_function",
    "SentenceTransformerEmbeddingFunction",
    "KnowledgeBaseManager",
    "LLMClient",
    "RAGRetriever",
]
