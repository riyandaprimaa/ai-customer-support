# Git Versioning & Branching Workflow

> **Purpose:** Standard Git workflow, branch naming conventions, commit guidelines, and Pull Request lifecycle for the 2-person development team (AI Engineer + Software Engineer).

---

## 1. Branch Naming Strategy

We follow a **Feature-Branch Workflow** directly aligned with our Spec IDs (`AI-1`, `API-1`, `WEB-1`, etc.).

### Branch Naming Formula:
`<type>/<spec-code>-<short-description>`

| Branch Type | When to Use | Naming Pattern | Example |
|---|---|---|---|
| **`feature/`** | Implementing a new Spec deliverable | `feature/<spec-code>-<theme>` | `feature/ai-1-data-pipeline`, `feature/api-1-fastapi-backend` |
| **`docs/`** | Standalone documentation or journals | `docs/<description>` | `docs/week-01-journal`, `docs/update-architecture` |
| **`chore/`** | Configs, dependencies, gitignore | `chore/<description>` | `chore/update-dependencies`, `chore/setup-linters` |
| **`fix/`** | Bug fix on an existing feature | `fix/<description>` | `fix/chromadb-query-timeout` |
| **`refactor/`** | Code refactoring without new features | `refactor/<description>` | `refactor/clean-knowledge-base-utils` |

---

## 2. Rule of Thumb: What Goes in a Feature Branch? (Atomic PRs)

### ✅ What to include in the same `feature/` branch:
1. **Feature source code** (e.g. `src/pipelines/data_loader.py`).
2. **Automated unit/integration tests** (e.g. `tests/test_data_loader.py`).
3. **Spec documentation & updates** (e.g. `docs/specs/YYYY-MM-DD-spec-AI1-...md`, updating `SPEC-INDEX.md` and `DELIVERY-STATUS.md`).
4. **Developer setup guides & test sandboxes for that feature** (e.g. `SETUP_GUIDE.md`, `sandbox.ipynb`).

> **Why?** Keeping documentation, tests, and code together ensures that every Pull Request is self-contained and atomic. When merged into `main`, the docs and code stay 100% in sync.

---

## 3. End-to-End Spec Lifecycle in Git

### Step 1: Start a New Spec
Before starting work on a spec (e.g. `AI-2`), ensure you are on latest `main`:
```bash
git checkout main
git pull origin main
git checkout -b feature/ai-2-rag-pipeline
```

### Step 2: Work & Commit Progressively
Use **Conventional Commits** format:
- `feat(ai): add query retriever for chroma collections`
- `test(ai): add unit tests for top-k similarity search`
- `docs(specs): mark AI-2 as done in SPEC-INDEX.md`

### Step 3: Run Verification
Before pushing, ensure tests pass:
```bash
# For AI pipeline:
cd ai
uv run pytest
```

### Step 4: Push Branch & Open Pull Request (PR)
```bash
git push -u origin feature/ai-2-rag-pipeline
```
1. Open GitHub and create a Pull Request: `feature/ai-2-rag-pipeline` ➔ `main`.
2. Assign your teammate for peer review.
3. Once approved and checks pass, merge into `main` using **Squash & Merge** (or Create a Merge Commit).

### Step 5: Clean Up Branch
After merging to `main`:
```bash
git checkout main
git pull origin main
# Delete local branch
git branch -d feature/ai-2-rag-pipeline
```

---

## 4. Pull Request (PR) Naming Standards

To ensure clean, uniform repository history and portfolio presentation, all Pull Requests must follow this standardized naming convention:

### PR Title Formula:
`<type>(<scope>): [<spec-code>] <Short descriptive summary>`

| Scope | Spec / Deliverable | Standard PR Title Example |
|---|---|---|
| **`ai`** | Spec AI-1 | `feat(ai): [AI-1] implement data ingestion pipeline and ChromaDB vector store` |
| **`ai`** | Spec AI-2 | `feat(ai): [AI-2] implement RAG retrieval pipeline and multi-LLM fallback` |
| **`ai`** | Spec AI-3 | `feat(ai): [AI-3] implement orchestrator agent and intent router` |
| **`ai`** | Spec AI-4 | `feat(ai): [AI-4] implement 3 specialist agents and conversation memory` |
| **`api`** | Spec API-1 | `feat(api): [API-1] initialize FastAPI backend and SQLite database` |
| **`web`** | Spec WEB-1 | `feat(web): [WEB-1] create React chat UI and streaming SSE` |
| **`int`** | Spec INT-1 | `feat(int): [INT-1] connect AI pipeline to FastAPI chat endpoint` |
| **`monorepo`** / **`docs`** | Spec M1 / ADRs | `feat(monorepo): [M1] setup monorepo structure and local dev environment` |
| **`chore`** | Maintenance | `chore(repo): update dependencies and gitignore` |

---

## 5. Useful Git Commands Cheat Sheet

### 📦 Staging & Unstaging Changes
| Action | Command |
|---|---|
| **Check current status** | `git status` |
| **Stage specific file** | `git add <file-path>` |
| **Stage all changes** | `git add .` |
| **Un-add / Unstage a specific file** | `git restore --staged <file-path>` |
| **Un-add / Unstage all files** | `git restore --staged .` |

### 🗑️ Discarding Changes
| Action | Command |
|---|---|
| **Discard unstaged modifications in a file** | `git restore <file-path>` |
| **Discard all unstaged modifications** | `git restore .` |
| **Remove all untracked files/folders** | `git clean -fd` |

### 🗄️ Stashing (Temporarily Shelve Work)
| Action | Command |
|---|---|
| **Stash all uncommitted changes** | `git stash` |
| **Stash with a descriptive message** | `git stash save "wip: halfway through rag retriever"` |
| **Stash a specific file only** | `git stash push <file-path>` |
| **Restore most recent stash and remove it** | `git stash pop` |
| **View all stashes** | `git stash list` |
| **Delete most recent stash without applying** | `git stash drop` |

### 🌿 Branch Management & Switching
| Action | Command |
|---|---|
| **Create and switch to new branch** | `git checkout -b <branch-name>` |
| **Switch to an existing branch** | `git checkout <branch-name>` |
| **List all local branches** | `git branch` |
| **Delete local branch (safe)** | `git branch -d <branch-name>` |
| **Force delete local branch** | `git branch -D <branch-name>` |
| **Delete remote branch on GitHub** | `git push origin --delete <branch-name>` |

### 🔍 Diffs & History
| Action | Command |
|---|---|
| **View unstaged changes diff** | `git diff` |
| **View staged changes diff** | `git diff --staged` |
| **View concise commit history** | `git log --oneline -n 10` |
| **Undo last commit (keep changes staged)** | `git reset --soft HEAD~1` |
| **Undo last commit (keep changes unstaged)** | `git reset HEAD~1` |
