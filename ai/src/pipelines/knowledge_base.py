"""
Knowledge Base module.
Manages ChromaDB persistent vector database operations for specialist agent domains.
"""

from typing import Any
import uuid
import chromadb
from src.config import CHROMA_DB_DIR
from src.pipelines.embeddings import get_embedding_function


class KnowledgeBaseManager:
    """
    ChromaDB vector store manager maintaining persistent collections for:
    - billing_kb
    - technical_kb
    - general_kb
    """

    COLLECTION_NAMES = {
        "billing": "billing_kb",
        "technical": "technical_kb",
        "general": "general_kb",
    }

    def __init__(self, persist_directory: str = CHROMA_DB_DIR):
        self.persist_directory = persist_directory
        print(f"Initializing ChromaDB PersistentClient at: {persist_directory}")
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.embedding_fn = get_embedding_function()

    def get_collection_name(self, category: str) -> str:
        """
        Get collection name corresponding to category.
        """
        cat_clean = category.lower().strip()
        return self.COLLECTION_NAMES.get(cat_clean, "general_kb")

    def get_or_create_collection(self, category: str) -> Any:
        """
        Retrieve or create a ChromaDB collection for a category.
        """
        collection_name = self.get_collection_name(category)
        return self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn,  # type: ignore
        )

    def add_records(self, category: str, records: list[dict[str, Any]]) -> int:
        """
        Insert clean FAQ records into the corresponding ChromaDB vector collection.
        Combines query and response into document text for optimal similarity search context.
        """
        if not records:
            return 0

        collection = self.get_or_create_collection(category)

        ids: list[str] = []
        documents: list[str] = []
        metadatas: list[dict[str, Any]] = []

        for record in records:
            doc_id = str(uuid.uuid4())
            query = record.get("query", "")
            response = record.get("response", "")
            intent = record.get("intent", "general")

            # Document text indexed in vector space
            doc_text = f"Question: {query}\nAnswer: {response}"

            ids.append(doc_id)
            documents.append(doc_text)
            metadatas.append(
                {
                    "query": query,
                    "response": response,
                    "intent": intent,
                    "category": category,
                }
            )

        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
        )

        count = len(ids)
        print(f"Added {count} records to collection '{collection.name}'. Total items: {collection.count()}")
        return count

    def query(self, query_text: str, category: str, n_results: int = 3) -> list[dict[str, Any]]:
        """
        Query vector collection for similarity matches against user input query.
        """
        collection = self.get_or_create_collection(category)
        if collection.count() == 0:
            return []

        results = collection.query(
            query_texts=[query_text],
            n_results=min(n_results, collection.count()),
        )

        matched_items: list[dict[str, Any]] = []
        if results and results.get("documents") and results["documents"][0]:
            docs = results["documents"][0]
            metas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(docs)
            dists = results["distances"][0] if results.get("distances") else [0.0] * len(docs)

            for doc, meta, dist in zip(docs, metas, dists):
                matched_items.append(
                    {
                        "document": doc,
                        "query": meta.get("query", ""),
                        "response": meta.get("response", ""),
                        "intent": meta.get("intent", ""),
                        "category": meta.get("category", category),
                        "distance": dist,
                        "relevance_score": max(0.0, 1.0 - dist),
                    }
                )

        return matched_items

    def reset_all_collections(self) -> None:
        """
        Clear and reset all knowledge base collections.
        """
        for cat, col_name in self.COLLECTION_NAMES.items():
            try:
                self.client.delete_collection(name=col_name)
                print(f"Deleted existing collection '{col_name}'.")
            except Exception:
                pass
