---

# Ghost Structure Refactor Script

A focused bash script for restructuring the GhostOS project from a flat `system/` directory to a modular `ghost/` package structure with surgical precision - fixing only what's needed to maintain functionality.

## Overview

This script performs a **surgical refactoring** of the GhostOS codebase, moving from:

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

## Philosophy: "Just Enough" Refactoring

This script follows a **surgical approach**:

- ✅ **Fix what breaks** - Critical functionality preservation
- 📋 **Document what's messy** - Technical debt recorded for follow-up
- 🎯 **Single mission** - Make file structure work, nothing more

## Features

### 🛡️ **Safety & Reliability**

- **Pre-flight validation** - Checks git status, required files, and working directory
- **Automatic rollback** - Creates backup commit reference for recovery if anything fails
- **Surgical error handling** - Focused on critical path failures
- **Functional validation** - Tests that restructured code actually works

### 🔧 **Critical Functionality Preservation**

- **Daemon process management** - Updates process paths and PID file handling
- **CLI symlink management** - Detects and updates existing symlinks
- **Import chain fixes** - Ensures all module imports resolve correctly
- **Path reference updates** - Fixes hardcoded system/ paths in moved files

### 📦 **Configuration Management**

- **Path consolidation** - Centralizes hardcoded paths in config
- **QUEUE_MD constant** - Properly handles markdown queue file location
- **Future-proof structure** - Easy to modify paths programmatically

### 📋 **Technical Debt Management**

- **Follow-up documentation** - Creates `REFACTOR_FOLLOWUP.md` with cleanup recommendations
- **Quality vs. Critical separation** - Clear categorization of what was fixed vs. deferred
- **Action items** - Specific recommendations for post-refactor improvements

## Prerequisites

- Git repository with clean working directory (no uncommitted changes)
- Python 3.10+
- All required source files present in `system/` directory
- Active virtual environment (if using one)

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

### Phase 4: Critical Fixes

13. **Import chain fixes** - Updates all import statements
14. **Daemon functionality** - Fixes process management paths
15. **CLI preservation** - Updates symlinks and entry points
16. **Path reference cleanup** - Removes hardcoded system/ paths

### Phase 5: Validation & Documentation

17. **Functional testing** - Validates core functionality works
18. **Follow-up documentation** - Creates technical debt action items

## File Mapping

| Original Location         | New Location                 | Purpose             |
| ------------------------- | ---------------------------- | ------------------- |
| `system/ghost.py`         | `ghost/cli/ghost.py`         | CLI logic           |
| `system/ghostd.py`        | `ghost/ghostd.py`            | Daemon (root level) |
| `system/ghost_cli.py`     | `ghost/cli/cli.py`           | CLI handlers        |
| `system/ghost_daemon.py`  | `ghost/core/daemon.py`       | Process management  |
| `system/ghost_config.py`  | `ghost/core/config.py`       | Configuration       |
| `system/ghost_queue.py`   | `ghost/core/queue.py`        | Queue management    |
| `system/ghost_runtime.py` | `ghost/core/runtime.py`      | Runtime functions   |
| `system/ghost_state.py`   | `ghost/core/state.py`        | State management    |
| `system/ghost_modules.py` | `ghost/module/modules.py`    | Module system       |
| `system/ghost_utils.py`   | `ghost/utils/ghost_utils.py` | Utilities           |
| `system/test_ghost.py`    | `ghost/tests/test_ghost.py`  | Tests               |
| `system/_docs/*.md`       | `ghost/docs/*.md`            | Documentation       |
| `system/ghost-queue.md`   | `ghost/state/queue.md`       | Task queue          |
| **NEW:** `ghost.py`       | `ghost.py` (root)            | CLI entry point     |

## Critical Fixes Applied

### 🔧 **Daemon Process Management**

- Updates daemon process paths to find executable in new location
- Fixes PID file handling to use absolute paths from config
- Ensures daemon start/stop functionality survives restructure

### 🔗 **CLI Symlink Management**

