# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Current Project Phase: Kernel Rebuild

**Status:** Building minimal execution kernel from 12 salvaged files in `/tmp/`
**Goal:** Flat, observable, testable automation substrate  
**Anti-Goals:** Symbolic layers, ritual execution, persona systems

## ghostOS-kernel Directory Structure (ENFORCED)

**Modular Layout:**
```
ghost/
├── daemon/              # Daemon runtime + loop
│   └── daemon.py
├── queue/               # Task queue and helpers  
│   └── queue.json
├── logs/                # Event logs (flat, timestamped)
│   └── events.md
├── config/              # Path and runtime constants
│   └── config.py
├── cli/                 # CLI entrypoint and helpers
│   └── cli.py
├── tests/               # Tests per issue (observable behavior only)
│   └── test_dependencies.py
```

**Constraints:**
- **NO** symbolic directories or runtime in project root
- **NO** unresolved tmp/ references in production code  
- **USE** relative imports within ghost/ modules
- **KEEP** flat but organized structure (no deep nesting)

**Development Principle: Build New, Don't Migrate**
- Create fresh module stubs for each component
- Copy only validated logic from legacy files
- Delete functions/references not covered by current issues
- Treat kernel as new OS build, not refactor of old system

**🔒 Dependency Constraint Rule:**
No code may be preserved from ghostOS-v0 unless:
- It is explicitly referenced by an active GitHub issue, OR
- It is accompanied by a `[v0_carryforward]` tag and justification

## Build Order (LOCKED CONSTRAINTS)

**Priority Sequence:**
1. **Daemon loop** that scans queue and runs shell scripts
2. **Queue format** + atomic status tracking  
3. **CLI** to enqueue and inspect
4. **Log writer** that records success/failure

**Rule:** Don't build CLI wrappers until underlying logic works in direct Python.

## Testing Strategy (LOCKED)

**Approach:** Functionality first, then tests.
- Tests follow once execution path is traceable and file I/O is structured
- Don't write tests against symbolic behavior or CLI scaffolding that might change
- Prioritize traceable state over comprehensive coverage

## Language Guidelines (LOCKED)

**Symbolic Language Policy:**
- **AVOID** in user-facing surfaces and execution logic
- **OK** in comments/variables if marked as symbolic/narrative reference
- **NEVER** encode personas, rituals, or recursive symbolic links into active logic

**Approved Symbolic Terms (from flattening position paper):**
- `ghost` — the system  
- `vault` — persistent memory  
- `ritual` — structured task  
- `daemon` — background worker  
- `daemon state` — status snapshot  
- `chunk` — input unit  
- `schema` — structure definition

All other symbolic terms must be flattened, archived, or aliased.

**LLM Alignment Constraint:**
Every command, queue entry, and log line must be parseable by a 1B model using stateless context.

This enforces:
- Shallow nesting
- Consistent schemas  
- Avoidance of latent symbolic coupling

**Example:**
```python
# ghost_mode = legacy symbolic placeholder — deprecated
daemon_running = check_process_status()  # literal function name
```

## GitHub Workflow (via `gh` CLI)

**Observable State Requirement:**
Every issue that changes behavior must reference:
- **Before state:** `python tmp/daemon.py` → `ImportError: No module named 'psutil'`
- **After state:** `python tmp/daemon.py` → `[daemon] scanning queue every 5s`  
- **Observation method:** `tail -f tmp/events.md` shows daemon startup log

**Exception for cosmetic changes:**
- Tag the file and line
- Include the new string
- Label `cosmetic`

**Issue Format:**
```
Title: [concise description]
Body:
1. Problem summary
2. Relevant files/logs  
3. Proposed action
4. Related constraints or specs (if any)

Labels: [claude, ghostOS-kernel]
```

## Development Guidelines

**DO:**
- Write testable, observable code
- Use literal function names  
- Create flat, traceable state
- Log everything to JSON/JSONL
- Build for humans and LLMs to read the same logs

**AVOID:**
- Symbolic variable names in execution logic
- Markdown-driven execution
- Hidden state or remote dependencies
- Ritual/persona execution patterns

## Essential Development Checks

**Path Configuration:**
```bash
python -c "import sys; sys.path.append('tmp'); from config import VAULT; print(VAULT)"
```

**Queue Validation:**
```bash
jq . tmp/queue.json
```

**Event Log Monitoring:**
```bash
tail -f tmp/events.md
```

*Note: Additional CLI flags shown are placeholders—implement only after core daemon functionality is proven.*

## Key Architectural Principles

**Local-First Execution:**
- All state in flat files (JSON, JSONL, Markdown)
- Inspectable with `cat`, `grep`, `jq`
- Zero infrastructure dependencies
- Human-readable logs that LLMs can also parse

**Traceable Behavior:**
- Every action logged with timestamp
- Queue operations are atomic
- Success/failure recorded in structured format
- No hidden state or implicit behavior

## Known Failure Modes from ghostOS-v0

Mitigated by current constraints—must remain under test:

- **Path confusion** - Legacy `/system/` vs `/ghost/` references
- **Dependency gaps** - Missing `psutil` breaking daemon functions
- **Import inconsistencies** - Circular dependencies in nested structure
- **Symbolic execution without runtime behavior** - Markdown "modules" with no execution hooks
- **Token overhead** - Symbolic language preventing small model compatibility

## Important Context

This is a **minimal automation kernel** designed for:
- Persistent human-LLM collaboration
- Observable task execution  
- Shared symbolic understanding through logs, not code
- Path to symbolic layering once execution foundation is proven

The system acts as a collaborative substrate, not just a tool.