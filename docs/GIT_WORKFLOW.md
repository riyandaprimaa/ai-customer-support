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

## 4. Useful Git Commands Cheat Sheet

| Action | Command |
|---|---|
| **Create and switch to new branch** | `git checkout -b <branch-name>` |
| **Check branch status** | `git status` |
| **Stage all changes** | `git add .` |
| **Commit with message** | `git commit -m "feat(scope): message"` |
| **Push new branch to remote** | `git push -u origin <branch-name>` |
| **Delete local branch** | `git branch -d <branch-name>` (or `-D` to force) |
| **Delete remote branch** | `git push origin --delete <branch-name>` |
| **Switch back to main** | `git checkout main` |
| **Pull latest changes** | `git pull origin main` |
