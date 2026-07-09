# Contributing to Antigravity Obsidian Exporter

Thank you for your interest in contributing! This guide will get you set up quickly.

---

## 🛠 Development Setup

```bash
# 1. Fork and clone
git clone https://github.com/owrew/antigravity-obsidian-exporter.git
cd antigravity-obsidian-exporter

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows

# 3. Install in editable mode
pip install -e ".[watch,test]"

# 4. Run tests
python run_tests.py
```

---

## 🧪 Tests

Tests live in `tests/`. Run them with:

```bash
python run_tests.py
# or, if pytest is installed:
pytest tests/
```

Please add a test for any new parser, renderer, or analysis feature you add.

---

## 🗂 Project Layout

| Directory | Purpose |
|---|---|
| `agy_exporter/sources/` | Data loaders (JSONL, protobuf, SQLite) |
| `agy_exporter/analysis/` | Intelligence engine, relations, wiki-links |
| `agy_exporter/render/` | Markdown + index file generators |
| `agy_exporter/sync/` | Orchestrator, state tracker, file watcher |
| `tests/` | Unit tests |
| `examples/` | Example configs and sample outputs |

---

## 📝 Submitting Changes

1. **Open an issue first** for any non-trivial change so we can discuss it.
2. Create a branch: `git checkout -b feature/my-feature`
3. Write tests for your change.
4. Make sure `python run_tests.py` passes with 0 failures.
5. Open a Pull Request with a clear description and link to the issue.

---

## 🚫 What NOT to include in PRs

- Personal conversation data or transcripts
- Absolute Windows paths (`C:\Users\...`)
- Hard-coded credentials or API keys
- Any file matching `.gitignore`

---

## 🎨 Code Style

- Python 3.9+ compatible
- Type hints on all public functions
- Docstrings on all public classes and functions
- No lines longer than 100 characters
- f-strings preferred over `%` formatting in new code (except `logging` calls — use `%` there for performance)

---

## 📖 Documentation

If your change adds or modifies user-facing behaviour, please update:

- `README.md` (relevant section)
- `CHANGELOG.md` (under `[Unreleased]`)

---

## ❓ Questions?

Open a [GitHub Discussion](https://github.com/owrew/antigravity-obsidian-exporter/discussions) — we're happy to help.
