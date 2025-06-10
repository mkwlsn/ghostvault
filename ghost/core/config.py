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
