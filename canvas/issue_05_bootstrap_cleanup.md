# [HIGH] Bootstrap Code PYTHONPATH Cleanup

**Labels:** `high`, `code-quality`, `environment-pollution`

## The Problem Right Now

Bootstrap code **pollutes user environments** with obsolete PYTHONPATH manipulation:

```python
# ghost/cli/bootstrap.py
def ensure_path():
    system_path = VAULT / "system"  # This directory doesn't exist anymore!
    system_path_str = str(system_path)
    os.environ["PYTHONPATH"] = system_path_str  # Pollutes environment
    
    # Creates pollution artifacts
    with open(ghostenv_path, "w") as f:
        f.write(f'export PYTHONPATH="{system_path_str}"\n')

# ghost/cli/install.py 
def patch_shell_rc():
    export_line = f'export PYTHONPATH="{VAULT / "system"}"\n'
    # Permanently modifies user's shell RC files
```

**Problems:**
- References non-existent `system/` directory post-refactor
- Corrupts user's Python environment permanently
- Creates `.ghostenv` pollution files
- Breaks other Python projects

## Why This Breaks Everything

**Real scenario:** User installs ghostOS, then tries to work on another Python project.
- Bootstrap polluted PYTHONPATH with invalid `/system` path
- Other project's imports now fail mysteriously
- User has to manually clean shell configuration

With proper package structure, **PYTHONPATH manipulation is completely unnecessary**.

## The Standard We Need

```python
# Clean bootstrap without environment pollution
def ghost_bootstrap_routine():
    """Clean bootstrap that validates package structure"""
    
    # Validate package structure instead of setting paths
    required_files = [
        VAULT / "ghost" / "__init__.py",
        VAULT / "ghost" / "core" / "config.py",
        VAULT / "ghost" / "cli" / "cli.py"
    ]
    
    missing_files = [f for f in required_files if not f.exists()]
    if missing_files:
        raise RuntimeError(f"Package structure invalid: {missing_files}")
    
    # Create runtime directories
    ensure_runtime_directories()
    
    print("✅ Bootstrap complete - no environment pollution")

def ensure_runtime_directories():
    """Create required directories without PATH manipulation"""
    directories = [
        VAULT / "rituals",
        VAULT / "memory",
        VAULT / "ghost" / "state"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# REMOVED: All PYTHONPATH manipulation
# REMOVED: .ghostenv file creation  
# REMOVED: Shell RC patching
```

**Benefits:**
- Clean user environment (no pollution)
- Proper Python package imports
- Easy testing in isolated environments
- No mysterious import failures in other projects

## Implementation: 1-2 days

1. Remove all PYTHONPATH manipulation code
2. Create cleanup utility for existing pollution
3. Add environment validation instead of path setting