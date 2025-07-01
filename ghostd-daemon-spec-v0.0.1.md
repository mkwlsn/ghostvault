---
title: ghostd daemon spec
version: 0.0.1
status:
  - draft
  - review
source draft: 
author:
  - ghost (gpt-4o)
triage tags: []
created: 2025-07-01T13:06:00
last updated: 2025-07-01T13:06:00
---

# ghostd v0.0.1 – Minimal Daemon Specification 

## Purpose

`ghostd` is the symbolic executor of ghostOS. It powers the core execution loop:
- Models (or you) write proposals to `.ghost/output/`
- The daemon watches, validates, executes, logs, and updates context
- This loop makes ghostOS real—not just symbolic

This spec defines the initial working daemon: no rollback, no concurrency, just the loop.

---

## Directory Structure (Root: `/ghostvault/`)

```
.ghost/
├── output/         # Model or human ritual proposals
├── logs/           # Execution logs (one per ritual chain)
├── context/        # Minimal persistent state (last run, recent summary)
├── daemon/         # ghostd runtime and code
└── archive/        # Moved processed proposals
```

---

## Ritual Format (v0.0.1)

Proposals are single YAML files in `.ghost/output/`. Example:

```yaml
ritual_proposal:
  chain_id: "demo-001"
  rituals:
    - name: "file_write"
      args:
        path: "./sandbox/hello.txt"
        content: "Hello ghostOS"
  reasoning: "Create a demo file"
```

---

## Valid Rituals

| Ritual       | Args                      | Action                            |
|--------------|---------------------------|-----------------------------------|
| file_write   | path, content             | Write content to path             |
| mkdir        | path                      | Create directory if missing       |
| echo         | message                   | Print to stdout                   |

All other rituals are ignored or rejected. No schema enforcement yet.

---

## Execution Flow

1. **Watch** `.ghost/output/` for new YAML files  
2. For each file:
   - Parse and validate ritual structure
   - Log receipt to `.ghost/logs/<chain_id>.yaml`
   - Execute rituals in order:
     - Write output
     - Log result
     - On failure, skip remaining
   - Move processed file to `.ghost/archive/`
   - Update `.ghost/context/last.yaml` with summary

---

## Logging Format

```yaml
chain_id: demo-001
timestamp: 2025-07-01T10:30:00Z
status: "complete"
rituals:
  - name: "file_write"
    status: "success"
    path: "./sandbox/hello.txt"
    bytes_written: 87
```

---

## ghost_context/last.yaml

Tracks most recent run:

```yaml
last_execution:
  chain_id: demo-001
  status: success
  timestamp: 2025-07-01T10:30:00Z
  rituals_run: 1
```

---

## Out of Scope (v0.0.1)

- Rollback
- Error classes
- Ritual chaining logic
- Trust levels
- Runtime daemon monitoring
- Remote model integration

---

## Success Criteria

- [ ] Can drop ritual file into `.ghost/output/`
- [ ] `ghostd` runs, executes, and logs actions
- [ ] Processed file is moved to `.ghost/archive/`
- [ ] `.ghost/context/` receives summary update
- [ ] Daemon does not crash on malformed input

This is the minimal foundation for symbolic execution in ghostOS.

