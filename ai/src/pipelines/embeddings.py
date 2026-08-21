"""
Embeddings module.
Wraps sentence-transformers model (all-MiniLM-L6-v2 per ADR-0003) for vector embeddings.
"""

from typing import Any
import chromadb.utils.embedding_functions as ef
from src.config import EMBEDDING_MODEL_NAME


class SentenceTransformerEmbeddingFunction(ef.EmbeddingFunction):
    """
    ChromaDB compatible embedding function using sentence-transformers.
    Runs locally on CPU with lightweight 80MB footprint (384-dimensional vectors).
    """

    def __init__(self, model_name: str = EMBEDDING_MODEL_NAME):
        from sentence_transformers import SentenceTransformer  # type: ignore

        self.model_name = model_name
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)

    def __call__(self, input: list[str]) -> list[list[float]]:
        """
        Generate embedding vectors for a list of input texts.
        """
        embeddings = self.model.encode(list(input), convert_to_numpy=True)
        return embeddings.tolist()

    def name(self) -> str:
        return "sentence_transformer"

    def embed_query(self, query: str) -> list[float]:
        """
        Embed a single query string.
        """
        return self.__call__([query])[0]


def get_embedding_function(model_name: str = EMBEDDING_MODEL_NAME) -> Any:
    """
    Factory function returning a ChromaDB compatible embedding function.
    """
    try:
        return ef.SentenceTransformerEmbeddingFunction(model_name=model_name)
    except Exception as e:
        print(f"Notice: Falling back to custom wrapper ({e}).")
        return SentenceTransformerEmbeddingFunction(model_name=model_name)
