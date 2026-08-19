# AI Pipeline & Kernel Environment Setup Guide

> **Purpose:** Step-by-step setup manual for Python virtual environments, dependency management with `uv`, Jupyter notebook kernel registration, CLI script execution, and test workflows.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Python Virtual Environment Setup (via `uv`)](#2-python-virtual-environment-setup-via-uv)
3. [Jupyter Notebook Kernel Setup](#3-jupyter-notebook-kernel-setup)
4. [Running Pipeline Scripts & Ingestion CLI](#4-running-pipeline-scripts--ingestion-cli)
5. [Running Unit Tests](#5-running-unit-tests)
6. [Interactive Notebooks Best Practices (`sandbox.ipynb`)](#6-interactive-notebooks-best-practices-sandboxipynb)
7. [Adding New Dependencies](#7-adding-new-dependencies)
8. [Troubleshooting & FAQs](#8-troubleshooting--faqs)

---

## 1. Prerequisites

- **Operating System:** Windows 10/11 (or macOS / Linux)
- **Python:** Python `>= 3.11`
- **Package Manager:** `uv` (Fast Python package and project manager)
  - Verify installation:
    ```bash
    uv --version
    ```
  - If `uv` is not installed:
    ```powershell
    # Windows (PowerShell)
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

---

## 2. Python Virtual Environment Setup (via `uv`)

All Python dependencies for the AI pipeline are isolated in the `ai/` folder using `uv`.

### Step 2.1: Navigate to the `ai` directory
Always make sure your terminal's current working directory is `ai/`:
```bash
cd d:\Learning\projects\ai-customer-support\ai
```

### Step 2.2: Create and Sync the Virtual Environment
Create the virtual environment (`.venv`) and install all dependencies locked in `pyproject.toml` / `uv.lock`:
```bash
uv sync
```
This automatically installs:
- Core LLM & Agent frameworks: `langchain`, `langchain-google-genai`, `langchain-groq`, `langgraph`
- Vector DB & Embeddings: `chromadb`, `sentence-transformers`
- Data & Utilities: `datasets`, `pandas`, `python-dotenv`
- Evaluation & Testing: `ragas`, `pytest`, `ipykernel`

---

## 3. Jupyter Notebook Kernel Setup

To run Jupyter Notebooks (like `sandbox.ipynb`) inside Antigravity IDE or VS Code with all project dependencies:

### Step 3.1: Install `ipykernel` (already configured as dev dependency)
If you ever start from a fresh environment, ensure `ipykernel` is installed:
```bash
uv add --dev ipykernel
```

### Step 3.2: Register the Kernel with Jupyter
Register your virtual environment as a distinct, selectable Jupyter kernel:
```bash
uv run python -m ipykernel install --user --name ai-customer-support --display-name "Python (Customer Support AI)"
```

### Step 3.3: Select the Kernel in your Notebook
1. Open any `.ipynb` file (e.g. `ai/sandbox.ipynb`).
2. In the top-right corner of the editor, click **Select Kernel** (or the current Python version).
3. Select **Jupyter Kernel...** -> **Python (Customer Support AI)**.
   - *Alternative:* Choose **Python Environments...** -> navigate to `d:\Learning\projects\ai-customer-support\ai\.venv\Scripts\python.exe`.

---

## 4. Running Pipeline Scripts & Ingestion CLI

`uv run` executes Python commands within the virtual environment without needing to manually activate `.venv`.

### Running Data Ingestion
Ingests customer support FAQ records into persistent ChromaDB collections (`billing_kb`, `technical_kb`, `general_kb`):

```bash
# Ingest 100 sample records (default)
uv run python -m src.scripts.ingest

# Ingest custom amount (e.g. 500 records)
uv run python -m src.scripts.ingest --limit 500

# Reset/clear existing ChromaDB collections before ingesting
uv run python -m src.scripts.ingest --limit 500 --reset
```

---

## 5. Running Unit Tests

Automated tests are located in `ai/tests/`.

```bash
# Run all unit tests
uv run pytest

# Run tests with verbose output and print statements
uv run pytest -v -s

# Run a specific test file
uv run pytest tests/test_data_loader.py
uv run pytest tests/test_knowledge_base.py
```

---

## 6. Interactive Notebooks Best Practices (`sandbox.ipynb`)

When working inside a notebook within a subfolder (`ai/`), Python's default import path might not always resolve the root `src/` package automatically.

### Recommended Notebook Header Cell:
Always put this at the very top cell of your `.ipynb` notebook:

```python
import sys
from pathlib import Path

# Add project root ('ai' folder) to sys.path
PROJECT_ROOT = Path.cwd()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Test imports
from src.config import CHROMA_DB_DIR, EMBEDDING_MODEL_NAME
from src.pipelines.data_loader import load_dataset_records, categorize_records
from src.pipelines.knowledge_base import KnowledgeBaseManager

print("Environment ready! Imports successful.")
```

---

## 7. Adding New Dependencies

When you need to install additional Python packages:

```bash
# Add a runtime package
uv add <package_name>

# Add a development/testing package
uv add --dev <package_name>

# Example: adding matplotlib or seaborn for EDA
uv add --dev matplotlib seaborn
```

This updates both `pyproject.toml` and `uv.lock` deterministically.

---

## 8. Troubleshooting & FAQs

### Q1: Kernel is not appearing in the list in IDE
**Solution:**
Re-register the kernel spec in PowerShell/terminal:
```powershell
cd d:\Learning\projects\ai-customer-support\ai
uv run python -m ipykernel install --user --name ai-customer-support --display-name "Python (Customer Support AI)"
```
Then reload IDE window or restart IDE.

---

### Q2: `ModuleNotFoundError: No module named 'src'` in Notebook
**Solution:**
Ensure you have added the current working directory to `sys.path` in the first cell:
```python
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))
```

---

### Q3: How to reset/recreate the virtual environment from scratch?
If your `.venv` ever gets corrupted:
```bash
# 1. Delete .venv folder
Remove-Item -Recurse -Force .venv

# 2. Re-sync clean environment
uv sync

# 3. Re-register Jupyter kernel
uv run python -m ipykernel install --user --name ai-customer-support --display-name "Python (Customer Support AI)"
```
