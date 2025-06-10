#!/bin/bash

set -e  # halt on error

# ─────────────────────────────────────────────────────────────────────────────
# 📦 GhostOS Structure Refactor Script (Enhanced - Debug Fixed)
# Moves system/ into ghost/ submodules, updates layout, prepares runtime state
# ─────────────────────────────────────────────────────────────────────────────

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

skipped=()
errors=()

log_info() { echo -e "${BLUE}→${NC} $1"; }
log_success() { echo -e "${GREEN}✅${NC} $1"; }
log_warning() { echo -e "${YELLOW}⚠️${NC} $1"; }
log_error() { echo -e "${RED}❌${NC} $1"; }

# Rollback function
rollback() {
    log_error "Script failed. Attempting rollback..."
    if [ -f ".refactor_backup_commit" ]; then
        git reset --hard "$(cat .refactor_backup_commit)"
        rm -f .refactor_backup_commit
        log_info "Rolled back to previous commit"
    fi
    exit 1
}

trap rollback ERR

echo -e "\n📦 ${BLUE}GhostOS Structure Refactor${NC} initiated..."

# Step 0: Pre-flight checks
log_info "Running pre-flight checks..."

if [ -d "ghost" ]; then
  log_error "'ghost/' directory already exists. Aborting to prevent overwrite."
  exit 1
fi

if [ ! -d ".git" ]; then
  log_error "Not inside a Git repository. Aborting."
  exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
  log_error "Uncommitted changes detected. Please commit or stash changes first."
  exit 1
fi

# Create backup commit reference
git rev-parse HEAD > .refactor_backup_commit
log_success "Created backup reference"

# Validate required files exist
required_files=(
  "system/ghost.py"
  "system/ghostd.py" 
  "system/ghost_cli.py"
  "system/ghost_daemon.py"
  "system/ghost_config.py"
  "system/ghost_queue.py"
  "system/ghost_runtime.py"
  "system/ghost_state.py"
  "system/ghost_modules.py"
  "system/ghost_utils.py"
  "system/ghost_registry.py"
)

for file in "${required_files[@]}"; do
  if [ ! -f "$file" ]; then
    log_error "Required file missing: $file"
    exit 1
  fi
done

log_success "Pre-flight checks passed"

# Step 1: Create new ghost/ substructure
log_info "Creating directory scaffold..."
mkdir -p ghost/{cli,core,state/cache,utils,tests,docs,module}

# Add __init__.py to all directories to make them Python packages
log_info "Creating __init__.py files in all ghost/* directories..."
find ghost -type d -exec touch {}/__init__.py \;

# Step 2: Move CLI files
log_info "Moving CLI files..."
git mv system/ghost.py ghost/cli/ghost.py
git mv system/ghost_cli.py ghost/cli/cli.py
git mv system/ghost_bootstrap.py ghost/cli/bootstrap.py
git mv system/ghost_install.py ghost/cli/install.py
git mv system/ghost_init.py ghost/cli/init.py

# Step 3: Move daemon (keep at root level for process management)
log_info "Moving daemon files..."
git mv system/ghostd.py ghost/ghostd.py
git mv system/ghost_daemon.py ghost/core/daemon.py

# Step 4: Move core logic
log_info "Moving core files..."
git mv system/ghost_config.py ghost/core/config.py
git mv system/ghost_queue.py ghost/core/queue.py
git mv system/ghost_registry.py ghost/core/registry.py
git mv system/ghost_runtime.py ghost/core/runtime.py
git mv system/ghost_state.py ghost/core/state.py

# Step 5: Move module system
log_info "Moving module definitions..."
git mv system/ghost_modules.py ghost/module/modules.py

# Step 6: Move utilities
log_info "Moving utils..."
git mv system/ghost_utils.py ghost/utils/ghost_utils.py

# Step 7: Move tests
log_info "Moving test files..."
git mv system/test_ghost.py ghost/tests/test_ghost.py

