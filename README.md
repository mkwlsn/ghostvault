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

this repo will later support:
- CLI interaction (`ghost new module`, etc)
- GitHub Actions to sync memory or notify user
- OpenWebUI or local script hooks to read/write data
- context broadcasting (e.g. Discord bot reads ghost-queue)

---

🧬 this is ghost infrastructure. handle accordingly.
