# Ghost Structure Refactor Script

A resilient bash script for restructuring the GhostOS project from a flat `system/` directory to a modular `ghost/` package structure with comprehensive error handling and best-effort optimization fixes.

## Overview

This script performs a **resilient refactoring** of the GhostOS codebase, moving from:

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

## Philosophy: Resilient Migration with Best-Effort Optimization

This script follows a **"complete the mission, optimize what we can"** approach:

- ✅ **Guarantee file structure migration** - Core mission always succeeds
- 🔧 **Best-effort functionality fixes** - Apply optimizations where possible
- 📋 **Document what's skipped** - Clear follow-up guidance for manual fixes
- 🛡️ **Never abort on optimization failures** - Structure migration takes priority

## Features

### 🛡️ **Guaranteed Success & Rollback Safety**

- **Mission-critical guarantee** - File structure migration always completes
- **Automatic rollback** - Only triggers on infrastructure failures (git issues, file corruption)
- **Graceful degradation** - Individual fix failures don't abort the entire process
- **Pre-flight validation** - Comprehensive checks before any modifications

### 🔧 **Comprehensive Functionality Preservation**

- **Daemon process management** - Updates process paths, PID handling, and executable references
- **CLI symlink management** - Detects and updates existing symlinks with conflict resolution
- **Import chain integrity** - Ensures all module imports resolve correctly after restructuring
- **Configuration consolidation** - Centralizes hardcoded paths and adds new constants

### 📦 **Modern Package Structure**

- **Proper Python packaging** - Creates correct `__init__.py` files and package hierarchy
- **Path consolidation** - Centralizes all path references in configuration
- **Queue file management** - Preserves both programmatic (JSON) and human-readable (MD) queues
- **Runtime state organization** - Clean separation of code and runtime data

### 📋 **Intelligent Error Handling**

- **Graceful skip tracking** - Records what couldn't be fixed for follow-up
- **Non-fatal validation** - Tests functionality without blocking completion
- **Detailed reporting** - Clear distinction between success, warnings, and skipped items
- **Manual intervention guidance** - Specific next steps when automated fixes fail

## Prerequisites

- **Git repository** with clean working directory (no uncommitted changes)
- **Python 3.10+**
- **Required source files** present in `system/` directory
- **Virtual environment** (recommended but not required)

## Usage

```bash
# Make executable
chmod +x ghost_structure_refactor.sh

# Run the refactor
./ghost_structure_refactor.sh
```

## What It Does

### Phase 1: Infrastructure Validation

1. **Pre-flight checks** - Git status, file existence, working directory validation
2. **Backup creation** - Records current commit for rollback capability
3. **Environment validation** - Checks Python version and repository state

### Phase 2: Configuration Preparation

4. **Path consolidation setup** - Updates config files with new structure paths
5. **Import preparation** - Fixes hardcoded paths before file moves

### Phase 3: Structure Creation

6. **Directory scaffold** - Creates new `ghost/` package structure
7. **Package initialization** - Adds `__init__.py` files for Python packages

### Phase 4: File Migration (Guaranteed)

8. **CLI files** → `ghost/cli/`
9. **Core logic** → `ghost/core/`
10. **Daemon files** → `ghost/core/daemon.py` + `ghost/ghostd.py`
11. **Module system** → `ghost/module/`
12. **Utilities** → `ghost/utils/`
13. **Tests** → `ghost/tests/`
14. **Documentation** → `ghost/docs/`
15. **Queue file** → `ghost/state/queue.md`

### Phase 5: Optimization Fixes (Best-Effort)

16. **Queue path updates** - Adds QUEUE_MD constant and updates references
17. **Import chain fixes** - Updates all import statements to new structure
18. **Daemon functionality** - Fixes process management paths and PID handling
19. **CLI preservation** - Updates symlinks and creates new entry point

### Phase 6: Validation & Documentation

20. **Functional testing** - Validates core functionality (non-fatal)
21. **Follow-up documentation** - Creates comprehensive cleanup recommendations

## File Mapping

