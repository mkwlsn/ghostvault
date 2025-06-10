#!/usr/bin/env python3
import os
import re
import sys

# Mapping of old module names to new paths
REWRITE_MAP = {
    'from ghost.core.config': 'from ghost.core.config',
    'import ghost.core.config as ghost_config': 'import ghost.core.config as ghost_config',
    'from ghost.core.queue': 'from ghost.core.queue',
    'import ghost.core.queue as ghost_queue': 'import ghost.core.queue as ghost_queue',
    'from ghost.core.registry': 'from ghost.core.registry',
    'import ghost.core.registry as ghost_registry': 'import ghost.core.registry as ghost_registry',
    'from ghost.core.runtime': 'from ghost.core.runtime',
    'import ghost.core.runtime as ghost_runtime': 'import ghost.core.runtime as ghost_runtime',
    'from ghost.core.state': 'from ghost.core.state',
    'import ghost.core.state as ghost_state': 'import ghost.core.state as ghost_state',
    'from ghost.utils.ghost_utils': 'from ghost.utils.ghost_utils',
    'import ghost.utils.ghost_utils as ghost_utils': 'import ghost.utils.ghost_utils as ghost_utils',
    'from ghost.cli.bootstrap': 'from ghost.cli.bootstrap',
    'import ghost.cli.bootstrap as ghost_bootstrap': 'import ghost.cli.bootstrap as ghost_bootstrap',
    'from ghost.cli.install': 'from ghost.cli.install',
    'import ghost.cli.install as ghost_install': 'import ghost.cli.install as ghost_install',
    'from ghost.cli.init': 'from ghost.cli.init',
    'import ghost.cli.init as ghost_init': 'import ghost.cli.init as ghost_init',
    'from ghost.module.modules': 'from ghost.module.modules',
    'import ghost.module.modules as ghost_modules': 'import ghost.module.modules as ghost_modules',
    'from ghost.cli.cli': 'from ghost.cli.cli',
    'import ghost.cli.cli as ghost_cli': 'import ghost.cli.cli as ghost_cli',
    'from ghost.core.daemon': 'from ghost.core.daemon',
    'import ghost.core.daemon as ghost_daemon': 'import ghost.core.daemon as ghost_daemon',
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
