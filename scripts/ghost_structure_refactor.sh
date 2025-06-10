#!/bin/bash

set -e  # halt on error

# ─────────────────────────────────────────────────────────────────────────────
# 📦 GhostOS Structure Refactor Script
# Moves system/ into ghost/ submodules, updates layout, prepares runtime state
# ─────────────────────────────────────────────────────────────────────────────

skipped=()

echo "\n📦 Restructure initiated..."

# Step 0: Safety Checks
if [ -d "ghost" ]; then
  echo "❌ 'ghost/' directory already exists. Aborting to prevent overwrite."
  exit 1
fi

if [ ! -d ".git" ]; then
  echo "❌ Not inside a Git repository. Aborting."
  exit 1
fi

# Step 1: Create new ghost/ substructure
echo "→ Creating directory scaffold..."
mkdir -p ghost/{cli,core,state/cache,utils,tests,docs,module}

# Add __init__.py to all directories to make them Python packages
echo "→ Creating __init__.py files in all ghost/* directories..."
find ghost -type d -exec touch {}/__init__.py \;

# Step 2: Move CLI files
echo "→ Moving CLI files..."
git mv system/ghost.py ghost/cli/ghost.py
git mv system/ghostd.py ghost/ghostd.py
git mv system/ghost_bootstrap.py ghost/cli/bootstrap.py
git mv system/ghost_install.py ghost/cli/install.py
git mv system/ghost_init.py ghost/cli/init.py

# Step 3: Move core logic
echo "→ Moving core files..."
git mv system/ghost_config.py ghost/core/config.py
git mv system/ghost_queue.py ghost/core/queue.py
git mv system/ghost_registry.py ghost/core/registry.py
git mv system/ghost_runtime.py ghost/core/runtime.py
git mv system/ghost_state.py ghost/core/state.py

# Step 4: Move module system
echo "→ Moving module definitions..."
git mv system/ghost_modules.py ghost/module/modules.py

# Step 5: Move utilities
echo "→ Moving utils..."
git mv system/ghost_utils.py ghost/utils/ghost_utils.py

# Step 6: Move tests
echo "→ Moving test files..."
git mv system/test_ghost.py ghost/tests/test_ghost.py

# Step 7: Move documentation
echo "→ Moving internal docs..."
git mv system/_docs/architecture.md ghost/docs/architecture.md
git mv system/_docs/ghostOS_rules.md ghost/docs/ghostOS_rules.md
git mv system/_docs/executor_rules.md ghost/docs/executor_rules.md
git mv system/_docs/vaultGhost_rules.md ghost/docs/vaultGhost_rules.md

# Step 8: Move .ghostproject config
echo "→ Moving .ghostproject config..."
if [ -f system/_docs/.ghostproject ]; then
  mv system/_docs/.ghostproject .ghostproject
else
  echo "⚠️  .ghostproject not found in system/_docs/. Skipping move."
  skipped+=(".ghostproject")
fi

# Step 8.5: Track _docs directory if not empty
if [ -d system/_docs ]; then
  if rmdir system/_docs 2>/dev/null; then
    echo "→ Removed empty _docs directory."
  else
    echo "⚠️  _docs/ not empty, skipped auto-delete."
    skipped+=("_docs directory")
  fi
fi

# Step 9: Remove legacy or redundant files
echo "→ Cleaning up obsolete files..."
rm -rf system/__pycache__
rm -f system/*.pyc
rm -f system/ghost-queue.md

# Step 10: Remove old system dir
if [ -d system ]; then
  echo "→ Removing old system directory..."
  rmdir system || {
    echo "⚠️  system/ not empty or failed to remove. Manual cleanup may be required."
    skipped+=("system directory")
  }
fi

# Step 11: Stub runtime state
echo "→ Stubbing ghost/state/ runtime data..."
echo '{}' > ghost/state/queue.json
: > ghost/state/daemon.pid
echo "This directory holds volatile cache state." > ghost/state/cache/README.md

# Step 12: Queue post-restructure doc update
echo "→ Queuing architecture.md rewrite task..."
echo 'ghost queue "rewrite architecture.md to reflect post-restructure file system and component boundaries"' >> ghost_queue.sh

# Step 13: Suggest import rewrite
mkdir -p scripts
echo "→ Suggesting import path rewrite..."
cat <<EOF > scripts/update_imports.py
#!/usr/bin/env python3
import os
import re

REWRITE_MAP = {
    'ghost_config': 'ghost.core.config',
    'ghost_queue': 'ghost.core.queue',
    'ghost_registry': 'ghost.core.registry',
    'ghost_runtime': 'ghost.core.runtime',
    'ghost_state': 'ghost.core.state',
    'ghost_utils': 'ghost.utils',
    'ghost_bootstrap': 'ghost.cli.bootstrap',
    'ghost_install': 'ghost.cli.install',
    'ghost_init': 'ghost.cli.init',
    'ghost_modules': 'ghost.module.modules',
}

for dirpath, _, filenames in os.walk("."):
    for fname in filenames:
        if not fname.endswith(".py"):
            continue
        fpath = os.path.join(dirpath, fname)
        with open(fpath, "r") as f:
            lines = f.readlines()
        rewritten = False
        with open(fpath, "w") as f:
            for line in lines:
                original = line
                for old, new in REWRITE_MAP.items():
                    line = re.sub(rf"(from|import)\\s+{old}(?!\.)", rf"\\1 {new}", line)
                if line != original:
                    rewritten = True
                f.write(line)
        if rewritten:
            print(f"✅ Updated imports in: {fpath}")
EOF
chmod +x scripts/update_imports.py

# Summary of skipped/failed actions
if [ ${#skipped[@]} -gt 0 ]; then
  echo "
⚠️  Skipped or failed to complete the following items:"
  for item in "${skipped[@]}"; do
    echo " - $item"
  done
  echo "
❌ Skipped items detected. Not suggesting import rewrite."
else
  echo "
✅ All steps succeeded. You may now run:"
  echo "   ./scripts/update_imports.py"
fi

echo "
✅ Restructure complete. Here are some useful git commands to review changes:"
echo "   git diff --name-status        # renamed, added, deleted files"
echo "   git diff --stat --summary     # rename + line change summary"
echo "   git diff --color-moved=plain  # see moved lines without noise"
echo "   git status --short            # quick file overview""

