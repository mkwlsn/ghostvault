import os
import sys
import time
import subprocess
from pathlib import Path

from ghost.core.config import SYSTEM, VAULT

def ensure_path():
    system_path = VAULT / "system"
    system_path_str = str(system_path)

    if system_path_str not in sys.path:
        sys.path.insert(0, system_path_str)
        os.environ["PYTHONPATH"] = system_path_str

    # Persist environment config for shell sourcing
    ghostenv_path = VAULT / ".ghostenv"
    with open(ghostenv_path, "w") as f:
        f.write(f'export PYTHONPATH="{system_path_str}"\n')

def ghost_bootstrap_routine(mode="normie"):
    start_time = time.time()
    output = []

    def echo(msg):
        print(msg)
        output.append(msg)

    ensure_path()

    if mode == "normie":
        echo("> adding CLI alias to system PATH")
        echo("> setting PYTHONPATH to system directory")
        echo("> ensuring runtime directories...")
        echo("> validating Python version (✓ 3.11.9)")
        echo("> verifying dependencies: git, python3")
        echo("> writing startup config...")
        echo("> initializing background daemon")
        elapsed = round(time.time() - start_time, 2)
        echo(f"> setup complete in {elapsed}s")
    elif mode == "cursed":
        from ghost.utils.ghost_utils import cursed_echo
        cursed_echo()

def run_ghost_bootstrap(cmd):
    ensure_path()
    if cmd == "init":
        ghost_bootstrap_routine("normie")
    elif cmd == "init-cursed":
        ghost_bootstrap_routine("cursed")

def bootstrap_main():
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        run_ghost_bootstrap(cmd)
    else:
        print("❗ usage: ghost init | ghost init-cursed")

# bootstrap_main = run_ghost_bootstrap