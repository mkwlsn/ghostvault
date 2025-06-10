from ghost.core.config import STATE_DIR# ghostd.py — GhostOS local daemon

"""
watches the queue and memory system for tasks and triggers corresponding rituals.
can be run as a background process or invoked manually via CLI.
"""

import time
from ghost.core.queue import load_queue, clear_task
from ghost.core.runtime import dispatch_ritual

def ghostd_loop(poll_interval=10):
    print("👻 ghostd running — watching queue...")
    while True:
        queue = load_queue()
        for task in queue:
            print(f"🔁 running ritual for: {task}")
            dispatch_ritual(task)
            clear_task(task)
        time.sleep(poll_interval)

if __name__ == "__main__":
    ghostd_loop()
