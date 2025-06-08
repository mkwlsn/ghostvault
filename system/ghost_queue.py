import json
from pathlib import Path

QUEUE_PATH = Path(__file__).resolve().parent.parent / "memory" / "queue.json"

def load_queue():
    if not QUEUE_PATH.exists():
        return []
    try:
        with open(QUEUE_PATH, "r") as f:
            data = f.read().strip()
            return json.loads(data) if data else []
    except json.JSONDecodeError:
        print("[ghost_queue] ⚠️ malformed queue.json — returning empty queue")
        return []

def clear_task(task_description):
    queue = load_queue()
    new_queue = [task for task in queue if task != task_description]
    with open(QUEUE_PATH, "w") as f:
        json.dump(new_queue, f, indent=2)
    return new_queue

def run_ritual_for_task(task):
    print(f"[ghost_modules] running ritual for task: {task}")
    # placeholder logic — eventually this will delegate to the appropriate module