import json
from pathlib import Path

from ghost_config import VAULT

QUEUE_PATH = VAULT / "memory" / "queue.json"

def load_queue():
    if not QUEUE_PATH.exists():
        return []
    try:
        with QUEUE_PATH.open("r") as f:
            data = f.read().strip()
            return json.loads(data) if data else []
    except json.JSONDecodeError:
        print("[ghost_queue] ⚠️ malformed queue.json — returning empty queue")
        return []

def clear_task(task_description):
    queue = load_queue()
    new_queue = [task for task in queue if task != task_description]
    with QUEUE_PATH.open("w") as f:
        json.dump(new_queue, f, indent=2)
    return new_queue