"""
ghostOS-kernel configuration
Flat, observable paths for execution substrate
"""
from pathlib import Path

# Root directories
VAULT = Path.home() / "ghostvault"
GHOST_ROOT = VAULT / "ghost"

# Kernel modules
DAEMON_DIR = GHOST_ROOT / "daemon"
QUEUE_DIR = GHOST_ROOT / "queue" 
LOGS_DIR = GHOST_ROOT / "logs"
CONFIG_DIR = GHOST_ROOT / "config"
CLI_DIR = GHOST_ROOT / "cli"
TESTS_DIR = GHOST_ROOT / "tests"

# Runtime files
QUEUE_JSON = QUEUE_DIR / "queue.json"
EVENTS_MD = LOGS_DIR / "events.md" 
DAEMON_PID = DAEMON_DIR / "daemon.pid"