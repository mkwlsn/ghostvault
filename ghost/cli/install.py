import sys
import subprocess
import time
import os
import shutil
from pathlib import Path
from ghost.cli.init import cursed_output, clean_output
from ghost.core.config import VAULT, GHOST_ROOT

def check_python_version():
    if sys.version_info < (3, 10):
        print("Python 3.10 or higher is required.")
        sys.exit(1)

def check_dependencies():
    try:
        subprocess.run(["git", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except subprocess.CalledProcessError:
        print("Git is required but not found.")
        sys.exit(1)

def ensure_venv():
    venv_path = VAULT / ".venv"
    python_bin = venv_path / "bin" / "python"
    if not venv_path.exists():
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
    return python_bin

def ensure_runtime_dirs():
    """Create runtime directories"""
    directories = [
        VAULT / "rituals",
        VAULT / "memory",
        VAULT / "modules", 
        GHOST_ROOT / "state",
        GHOST_ROOT / "state" / "cache"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

def symlink_ghost_cli():
    """Create CLI symlink without environment modification"""
    local_bin = Path.home() / ".local" / "bin"
    local_bin.mkdir(parents=True, exist_ok=True)
    ghost_cli_target = VAULT / "ghost.py"
    ghost_symlink = local_bin / "ghost"

    if not ghost_symlink.exists():
        try:
            ghost_symlink.symlink_to(ghost_cli_target)
            print(f"✅ Created ghost CLI symlink at {ghost_symlink}")
        except FileExistsError:
            print("⚠️  Could not create symlink: file already exists.")
        except Exception as e:
            print(f"⚠️  Symlink creation failed: {e}")
    else:
        print(f"✅ Ghost CLI symlink already exists at {ghost_symlink}")

def validate_package_structure():
    """Validate that ghost package can be imported properly"""
    try:
        # Test critical imports
        from ghost.core.config import VAULT
        from ghost.core.runtime import log_event
        from ghost.cli.cmd import main
        print("✅ Package structure validated - imports working")
        return True
    except ImportError as e:
        print(f"❌ Package structure invalid: {e}")
        return False

def install_dependencies(python_bin):
    reqs = VAULT / "requirements.txt"
    if reqs.exists():
        subprocess.run([str(python_bin), "-m", "pip", "install", "-r", str(reqs)], check=True)

def run_install(cursed=False):
    start_time = time.time()
    
    # Pre-flight checks
    check_python_version()
    check_dependencies()
    
    # Set up directories
    ensure_runtime_dirs()
    
    # Create symlink
    symlink_ghost_cli()
    
    # Set up virtual environment
    python_bin = ensure_venv()
    install_dependencies(python_bin)
    
    # Validate package structure
    if not validate_package_structure():
        print("⚠️  Package validation failed - ghost may not work properly")
    
    duration = time.time() - start_time

    if cursed:
        cursed_output()
    else:
        clean_output(duration)