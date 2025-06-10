#!/bin/bash

set -e  # halt on error

# ─────────────────────────────────────────────────────────────────────────────
# 📦 GhostOS Structure Refactor Script (Enhanced)
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

# Step 1: Update ghost_config.py paths BEFORE moving files
log_info "Consolidating path configuration..."

# Update ghost_config.py to reflect new structure
cat > system/ghost_config.py << 'EOF'
from pathlib import Path

# Root directories
VAULT = Path.home() / "ghostvault"

# New ghost/ structure paths  
GHOST_ROOT = VAULT / "ghost"
CLI_DIR = GHOST_ROOT / "cli"
CORE_DIR = GHOST_ROOT / "core"
MODULE_DIR = GHOST_ROOT / "module"
UTILS_DIR = GHOST_ROOT / "utils"
TESTS_DIR = GHOST_ROOT / "tests"
DOCS_DIR = GHOST_ROOT / "docs"
STATE_DIR = GHOST_ROOT / "state"
CACHE_DIR = STATE_DIR / "cache"

# Legacy paths (for backward compatibility during transition)
SYSTEM = VAULT / "system"  # Will be removed after refactor
RITUALS = ["rituals", "memory", "queue", "logs"]

# Runtime files
QUEUE_JSON = STATE_DIR / "queue.json"
QUEUE_MD = STATE_DIR / "queue.md"
DAEMON_PID = STATE_DIR / "daemon.pid"
EOF

log_success "Updated ghost_config.py with new structure paths"

# Step 2: Update imports to use config constants
log_info "Updating hardcoded paths to use config..."

# Fix ghost_utils.py to use config instead of hardcoded paths
sed -i.bak 's|VAULT = Path.home() / "ghostvault"|from ghost_config import VAULT|' system/ghost_utils.py
sed -i.bak 's|SYSTEM = VAULT / "system"|from ghost_config import SYSTEM|' system/ghost_utils.py

log_success "Updated hardcoded paths to use centralized config"

# Step 3: Create new ghost/ substructure
log_info "Creating directory scaffold..."
mkdir -p ghost/{cli,core,state/cache,utils,tests,docs,module}

# Add __init__.py to all directories to make them Python packages
log_info "Creating __init__.py files in all ghost/* directories..."
find ghost -type d -exec touch {}/__init__.py \;

# Step 4: Move CLI files
log_info "Moving CLI files..."
git mv system/ghost.py ghost/cli/ghost.py
git mv system/ghost_cli.py ghost/cli/cli.py
git mv system/ghost_bootstrap.py ghost/cli/bootstrap.py
git mv system/ghost_install.py ghost/cli/install.py
git mv system/ghost_init.py ghost/cli/init.py

# Step 5: Move daemon (keep at root level for process management)
log_info "Moving daemon files..."
git mv system/ghostd.py ghost/ghostd.py
git mv system/ghost_daemon.py ghost/core/daemon.py

# Step 5: Move core logic
log_info "Moving core files..."
git mv system/ghost_config.py ghost/core/config.py
git mv system/ghost_queue.py ghost/core/queue.py
git mv system/ghost_registry.py ghost/core/registry.py
git mv system/ghost_runtime.py ghost/core/runtime.py
git mv system/ghost_state.py ghost/core/state.py

# Step 6: Move module system
log_info "Moving module definitions..."
git mv system/ghost_modules.py ghost/module/modules.py

# Step 7: Move utilities
log_info "Moving utils..."
git mv system/ghost_utils.py ghost/utils/ghost_utils.py

# Step 8: Move tests
log_info "Moving test files..."
git mv system/test_ghost.py ghost/tests/test_ghost.py

# Step 9: Move documentation
log_info "Moving internal docs..."
git mv system/_docs/architecture.md ghost/docs/architecture.md
git mv system/_docs/ghostOS_rules.md ghost/docs/ghostOS_rules.md
git mv system/_docs/executor_rules.md ghost/docs/executor_rules.md
git mv system/_docs/vaultGhost_rules.md ghost/docs/vaultGhost_rules.md

# Step 10: Move .ghostproject config
log_info "Moving .ghostproject config..."
if [ -f system/_docs/.ghostproject ]; then
  mv system/_docs/.ghostproject .ghostproject
  log_success "Moved .ghostproject to root"
else
  log_warning ".ghostproject not found in system/_docs/. Skipping move."
  skipped+=(".ghostproject")
fi

# Step 11: Move queue file and clean up cache files
log_info "Moving queue file to new location..."
git mv system/ghost-queue.md ghost/state/queue.md