# Step 8: Move documentation
log_info "Moving internal docs..."
# Move all markdown files from _docs to ghost/docs
if [ -d "system/_docs" ]; then
    for doc_file in system/_docs/*.md; do
        if [ -f "$doc_file" ]; then
            filename=$(basename "$doc_file")
            git mv "$doc_file" "ghost/docs/$filename"
            log_success "Moved $filename to ghost/docs/"
        fi
    done
else
    log_warning "system/_docs directory not found"
    skipped+=("documentation files")
fi

# Step 9: Move .ghostproject config
log_info "Moving .ghostproject config..."
if [ -f system/_docs/.ghostproject ]; then
  mv system/_docs/.ghostproject .ghostproject
  log_success "Moved .ghostproject to root"
else
  log_warning ".ghostproject not found in system/_docs/. Skipping move."
  skipped+=(".ghostproject")
fi

# Step 10: Move queue file and clean up cache files
log_info "Moving queue file to new location..."
git mv system/ghost-queue.md ghost/state/queue.md

log_info "Cleaning up cache files..."
rm -rf system/__pycache__
rm -f system/*.pyc

# Step 11: Handle remaining directories
if [ -d system/_docs ]; then
  if rmdir system/_docs 2>/dev/null; then
    log_success "Removed empty _docs directory"
  else
    log_warning "_docs/ not empty, listing contents:"
    ls -la system/_docs/
    skipped+=("_docs directory")
  fi
fi

# Step 12: Remove old system dir
if [ -d system ]; then
  if rmdir system 2>/dev/null; then
    log_success "Removed empty system directory"
  else
    log_warning "system/ not empty, listing remaining contents:"
    ls -la system/
    skipped+=("system directory")
  fi
fi

# Step 13: Create runtime state files
log_info "Setting up ghost/state/ runtime data..."
echo '[]' > ghost/state/queue.json
: > ghost/state/daemon.pid
echo "This directory holds volatile cache state." > ghost/state/cache/README.md

# Step 14: Update config paths to reflect new structure
log_info "Creating updated configuration..."
cat > ghost/core/config.py << 'EOF'
from pathlib import Path

# Root directories
VAULT = Path.home() / "ghostvault"

# Ghost structure paths  
GHOST_ROOT = VAULT / "ghost"
CLI_DIR = GHOST_ROOT / "cli"
CORE_DIR = GHOST_ROOT / "core"
MODULE_DIR = GHOST_ROOT / "module"
UTILS_DIR = GHOST_ROOT / "utils"
TESTS_DIR = GHOST_ROOT / "tests"
DOCS_DIR = GHOST_ROOT / "docs"
STATE_DIR = GHOST_ROOT / "state"
CACHE_DIR = STATE_DIR / "cache"

# Runtime directories (backward compatibility)
RITUALS = ["rituals", "memory", "queue", "logs"]

# Runtime files
QUEUE_JSON = STATE_DIR / "queue.json"
QUEUE_MD = STATE_DIR / "queue.md"
DAEMON_PID = STATE_DIR / "daemon.pid"

# Legacy compatibility (for transition period)
SYSTEM = GHOST_ROOT  # Map SYSTEM to GHOST_ROOT for backward compatibility
EOF

# Step 15: Create enhanced import rewrite script
log_info "Creating import rewrite script..."
mkdir -p scripts
cat > scripts/update_imports.py << 'EOF'
#!/usr/bin/env python3
import os
import re
import sys

# Mapping of old module names to new paths
REWRITE_MAP = {
    'from ghost_config': 'from ghost.core.config',
    'import ghost_config': 'import ghost.core.config as ghost_config',
    'from ghost_queue': 'from ghost.core.queue',
    'import ghost_queue': 'import ghost.core.queue as ghost_queue',
    'from ghost_registry': 'from ghost.core.registry',
    'import ghost_registry': 'import ghost.core.registry as ghost_registry',
    'from ghost_runtime': 'from ghost.core.runtime',
    'import ghost_runtime': 'import ghost.core.runtime as ghost_runtime',
    'from ghost_state': 'from ghost.core.state',
    'import ghost_state': 'import ghost.core.state as ghost_state',
    'from ghost_utils': 'from ghost.utils.ghost_utils',
    'import ghost_utils': 'import ghost.utils.ghost_utils as ghost_utils',
    'from ghost_bootstrap': 'from ghost.cli.bootstrap',
    'import ghost_bootstrap': 'import ghost.cli.bootstrap as ghost_bootstrap',
    'from ghost_install': 'from ghost.cli.install',
    'import ghost_install': 'import ghost.cli.install as ghost_install',
    'from ghost_init': 'from ghost.cli.init',
    'import ghost_init': 'import ghost.cli.init as ghost_init',
    'from ghost_modules': 'from ghost.module.modules',
    'import ghost_modules': 'import ghost.module.modules as ghost_modules',
    'from ghost_cli': 'from ghost.cli.cli',
    'import ghost_cli': 'import ghost.cli.cli as ghost_cli',
    'from ghost_daemon': 'from ghost.core.daemon',
    'import ghost_daemon': 'import ghost.core.daemon as ghost_daemon',
}

def update_file_imports(filepath):
    """Update imports in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply import rewrites
        for old_import, new_import in REWRITE_MAP.items():
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(old_import) + r'\b'
            content = re.sub(pattern, new_import, content)
        
        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated imports in: {filepath}")
            return True
        return False
        
    except Exception as e:
        print(f"❌ Error updating {filepath}: {e}")
        return False

def main():
    """Update imports in all Python files"""
    updated_files = []
    failed_files = []
    
    for root, dirs, files in os.walk("."):
        # Skip certain directories
        if any(skip in root for skip in ['.git', '__pycache__', '.venv']):
            continue
            
        for filename in files:
            if filename.endswith('.py'):
                filepath = os.path.join(root, filename)
                if update_file_imports(filepath):
                    updated_files.append(filepath)
    
    print(f"\n📊 Import rewrite summary:")
    print(f"   Updated: {len(updated_files)} files")
    if updated_files:
        print("   Files changed:")
        for f in updated_files:
            print(f"     - {f}")
    
    return len(failed_files) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
EOF

chmod +x scripts/update_imports.py

# Step 16: Run import updates
log_info "Updating import statements..."
if python3 scripts/update_imports.py; then
    log_success "Import statements updated successfully"
else
    log_error "Import update failed"
    exit 1
fi

# Step 17: Update file references to use new constants
log_info "Updating file references to use new constants..."

# Update ghost_state.py to use QUEUE_MD
if [ -f "ghost/core/state.py" ]; then
    # Update import line and queue references
    sed -i.bak 's|from ghost_config import VAULT, SYSTEM|from ghost.core.config import VAULT, QUEUE_MD|g' ghost/core/state.py
    sed -i.bak 's|SYSTEM / "ghost-queue.md"|QUEUE_MD|g' ghost/core/state.py
    sed -i.bak 's|queue_path = SYSTEM / "ghost-queue.md"|queue_path = QUEUE_MD|g' ghost/core/state.py
    log_success "Updated ghost/core/state.py to use QUEUE_MD"
fi

# Update ghost_runtime.py to use QUEUE_MD
if [ -f "ghost/core/runtime.py" ]; then
    sed -i.bak 's|from ghost_config import VAULT, SYSTEM|from ghost.core.config import VAULT, QUEUE_MD|g' ghost/core/runtime.py
    sed -i.bak 's|SYSTEM / "ghost-queue.md"|QUEUE_MD|g' ghost/core/runtime.py
    sed -i.bak 's|path = SYSTEM / "ghost-queue.md"|path = QUEUE_MD|g' ghost/core/runtime.py
    log_success "Updated ghost/core/runtime.py to use QUEUE_MD"
fi

# Step 18: Critical fixes for daemon and CLI functionality (best-effort)
log_info "Applying daemon functionality fixes (best-effort)..."

# Fix ghostd.py imports
if [ -f "ghost/ghostd.py" ]; then
    sed -i.bak 's|from ghost_queue|from ghost.core.queue|g' ghost/ghostd.py
    sed -i.bak 's|from ghost_runtime|from ghost.core.runtime|g' ghost/ghostd.py
    sed -i.bak 's|import ghost_queue|import ghost.core.queue as ghost_queue|g' ghost/ghostd.py
    sed -i.bak 's|import ghost_runtime|import ghost.core.runtime as ghost_runtime|g' ghost/ghostd.py
    log_success "Fixed ghostd.py imports"
else
    log_warning "ghostd.py not found in expected location - daemon fixes skipped"
    skipped+=("ghostd.py import fixes")
fi

# Fix daemon process management paths
if [ -f "ghost/core/daemon.py" ]; then
    # Update ghostd path references to new location
    sed -i.bak 's|SYSTEM / "ghostd.py"|VAULT / "ghost" / "ghostd.py"|g' ghost/core/daemon.py
    sed -i.bak 's|str(SYSTEM / "ghostd.py")|str(VAULT / "ghost" / "ghostd.py")|g' ghost/core/daemon.py
    
    # Fix PID file handling to use absolute paths
    sed -i.bak 's|"ghostd.pid"|STATE_DIR / "daemon.pid"|g' ghost/core/daemon.py
    sed -i.bak 's|os.path.exists("ghostd.pid")|os.path.exists(str(STATE_DIR / "daemon.pid"))|g' ghost/core/daemon.py
    sed -i.bak 's|open("ghostd.pid"|open(str(STATE_DIR / "daemon.pid")|g' ghost/core/daemon.py
    sed -i.bak 's|os.remove("ghostd.pid")|os.remove(str(STATE_DIR / "daemon.pid"))|g' ghost/core/daemon.py
    
    # Add imports if not present
    if ! grep -q "STATE_DIR" ghost/core/daemon.py; then
        sed -i.bak '1i\
from ghost.core.config import VAULT, STATE_DIR' ghost/core/daemon.py
    fi
    
    log_success "Fixed daemon management paths and PID handling"
else
    log_warning "ghost/core/daemon.py not found - daemon management fixes skipped"
    skipped+=("daemon management path fixes")
fi

# Fix ghostd.py PID file references too
if [ -f "ghost/ghostd.py" ]; then
    # Add STATE_DIR import if not present
    if ! grep -q "STATE_DIR" ghost/ghostd.py; then
        sed -i.bak '1i\
from ghost.core.config import STATE_DIR' ghost/ghostd.py
    fi
    log_success "Fixed ghostd.py configuration imports"
fi

# Update CLI symlink target if it exists
log_info "Checking CLI symlink..."
local_bin="$HOME/.local/bin"
if [ -L "$local_bin/ghost" ]; then
    old_target=$(readlink "$local_bin/ghost")
    rm "$local_bin/ghost"
    ln -s "$(pwd)/ghost.py" "$local_bin/ghost"
    log_success "Updated CLI symlink target (was: $old_target)"
elif [ -f "$local_bin/ghost" ]; then
    log_warning "Non-symlink ghost file exists at $local_bin/ghost - manual review needed"
    skipped+=("CLI symlink update - file conflict")
else
    log_info "No existing CLI symlink found"
    # Create symlink if ~/.local/bin exists or can be created
    if [ -d "$local_bin" ] || mkdir -p "$local_bin" 2>/dev/null; then
        ln -s "$(pwd)/ghost.py" "$local_bin/ghost"
        log_success "Created new CLI symlink at $local_bin/ghost"
        
        # Check if ~/.local/bin is in PATH
        if [[ ":$PATH:" != *":$local_bin:"* ]]; then
            log_warning "$local_bin is not in your PATH"
            log_info "Add this to your shell rc file: export PATH=\"\$HOME/.local/bin:\$PATH\""
        fi
    else
        log_warning "Could not create $local_bin directory"
        skipped+=("CLI symlink creation - directory creation failed")
    fi
fi

# Step 19: Create new root CLI entry point
log_info "Creating new root CLI entry point..."
cat > ghost.py << 'EOF'
#!/usr/bin/env python3
"""
GhostOS CLI Entry Point
Delegates to ghost.cli.ghost for actual CLI functionality
"""

import sys
from pathlib import Path

# Add ghost package to path
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    from ghost.cli.cli import main
    main()
EOF
chmod +x ghost.py
log_success "Created new root CLI entry point"

# Step 20: Enhanced validation checks with detailed logging
log_info "Running enhanced validation checks..."

# Test core config import first (this was the main failure point)
log_info "Testing core configuration import..."
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    print('  → Attempting to import ghost.core.config...')
    from ghost.core.config import VAULT
    print(f'  ✅ VAULT imported successfully: {VAULT}')
    
    print('  → Testing GHOST_ROOT import...')
    from ghost.core.config import GHOST_ROOT
    print(f'  ✅ GHOST_ROOT imported successfully: {GHOST_ROOT}')
    
    print('  → Testing STATE_DIR import...')
    from ghost.core.config import STATE_DIR
    print(f'  ✅ STATE_DIR imported successfully: {STATE_DIR}')
    
    print('  → Testing QUEUE_MD import...')
    from ghost.core.config import QUEUE_MD
    print(f'  ✅ QUEUE_MD imported successfully: {QUEUE_MD}')
    
    print('✅ Core configuration imports successful')
except Exception as e:
    print(f'❌ Core config import failed: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
" || {
    log_error "Core configuration import validation failed"
    log_info "This indicates a fundamental issue with the config setup"
    exit 1
}

# Test that queue module can be imported
log_info "Testing queue module import..."
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    print('  → Attempting to import ghost.core.queue...')
    from ghost.core.queue import load_queue
    print('  ✅ Queue module imported successfully')
except Exception as e:
    print(f'❌ Queue module import failed: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
" || {
    log_warning "Queue module import failed - functionality may be limited"
    skipped+=("queue module validation")
}

# Test that runtime module can be imported
log_info "Testing runtime module import..."
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    print('  → Attempting to import ghost.core.runtime...')
    from ghost.core.runtime import log_event
    print('  ✅ Runtime module imported successfully')
except Exception as e:
    print(f'❌ Runtime module import failed: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
" || {
    log_warning "Runtime module import failed - functionality may be limited"
    skipped+=("runtime module validation")
}

# Test CLI functionality
log_info "Testing CLI import..."
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    print('  → Attempting to import ghost.cli.cli...')
    from ghost.cli.cli import main
    print('  ✅ CLI import successful')
except Exception as e:
    print(f'❌ CLI validation failed: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
" || {
    log_warning "CLI validation failed - CLI may not work properly"
    skipped+=("CLI functionality validation")
}

log_success "Enhanced validation completed"

# Step 21: Run tests if they exist
if [ -f "ghost/tests/test_ghost.py" ]; then
    log_info "Running tests..."
    # Check if pytest is available before trying to use it
    if python3 -c "import pytest" 2>/dev/null; then
        if python3 -m pytest ghost/tests/ -v; then
            log_success "All tests passed"
        else
            log_warning "Some tests failed - manual review needed"
            skipped+=("test suite validation")
        fi
    else
        log_warning "pytest not available - skipping test execution"
        log_info "Install pytest with: pip install pytest"
        skipped+=("test suite execution - pytest not installed")
    fi
else
    log_info "No test files found - skipping test execution"
fi

# Cleanup backup files
rm -f ghost/**/*.bak
rm -f .refactor_backup_commit

