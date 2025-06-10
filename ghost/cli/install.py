import sys
import subprocess
import time
import os
import shutil
from pathlib import Path
from system.ghost_init import cursed_output, clean_output
from ghost_config import VAULT, RITUALS


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
    for name in RITUALS:
        dir_path = VAULT / name
        dir_path.mkdir(parents=True, exist_ok=True)

def symlink_ghost_cli():
    local_bin = Path.home() / ".local" / "bin"
    local_bin.mkdir(parents=True, exist_ok=True)
    ghost_cli_target = VAULT / "ghost.py"
    ghost_symlink = local_bin / "ghost"

    if not ghost_symlink.exists():
        try:
            ghost_symlink.symlink_to(ghost_cli_target)
        except FileExistsError:
            print("Could not create symlink: file already exists.")
        except Exception as e:
            print(f"Symlink creation failed: {e}")

# Adds PYTHONPATH export to shell rc file for ambient CLI usage
def patch_shell_rc():
    shell = Path(os.environ.get("SHELL", "/bin/zsh")).name
    home = Path.home()
    rc_file = home / f".{shell}rc"
    export_line = f'export PYTHONPATH="{VAULT / "system"}"\n'
    marker = "# ghostOS path config\n"

    if not rc_file.exists():
        return

    with open(rc_file, "r") as f:
        contents = f.read()

    if marker in contents or export_line in contents:
        return

    with open(rc_file, "a") as f:
        f.write("\n" + marker + export_line)

def install_dependencies(python_bin):
    reqs = VAULT / "requirements.txt"
    if reqs.exists():
        subprocess.run([str(python_bin), "-m", "pip", "install", "-r", str(reqs)], check=True)

def run_install(cursed=False):
    start_time = time.time()
    check_python_version()
    check_dependencies()
    ensure_runtime_dirs()
    symlink_ghost_cli()
    patch_shell_rc()
    python_bin = ensure_venv()
    install_dependencies(python_bin)
    duration = time.time() - start_time

    if cursed:
        cursed_output()
    else:
        clean_output(duration)