| Original Location          | New Location                 | Purpose             |
| -------------------------- | ---------------------------- | ------------------- |
| `system/ghost.py`          | `ghost/cli/ghost.py`         | CLI logic           |
| `system/ghostd.py`         | `ghost/ghostd.py`            | Daemon (root level) |
| `system/ghost_cli.py`      | `ghost/cli/cli.py`           | CLI handlers        |
| `system/ghost_daemon.py`   | `ghost/core/daemon.py`       | Process management  |
| `system/ghost_config.py`   | `ghost/core/config.py`       | Configuration       |
| `system/ghost_queue.py`    | `ghost/core/queue.py`        | Queue management    |
| `system/ghost_runtime.py`  | `ghost/core/runtime.py`      | Runtime functions   |
| `system/ghost_state.py`    | `ghost/core/state.py`        | State management    |
| `system/ghost_modules.py`  | `ghost/module/modules.py`    | Module system       |
| `system/ghost_utils.py`    | `ghost/utils/ghost_utils.py` | Utilities           |
| `system/ghost_registry.py` | `ghost/core/registry.py`     | Module registry     |
| `system/test_ghost.py`     | `ghost/tests/test_ghost.py`  | Tests               |
| `system/_docs/*.md`        | `ghost/docs/*.md`            | Documentation       |
| `system/ghost-queue.md`    | `ghost/state/queue.md`       | Task queue          |
| **NEW:** `ghost.py`        | `ghost.py` (root)            | CLI entry point     |

## Configuration Updates

The script creates a centralized configuration in `ghost/core/config.py`:

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

## Optimization Fixes Applied

### 🔧 **Daemon Process Management**

- **Process path updates** - Fixes daemon executable references for new location
- **PID file consolidation** - Converts relative paths to absolute STATE_DIR paths
- **Import fixes** - Ensures daemon modules can find dependencies
- **Cross-file consistency** - Updates both process management and daemon files

### 🔗 **CLI Symlink Management**

- **Existing symlink detection** - Finds CLI symlinks in `~/.local/bin/ghost`
- **Target updates** - Points symlinks to new root CLI entry point
- **Conflict resolution** - Handles cases where symlink location has non-symlink files
- **Creation preparation** - Sets up for future symlink creation by install process

### 📦 **Import Chain Integrity**

- **Comprehensive pattern matching** - Catches various import statement formats
- **Package structure compliance** - Ensures imports use new package hierarchy
- **Cross-module dependencies** - Validates that modules can import each other
- **Root CLI delegation** - Creates simple entry point that delegates to package

### 🗂️ **Path Reference Cleanup**

- **Hardcoded path elimination** - Removes system/ references from moved files
- **Configuration constant usage** - Updates files to use centralized path constants
- **State file organization** - Ensures consistent state directory usage

## What's NOT Fixed (By Design)

The following issues are **documented but not automatically fixed** to maintain script reliability:

### 📋 **Bootstrap Code Technical Debt**

- **PYTHONPATH manipulation** - Obsolete with proper package structure but not removed
- **Shell RC modifications** - Environment pollution that should be cleaned up
- **File consolidation** - Multiple bootstrap files with overlapping functionality
- **Virtual environment handling** - Some complexity could be simplified

### 🔧 **Code Quality Improvements**

- **Dead code removal** - Functions that no longer serve a purpose
- **Import optimization** - Some imports could be more specific
- **Error handling enhancement** - Some modules could have better error handling
- **Documentation updates** - Some docstrings reference old structure

### 📝 **Follow-up Requirements**

See `REFACTOR_FOLLOWUP.md` after completion for:

- **Phase 2 preparation** - Specific requirements for introspection suite
- **Code cleanup opportunities** - Non-critical quality improvements
- **Testing recommendations** - Additional validation suggestions
- **Architecture optimizations** - Long-term structural improvements

## Error Handling Approach

### 🟢 **Never Aborts On (Graceful Handling):**

- Missing daemon files
- Symlink conflicts
- Validation test failures
- Individual path fix failures
- Import rewrite edge cases

### 🔴 **Aborts Only On (Critical Infrastructure):**

- Git repository corruption
- Uncommitted changes detected
- Core system files missing
- Backup creation failure
- Directory creation failure

### 📊 **Reporting Categories:**

- **✅ Success** - Operation completed successfully
- **⚠️ Warning** - Operation had issues but script continues
- **📋 Skipped** - Operation couldn't be completed, recorded for follow-up
- **❌ Error** - Critical failure requiring script abort

## Post-Refactor Verification

After successful completion:

