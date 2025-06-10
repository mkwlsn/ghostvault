# Ghost Structure Refactor Script

A comprehensive bash script for restructuring the GhostOS project from a flat `system/` directory to a modular `ghost/` package structure with proper Python packaging, centralized configuration, and robust error handling.

## Overview

This script performs a complete one-shot refactoring of the GhostOS codebase, moving from:

```
system/
├── ghost_*.py files
├── _docs/
└── ghost-queue.md
```

To:

```
ghost/
├── cli/        # Command-line interface
├── core/       # Core runtime logic
├── module/     # Module system
├── utils/      # Utilities
├── tests/      # Test files
├── docs/       # Documentation
└── state/      # Runtime state files
```

## Features

### 🛡️ Safety & Reliability

- **Pre-flight validation** - Checks git status, required files, and working directory
- **Automatic rollback** - Creates backup commit reference for recovery if anything fails
- **Comprehensive error handling** - No silent failures, all operations logged
- **Import validation** - Tests that all imports work after restructuring

### 📦 Configuration Management

- **Path consolidation** - Moves hardcoded paths to centralized config
- **QUEUE_MD constant** - Properly handles the markdown queue file location
- **Future-proof structure** - Easy to modify paths programmatically

### 🔧 File Operations

- **Git-aware moves** - Uses `git mv` to preserve file history
- **Package structure** - Creates proper `__init__.py` files
- **Cache cleanup** - Removes `__pycache__` and `.pyc` files
- **Import rewriting** - Updates all import statements to new structure

### 📊 Validation & Testing

- **Import testing** - Validates core modules can be imported
- **CLI validation** - Tests command-line interface functionality
- **Pytest integration** - Runs existing tests if available
- **Path verification** - Confirms config constants resolve correctly

## Prerequisites

- Git repository with clean working directory (no uncommitted changes)
- Python 3.10+
- All required source files present in `system/` directory
- Pytest (optional, for running tests)

## Usage

```bash
# Make executable
chmod +x ghost_structure_refactor.sh

# Run the refactor
./ghost_structure_refactor.sh
```

## What It Does

### Phase 1: Preparation

1. **Pre-flight checks** - Validates environment and git status
2. **Backup creation** - Records current commit for rollback capability
3. **Path consolidation** - Updates config files with new structure paths

### Phase 2: Structure Creation

4. **Directory scaffold** - Creates new `ghost/` package structure
5. **Package initialization** - Adds `__init__.py` files for Python packages

### Phase 3: File Migration

6. **CLI files** → `ghost/cli/`
7. **Core logic** → `ghost/core/`
8. **Module system** → `ghost/module/`
9. **Utilities** → `ghost/utils/`
10. **Tests** → `ghost/tests/`
11. **Documentation** → `ghost/docs/`
12. **Queue file** → `ghost/state/queue.md`

### Phase 4: Configuration Updates

13. **Config path updates** - Updates config to reflect final structure
14. **Import rewrites** - Fixes all import statements
15. **Reference updates** - Updates file references to use config constants

### Phase 5: Validation

16. **Import testing** - Validates core functionality
17. **CLI testing** - Ensures command-line interface works
18. **Test execution** - Runs pytest if tests exist

## File Mapping

| Original Location         | New Location                 | Purpose             |
| ------------------------- | ---------------------------- | ------------------- |
| `system/ghost.py`         | `ghost/cli/ghost.py`         | Main CLI entry      |
| `system/ghostd.py`        | `ghost/ghostd.py`            | Daemon (root level) |
| `system/ghost_cli.py`     | `ghost/cli/cli.py`           | CLI handlers        |
| `system/ghost_config.py`  | `ghost/core/config.py`       | Configuration       |
| `system/ghost_queue.py`   | `ghost/core/queue.py`        | Queue management    |
| `system/ghost_runtime.py` | `ghost/core/runtime.py`      | Runtime functions   |
| `system/ghost_state.py`   | `ghost/core/state.py`        | State management    |
| `system/ghost_modules.py` | `ghost/module/modules.py`    | Module system       |
| `system/ghost_utils.py`   | `ghost/utils/ghost_utils.py` | Utilities           |
| `system/test_ghost.py`    | `ghost/tests/test_ghost.py`  | Tests               |
| `system/_docs/*.md`       | `ghost/docs/*.md`            | Documentation       |
| `system/ghost-queue.md`   | `ghost/state/queue.md`       | Task queue          |

## Configuration Constants

The script consolidates path management into `ghost/core/config.py`:

```python
# Root directories
VAULT = Path.home() / "ghostvault"
GHOST_ROOT = VAULT / "ghost"

# Package directories
CLI_DIR = GHOST_ROOT / "cli"
CORE_DIR = GHOST_ROOT / "core"
MODULE_DIR = GHOST_ROOT / "module"
UTILS_DIR = GHOST_ROOT / "utils"
STATE_DIR = GHOST_ROOT / "state"

# Runtime files
QUEUE_JSON = STATE_DIR / "queue.json"
QUEUE_MD = STATE_DIR / "queue.md"
DAEMON_PID = STATE_DIR / "daemon.pid"
```

## Error Handling

- **Rollback capability** - Automatically reverts to backup commit on failure
- **Detailed logging** - Color-coded output with progress indicators
- **Validation checks** - Confirms all operations completed successfully
- **Recovery instructions** - Clear guidance if manual intervention needed

## Post-Refactor Verification

After successful completion, verify with:

```bash
# Check file moves
git diff --name-status

# Test imports
python3 -c "from ghost.core.config import VAULT; print(f'Vault: {VAULT}')"

# Test CLI
python3 ghost/cli/ghost.py --help

# Run tests
python3 -m pytest ghost/tests/ -v
```

## Troubleshooting

### Script Fails Mid-Execution

- Script automatically attempts rollback to previous commit
- Check error messages for specific failure point
- Ensure working directory is clean before retry

### Import Errors After Refactor

- Verify all `__init__.py` files exist in package directories
- Check that `scripts/update_imports.py` ran successfully
- Manually verify import paths in affected files

### Missing Files

- Check `skipped` array in script output for files that couldn't be moved
- Verify all source files existed before running script
- Review git status for any uncommitted changes

## Development Notes

This script is designed for the specific GhostOS project structure but can be adapted for similar Python package refactoring tasks. Key principles:

- **Atomic operations** - Either complete success or full rollback
- **Git integration** - Preserves file history through git mv
- **Validation-first** - Tests everything before declaring success
- **Configuration consolidation** - Centralizes path management for future flexibility
