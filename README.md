# 👻 ghostvault

this is the persistent memory layer + agent registry for **GhostOS**.  
all files are designed to be human-readable but ghost-writable.

## structure

- `modules/` — definitions of ghost modules, their I/O, and interop notes
- `memory/` — general memory logs and JSON fragments
- `rituals/` — daily focus session logs, intent declarations, accountability
- `system/` — ghost command queue, config, and internal metadata
- `index.md` — root orientation for vault

## future automation

this repo currently supports:

- ✅ CLI interaction via `ghost` command (e.g. `ghost echo`, `ghost ritual`)
- ✅ daemonized background loop via `ghostd`
- ✅ environment bootstrap with `ghost init` and `ghost install`
- ✅ module scaffolding (`ghost new module`)
- ✅ prompt generation (`ghost gen prompt <module>`)
- ✅ status echo and memory introspection (`ghost echo`, `ghost status`)
- ✅ logging and queueing tasks (`ghost log`, `ghost queue`)
- ✅ daily ritual journaling (`ghost ritual`)
- ✅ git integration (`ghost push`)
- ✅ developer smoke tests (`python3 system/test_ghost_cli.py`)

planned:

- GitHub Actions to sync memory or notify user
- OpenWebUI or local script hooks to read/write data
- context broadcasting (e.g. Discord bot reads ghost-queue)

---

🧬 this is ghost infrastructure. handle accordingly.