```bash
# Check file structure
tree ghost/
git status --short

# Test imports
python3 -c "
from ghost.core.config import VAULT, QUEUE_MD, STATE_DIR
from ghost.core.queue import load_queue
from ghost.core.runtime import log_event
print('✅ All imports working')
"

# Test CLI
python3 ghost.py --help
./ghost.py status

# Test daemon (if files were found and fixed)
python3 -c "
from ghost.core.daemon import status_ghostd
print('Daemon status:', status_ghostd())
"

# Run tests
python3 -m pytest ghost/tests/ -v
```

## Success Criteria

The refactor is considered **successful** when:

### ✅ **Guaranteed (Always Achieved):**

- All files moved to new structure
- Git history preserved through git mv
- Package structure created with **init**.py files
- Basic import chains work
- Follow-up documentation generated

### 🎯 **Optimized (Best-Effort):**

- All imports resolve correctly
- CLI remains accessible (direct execution and symlinks)
- Daemon can start/stop successfully
- Configuration paths are centralized
- No hardcoded system/ references remain

### 📋 **Documented (If Not Achieved):**

- Skipped operations recorded in output
- Manual intervention steps provided
- Follow-up recommendations generated
- Specific failure reasons logged

## Development Philosophy

This script embodies **resilient refactoring principles**:

### 🎯 **Mission-Critical Reliability**

- **Core mission always succeeds** - File structure migration is guaranteed
- **Optimization is best-effort** - Feature fixes don't block structural changes
- **Clear success criteria** - Distinction between required and optional outcomes

### 🔧 **Intelligent Error Handling**

- **Graceful degradation** - Individual failures don't cascade
- **Comprehensive documentation** - Everything that can't be fixed is recorded
- **User empowerment** - Clear guidance for manual intervention

### 📋 **Maintainable Architecture**

- **Single responsibility** - Structure migration with optimization hooks
- **Extensible design** - Easy to add new optimization fixes
- **Clear boundaries** - Separation between guaranteed and best-effort operations

## Troubleshooting

### Script Completes but Some Features Don't Work

This is expected behavior. Check the script output for:

- **⚠️ Warnings** - Issues that were handled gracefully
- **📋 Skipped operations** - Features that need manual attention
- **Follow-up recommendations** - Specific next steps in `REFACTOR_FOLLOWUP.md`

### Import Errors After Refactor

1. **Verify package structure**: `find ghost -name "__init__.py"`
2. **Check import rewrite logs**: Look for import update success messages
3. **Test specific imports**: Use Python shell to test problematic imports
4. **Review skipped items**: Check if import fixes were skipped

### CLI/Daemon Issues

1. **Check symlink status**: `ls -la ~/.local/bin/ghost`
2. **Verify daemon files**: `ls -la ghost/ghostd.py ghost/core/daemon.py`
3. **Test daemon imports**: `python3 -c "from ghost.core.daemon import status_ghostd"`
4. **Review daemon fix logs**: Look for daemon-related warnings in script output

### Partial Success Scenarios

The script is designed to handle partial success gracefully:

- **Structure migration successful** + **Some optimizations skipped** = Normal outcome
- **All operations successful** = Ideal outcome
- **Structure migration failed** = Script should have aborted (check git status)

### When to Run Again

- **Never run on the same repository** - The script is designed for one-time execution
- **Create new branch** if you need to retry after manual fixes
- **Use git reset** to restore pre-refactor state if needed

## Contributing

When extending this script:

1. **Preserve mission-critical guarantee** - File migration must always succeed
2. **Add optimizations as best-effort** - Use warning patterns, not exit patterns
3. **Enhance skip tracking** - Document what can't be fixed automatically
4. **Test partial failure scenarios** - Ensure graceful degradation works
5. **Update follow-up documentation** - Keep cleanup recommendations current

### Design Patterns to Follow:

```bash
# ✅ Good: Graceful degradation
if [ -f "target_file" ]; then
    # Apply fix
    log_success "Fixed target_file"
else
    log_warning "target_file not found - manual fix needed"
    skipped+=("target_file optimization")
fi

# ❌ Bad: Mission abortion
if [ -f "target_file" ]; then
    # Apply fix
else
    log_error "target_file missing"
    exit 1  # Don't do this for optimization fixes!
fi
```

Remember: This script's job is to **migrate the structure reliably** and **optimize what it can**. The combination of guaranteed success with best-effort enhancement creates a robust foundation for the GhostOS evolution.