# Summary of skipped/failed actions
if [ ${#skipped[@]} -gt 0 ]; then
  log_warning "Skipped or incomplete items:"
  for item in "${skipped[@]}"; do
    echo "   - $item"
  done
else
  log_success "All refactoring steps completed successfully"
fi

echo -e "\n${GREEN}✅ Restructure complete!${NC} Here are some useful commands:"
echo "   git diff --name-status        # See renamed/moved files"
echo "   git diff --stat --summary     # Rename + line change summary"
echo "   git status --short            # Quick file overview"
echo ""
echo "🧪 Test the new structure:"
echo "   python3 -c 'from ghost.core.config import VAULT; print(f\"Vault: {VAULT}\")'"
echo "   python3 ghost.py --help"
echo ""

# Step 22: Check and activate virtual environment
log_info "Checking virtual environment status..."
if [ -n "$VIRTUAL_ENV" ]; then
    log_success "Virtual environment is already active: $VIRTUAL_ENV"
elif [ -d ".venv" ]; then
    log_info "Virtual environment found but not active - activating..."
    echo "→ Running: source .venv/bin/activate"
    source .venv/bin/activate
    if [ -n "$VIRTUAL_ENV" ]; then
        log_success "Virtual environment activated: $VIRTUAL_ENV"
    else
        log_warning "Failed to activate virtual environment"
        skipped+=("virtual environment activation")
    fi
else
    log_warning "No virtual environment found (.venv directory missing)"
    log_info "Create one with: python3 -m venv .venv && source .venv/bin/activate"
    skipped+=("virtual environment activation - .venv not found")
fi

# Step 23: Test ghost commands if venv is active
if [ -n "$VIRTUAL_ENV" ]; then
    log_info "Testing ghost commands with active virtual environment..."
    
    # Test ghost status
    echo "→ Running: ghost status"
    if ghost status 2>/dev/null; then
        log_success "ghost status command working"
        
        # Log ritual completion
        echo "→ Running: ghost ritual \"✨restructure complete\""
        if ghost ritual "✨restructure complete" 2>/dev/null; then
            log_success "Logged restructure completion ritual"
        else
            log_warning "ghost ritual command failed - trying direct invocation"
            echo "→ Running: python3 ghost.py ritual \"✨restructure complete\""
            if python3 ghost.py ritual "✨restructure complete"; then
                log_success "Logged restructure completion ritual (direct invocation)"
            else
                log_warning "Could not log completion ritual"
                skipped+=("ritual logging")
            fi
        fi
    else
        log_warning "ghost status command failed - trying direct invocation"
        echo "→ Running: python3 ghost.py status"
        if python3 ghost.py status; then
            log_success "Direct ghost.py status working"
            echo "→ Running: python3 ghost.py ritual \"✨restructure complete\""
            if python3 ghost.py ritual "✨restructure complete"; then
                log_success "Logged restructure completion ritual (direct invocation)"
            else
                log_warning "Could not log completion ritual"
                skipped+=("ritual logging")
            fi
        else
            log_warning "Both ghost and python3 ghost.py commands failed"
            skipped+=("ghost command testing")
        fi
    fi
else
    log_warning "Virtual environment not active - skipping ghost command tests"
    skipped+=("ghost command testing - no active venv")
fi

echo ""
echo "💡 If 'ghost' command doesn't work:"
echo "   • Ensure ~/.local/bin is in your PATH"
echo "   • Test symlink: ~/.local/bin/ghost --help"
echo "   • Use direct: python3 ghost.py [command]"
echo "   • Activate venv: source .venv/bin/activate"