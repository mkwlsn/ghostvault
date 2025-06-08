# ghostd.py — GhostOS local daemon

"""
watches the queue and memory system for tasks and triggers corresponding rituals.
can be run as a background process or invoked manually via CLI.
"""

import time
from ghost_queue import load_queue, clear_task
from ghost_modules import run_ritual_for_task

def ghostd_loop(poll_interval=10):
    print("👻 ghostd running — watching queue...")
    while True:
        queue = load_queue()
        for task in queue:
            print(f"🔁 running ritual for: {task}")
            run_ritual_for_task(task)
            clear_task(task)
        time.sleep(poll_interval)

if __name__ == "__main__":
    ghostd_loop()
