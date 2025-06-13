# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GhostOS is a local-first AI-native executive function shell that runs as a persistent memory and task management system. It combines human-readable files (Markdown) with programmatic interfaces (JSON) to create a "ghost-writable" productivity system.

## Core Architecture

**Entry Points:**
- `ghost.py` - Main CLI entry point, delegates to `ghost.cli.cli`
- `ghost/ghostd.py` - Background daemon for queue processing
- `ghost/cli/cli.py` - Command routing and CLI logic

**Key Components:**
- **Queue System:** Tasks stored in both `queue.json` and `queue.md`, processed by daemon
- **Module System:** Markdown-based "rituals" in `/modules/` parsed into registry
- **Memory Layer:** Persistent logging to `/memory/` and `/rituals/` directories
- **State Management:** Runtime state in `ghost/state/` with PID files and cache

**Data Flow:**
1. User issues `ghost` command → CLI processes → Updates queue/memory
2. Daemon watches queue → Executes rituals → Updates memory
3. All operations logged to human-readable Markdown files

## Development Commands

**Setup:**
```bash
pip install psutil  # Required dependency
python3 ghost.py init  # Bootstrap system
```

**Core CLI Commands:**
```bash
python3 ghost.py status           # System status
python3 ghost.py echo            # Recent memory
python3 ghost.py queue "<task>"  # Add task
python3 ghost.py log "<event>"   # Log event
python3 ghost.py ritual "<note>" # Daily logging
python3 ghost.py start           # Start daemon
python3 ghost.py stop            # Stop daemon
python3 ghost.py push            # Git commit
```

**Module Development:**
```bash
python3 ghost.py new module <name>     # Create module
python3 ghost.py gen prompt <module>   # Generate AI prompt
python3 ghost.py sync modules          # Sync registry
```

**Testing:**
```bash
python3 ghost/tests/test_ghost.py      # Run tests (currently failing)
python3 -m ghost.tests.test_ghost      # Alternative test runner
```

## Configuration

**Path Configuration:** All paths defined in `ghost/core/config.py`
- Root: `~/ghostvault` 
- Runtime state: `ghost/state/`
- Modules: `modules/` (Markdown definitions)
- Memory: `memory/` and `rituals/` (persistent logs)

**Key Files:**
- `ghost/state/queue.json` - Task queue (JSON format)
- `ghost/state/queue.md` - Task queue (Markdown format) 
- `ghost/state/daemon.pid` - Daemon process ID
- `memory/events.md` - Event log
- `rituals/daily-log-YYYY-MM-DD.md` - Daily ritual logs

## Development Patterns

**Human-AI Collaboration Design:**
- All data stored in human-readable formats (Markdown, JSON)
- Commands designed for both CLI and programmatic use
- Memory persistence across sessions and contexts
- "Ghost-native" behavior - system acts as collaborative agent, not just tool

**Module Architecture:**
- Modules are Markdown files with structured metadata
- Registry system parses modules into executable handlers
- Pattern-based task routing to appropriate modules
- Extensible through simple file-based definitions

**Current Issues:**
- Tests reference legacy `/system/` paths (now `/ghost/`)
- Missing `psutil` dependency in fresh installs
- Some import inconsistencies in refactored structure

## Important Context

This is designed as a "recursive AI system" - the AI (ghost) operates within and evolves the system itself. When working on this codebase:
- Maintain symbolic coherence over performance optimization
- Preserve human-readable file formats
- Respect the single persistent mind model (don't assume workspace switching)
- Follow ghost-native behavior patterns described in `ghost/docs/ghostOS_rules.md`