- Detects existing CLI symlinks in `~/.local/bin/ghost`
- Updates symlink targets to point to new root CLI entry point
- Preserves global CLI access without manual intervention

### 📦 **Import Chain Integrity**

- Rewrites all import statements to use new package structure
- Fixes cross-module dependencies and circular import potential
- Validates that all imports resolve correctly after restructure

### 🗂️ **Path Reference Cleanup**

- Removes hardcoded `system/` path references from moved files
- Updates configuration constants to reflect new structure
- Ensures path-dependent functionality works with new layout

## What's NOT Fixed (By Design)

The following issues are **documented but deferred** to follow-up PRs:

### 📋 **Technical Debt (Non-Breaking)**

- **Bootstrap code cleanup** - PYTHONPATH manipulation in install scripts
- **Shell RC pollution** - Environment modifications in user's shell config
- **File consolidation** - Multiple bootstrap files with overlapping functionality
- **Obsolete functions** - Dead code that doesn't affect functionality

### 📝 **Follow-up Actions**

After successful refactor, see `REFACTOR_FOLLOWUP.md` for:

- Bootstrap code simplification opportunities
- Configuration improvements
- Additional testing recommendations
- Code quality enhancements

## Error Handling

- **Rollback capability** - Automatically reverts to backup commit on failure
- **Detailed logging** - Color-coded output with progress indicators
- **Validation checks** - Confirms all critical operations completed successfully
- **Recovery guidance** - Clear instructions if manual intervention needed

## Post-Refactor Verification

After successful completion, verify with:

```bash
# Check file moves
git diff --name-status

# Test imports
python3 -c "from ghost.core.config import VAULT; print(f'Vault: {VAULT}')"

# Test CLI
python3 ghost.py --help

# Test daemon functionality
python3 -c "from ghost.core.daemon import status_ghostd; print(status_ghostd())"

# Run tests
python3 -m pytest ghost/tests/ -v
```

## Success Criteria

The refactor is considered successful when:

- ✅ All files moved to new structure
- ✅ All imports resolve correctly
- ✅ CLI remains accessible (direct execution and symlinks)
- ✅ Daemon can start/stop successfully
- ✅ Core functionality tests pass
- ✅ Follow-up documentation generated

## Development Philosophy

This script embodies the principle of **surgical refactoring**:

- **Minimal viable changes** - Fix only what breaks functionality
- **Document technical debt** - Record quality issues for future attention
- **Preserve stability** - Prioritize working system over perfect code
- **Clear success criteria** - Binary pass/fail validation
- **Risk minimization** - Smaller change surface = fewer failure modes

The goal isn't perfect code - it's a **perfectly functional** new structure with a clear path forward for quality improvements.

## Troubleshooting

### Script Fails Mid-Execution

- Script automatically attempts rollback to previous commit
- Check error messages for specific failure point
- Ensure working directory is clean before retry

### Import Errors After Refactor

- Verify all `__init__.py` files exist in package directories
- Check that import rewrite completed successfully
- Review `REFACTOR_FOLLOWUP.md` for known issues

### CLI/Daemon Issues

- Verify symlinks updated correctly: `ls -la ~/.local/bin/ghost`
- Test daemon paths: `python3 -c "from ghost.core.daemon import status_ghostd"`
- Check process management: `ps aux | grep ghost`

### Technical Debt Concerns

- Review `REFACTOR_FOLLOWUP.md` for documented cleanup opportunities
- Bootstrap issues are functional but not optimal - safe to address in follow-up PRs
- Focus on functionality first, code quality second

## Contributing

When extending this script:

1. **Maintain surgical focus** - Only add fixes for breaking changes
2. **Document quality issues** - Add to follow-up recommendations instead of auto-fixing
3. **Test rollback scenarios** - Ensure failures don't leave partial state
4. **Validate success criteria** - Every addition should have clear pass/fail tests

Remember: This script's job is to **migrate safely**, not to **fix everything**. Quality improvements belong in dedicated cleanup PRs after the structure migration is proven stable.
