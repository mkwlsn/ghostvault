# 🏛️ GhostOS Architecture

GhostOS is a local-first executive function shell. It runs as a background daemon (`ghostd.py`), watches a symbolic task queue (`queue.json`), and executes modular instructions called **rituals**—written in Markdown and loaded into memory via a registry system.

---

## 🧠 Core Design Principles

- **Single persistent mind:** GhostOS operates from a root directory (usually `~/ghostvault`) and treats all external inputs (repos, vaults, directories) as symbolic material to ingest—not alternate “workspaces.”
- **Symbolic execution:** Tasks are encoded as rituals—human-readable, LLM-readable, and eventually agent-executable.
- **Modular backbone:** CLI is thin; logic is handled in `system/`. Everything routes through `ghost.py` and queue logic.

---

## ⚙️ Component Breakdown

| Component         | Role                                      |
|------------------|-------------------------------------------|
| `ghostd.py`       | Background daemon                        |
| `ghost.py`        | Symbolic CLI interface                   |
| `queue.json`      | Task queue, watched by `ghostd.py`      |
| `modules/`        | Ritual markdown files                    |
| `ghost_registry.py` | Registry of parsed modules             |
| `system/`         | Modular CLI handlers and internal logic  |
| `ghost_docs/`     | Canonical documentation                  |

---

## 🔁 Ritual Lifecycle

1. Ritual is defined in `modules/<name>.md`
2. Parsed into `ghost_registry.py`
3. CLI or `ghostd.py` queues it to `queue.json`
4. Executor module (usually `ghost_ritual.py`) interprets and runs it

---

## 🌐 Future Extensibility

- Add LLM-internal agent reflection
- Sync with multiple symbolic environments
- Drive custom workflow orchestration across repos