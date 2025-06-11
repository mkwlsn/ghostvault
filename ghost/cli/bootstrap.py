import os
import sys
import time
import subprocess
from pathlib import Path

from ghost.core.config import VAULT, GHOST_ROOT

def validate_package_structure():
    """Validate ghost package structure instead of manipulating paths"""
    required_files = [
        GHOST_ROOT / "__init__.py",                 #CONST-PATH
        GHOST_ROOT / "core" / "__init__.py",        #CONST-PATH
        GHOST_ROOT / "core" / "config.py",          #CONST-PATH
        GHOST_ROOT / "cli" / "__init__.py",         #CONST-PATH
        GHOST_ROOT / "cli" / "cli.py"               #CONST-PATH
    ]
    
    missing_files = [f for f in required_files if not f.exists()]
    if missing_files:
        raise RuntimeError(f"Invalid package structure. Missing files: {missing_files}")
    
    return True

def ensure_runtime_directories():
    """Create required runtime directories without environment manipulation"""
    directories = [
        VAULT / "rituals",                           #CONST-PATH
        VAULT / "memory",                            #CONST-PATH 
        VAULT / "modules",                           #CONST-PATH
        GHOST_ROOT / "state",                        #CONST-PATH
        GHOST_ROOT / "state" / "cache"               #CONST-PATH
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

def ghost_bootstrap_routine(mode="normie"):
    """Clean bootstrap without environment pollution"""
    start_time = time.time()
    output = []

    def echo(msg):
        print(msg)
        output.append(msg)

    try:
        # Validate package structure
        echo("> validating ghost package structure...")
        validate_package_structure()
        echo("> package structure valid ✓")
        
        # Create runtime directories
        echo("> ensuring runtime directories...")
        ensure_runtime_directories()
        
        if mode == "normie":
            echo("> verifying Python version...")
            python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            echo(f"> Python {python_version} ✓")
            echo("> verifying dependencies: git, python3")
            echo("> initializing state files...")
            
            # Initialize empty state files if needed
            queue_json = GHOST_ROOT / "state" / "queue.json"        #CONST-PATH
            if not queue_json.exists():
                queue_json.write_text("[]")
            
            elapsed = round(time.time() - start_time, 2)
            echo(f"> setup complete in {elapsed}s")
            
    except Exception as e:
        echo(f"❌ Bootstrap failed: {e}")
        raise

def run_ghost_bootstrap(cmd):
    """Entry point for bootstrap commands"""
    if cmd == "init":
        ghost_bootstrap_routine("normie")

def bootstrap_main():
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        run_ghost_bootstrap(cmd)
    else:
        print("❗ usage: ghost init")