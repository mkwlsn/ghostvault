# 🧩 system folder

this is where ghost runtime metadata and core code live.

includes:

- `ghost.py` — main CLI
- `ghostd.py` — background daemon (spawned via `ghost start`)
- `ghost_cli.py` — CLI entrypoint handler
- `ghost_runtime.py` — core runtime functions (e.g., log, queue, ritual)
- `ghost_utils.py` — utilities (macro expansion, status tools)
- `ghost_bootstrap.py` — bootstraps environment (sets paths, config, etc.)
- `ghost_registry.py` — module + ritual discovery / metadata
- `ghost_config.py` — runtime configuration management
- `ghost_install.py` — first-time setup script
- `ghost_init.py` — runtime prep (PATH, PYTHONPATH, directories)
- `ghost_queue.py` — queue logic
- `ghost_state.py` — state persistence

runtime data:

- `ghost-queue.md` — pending ops
- `config.json` — runtime settings
- `ghost_modules.py` — parsed module metadata

unit tests:

- `test_ghost.py` — unit tests
- `test_ghost_cli.py` — end-to-end CLI test suite
