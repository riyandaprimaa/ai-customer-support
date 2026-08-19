# AI Pipeline Component

Multi-agent RAG pipeline for Customer Support AI — data ingestion, ChromaDB vector store, and LangGraph agents.

## 📖 Setup & Development Guide

For complete, step-by-step instructions on setting up your Python virtual environment with `uv`, registering the Jupyter kernel for notebooks, running ingestion, and executing unit tests, see:

👉 **[`SETUP_GUIDE.md`](./SETUP_GUIDE.md)**

## Quick Start

```bash
# 1. Sync dependencies
uv sync

# 2. Register Jupyter Kernel
uv run python -m ipykernel install --user --name ai-customer-support --display-name "Python (Customer Support AI)"

# 3. Run Ingestion CLI
uv run python -m src.scripts.ingest --limit 100

# 4. Run Tests
uv run pytest
```