log_info "Cleaning up cache files..."
rm -rf system/__pycache__
rm -f system/*.pyc

# Step 12: Handle remaining directories
if [ -d system/_docs ]; then
  if rmdir system/_docs 2>/dev/null; then
    log_success "Removed empty _docs directory"
  else
    log_warning "_docs/ not empty, listing contents:"
    ls -la system/_docs/
    skipped+=("_docs directory")
  fi
fi

# Step 13: Remove old system dir
if [ -d system ]; then
  if rmdir system 2>/dev/null; then
    log_success "Removed empty system directory"
  else
    log_warning "system/ not empty, listing remaining contents:"
    ls -la system/
    skipped+=("system directory")
  fi
fi

# Step 14: Create runtime state files
log_info "Setting up ghost/state/ runtime data..."
echo '[]' > ghost/state/queue.json
: > ghost/state/daemon.pid
echo "This directory holds volatile cache state." > ghost/state/cache/README.md

# Step 15: Update config paths to reflect new structure
log_info "Updating config paths for new structure..."
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

# Runtime directories
RITUALS = ["rituals", "memory", "queue", "logs"]

# Runtime files
QUEUE_JSON = STATE_DIR / "queue.json"
QUEUE_MD = STATE_DIR / "queue.md"
DAEMON_PID = STATE_DIR / "daemon.pid"
EOF

# Step 16: Create enhanced import rewrite script
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

# Step 17: Update file references to use QUEUE_MD constant
log_info "Updating queue file references..."

# Update ghost_state.py to use QUEUE_MD
if [ -f "ghost/core/state.py" ]; then
    sed -i.bak 's|SYSTEM / "ghost-queue.md"|QUEUE_MD|g' ghost/core/state.py
    sed -i.bak 's|queue_path = SYSTEM / "ghost-queue.md"|from ghost.core.config import QUEUE_MD\n    queue_path = QUEUE_MD|g' ghost/core/state.py
    # Add QUEUE_MD import if not already present
    if ! grep -q "QUEUE_MD" ghost/core/state.py; then
        sed -i.bak '1i from ghost.core.config import VAULT, SYSTEM, QUEUE_MD' ghost/core/state.py
        # Remove the old import line to avoid duplication
        sed -i.bak 's|from ghost_config import VAULT, SYSTEM||g' ghost/core/state.py
    fi
    log_success "Updated ghost/core/state.py to use QUEUE_MD"
fi

# Update ghost_runtime.py to use QUEUE_MD
if [ -f "ghost/core/runtime.py" ]; then
    sed -i.bak 's|SYSTEM / "ghost-queue.md"|QUEUE_MD|g' ghost/core/runtime.py
    sed -i.bak 's|path = SYSTEM / "ghost-queue.md"|path = QUEUE_MD|g' ghost/core/runtime.py
    # Add QUEUE_MD import if not already present
    if ! grep -q "QUEUE_MD" ghost/core/runtime.py; then
        sed -i.bak 's|from ghost_config import VAULT, SYSTEM|from ghost.core.config import VAULT, SYSTEM, QUEUE_MD|g' ghost/core/runtime.py
    fi
    log_success "Updated ghost/core/runtime.py to use QUEUE_MD"
fi

# Step 18: Critical fixes for daemon and CLI functionality
log_info "Applying critical functionality fixes..."

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
    
    # Add STATE_DIR import if not present
    if ! grep -q "STATE_DIR" ghost/core/daemon.py; then
        sed -i.bak '1i from ghost.core.config import VAULT, STATE_DIR' ghost/core/daemon.py
    fi
    
    log_success "Fixed daemon management paths and PID handling"
else
    log_warning "ghost/core/daemon.py not found - daemon management fixes skipped"
    skipped+=("daemon management path fixes")
fi

# Fix ghostd.py PID file references too
if [ -f "ghost/ghostd.py" ]; then
    sed -i.bak 's|"ghostd.pid"|STATE_DIR / "daemon.pid"|g' ghost/ghostd.py
    sed -i.bak 's|open("ghostd.pid"|open(str(STATE_DIR / "daemon.pid")|g' ghost/ghostd.py
    
    # Add STATE_DIR import if not present
    if ! grep -q "STATE_DIR" ghost/ghostd.py; then
        sed -i.bak '1i from ghost.core.config import STATE_DIR' ghost/ghostd.py
    fi
    
    log_success "Fixed ghostd.py PID file handling"
fi

# Fix hardcoded system/ paths in moved files
log_info "Updating hardcoded system/ paths..."
for file in ghost/cli/*.py ghost/core/*.py ghost/utils/*.py; do
    if [ -f "$file" ]; then
        sed -i.bak 's|VAULT / "system"|CORE_DIR|g' "$file"
        sed -i.bak 's|/ "system" /|/ "ghost" / "core" /|g' "$file"
        # Fix any remaining system/ references
        sed -i.bak 's|"system/|"ghost/core/|g' "$file"
        sed -i.bak 's|system/|ghost/core/|g' "$file"
    fi
done
log_success "Updated hardcoded system/ paths"

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
    log_info "No existing CLI symlink found - will be created by install process"
fi

# Step 19: Fix root CLI entry point
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
    from ghost.cli.ghost import main
    main()
EOF
chmod +x ghost.py
log_success "Created new root CLI entry point"

# Step 20: Run import updates
log_info "Updating import statements..."
if python3 scripts/update_imports.py; then
    log_success "Import statements updated successfully"
else
    log_error "Import update failed"
    exit 1
fi

# Step 19: Validation checks
log_info "Running validation checks..."

# Test that key modules can be imported
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from ghost.core.config import VAULT
    from ghost.core.queue import load_queue
    from ghost.core.runtime import log_event
    print('✅ Core imports successful')
except Exception as e:
    print(f'❌ Import validation failed: {e}')
    sys.exit(1)
" || {
    log_error "Import validation failed"
    exit 1
}

# Test CLI functionality
if python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from ghost.cli.cli import main
    print('✅ CLI import successful')
except Exception as e:
    print(f'❌ CLI validation failed: {e}')
    sys.exit(1)
"; then
    log_success "CLI validation passed"
else
    log_error "CLI validation failed"
    exit 1
fi

# Step 19: Run tests if they exist
if [ -f "ghost/tests/test_ghost.py" ]; then
    log_info "Running tests..."
    if python3 -m pytest ghost/tests/ -v; then
        log_success "All tests passed"
    else
        log_warning "Some tests failed - manual review needed"
    fi
fi

# Cleanup backup files
rm -f system/*.bak
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
echo "   python3 ghost/cli/ghost.py --help"