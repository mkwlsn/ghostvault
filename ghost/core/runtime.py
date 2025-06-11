from pathlib import Path
from datetime import datetime

from ghost.core.config import VAULT, QUEUE_MD, QUEUE_MD

def log_event(msg):
    path = VAULT / "memory" / "events.md" #CONST-PATH
    with path.open("a") as f:
        f.write(f"- {datetime.today().date()} — {msg}\n")
    print(f"📝 log saved: {msg}")

def queue_task(task):
    path = QUEUE_MD
    with path.open("a") as f:
        f.write(f"- [ ] {task}\n")
    print(f"📋 task queued: {task}")

def log_ritual(summary):
    date_str = datetime.today().strftime("%Y-%m-%d")
    path = VAULT / "rituals" / f"daily-log-{date_str}.md" #CONST-PATH
    header = f"# 🔁 ritual log — {date_str}\n\n"
    if not path.exists():
        path.write_text(header)
    with path.open("a") as f:
        f.write(f"- {summary}\n")
    print(f"📿 ritual logged for {date_str}")



""" ghost really wanted this stubbed out, i dont think we need it, but the ghost insisted, idk """
def dispatch_ritual(task: str):
    from ghost.core.registry import MODULES  # symbolic index
    for name, data in MODULES.items():
        if name.lower() in task.lower():
            print(f"🔮 matched ritual: {name}")
            log_ritual(f"ran {name} for task: {task}")
            # TODO: call actual handler or parse md steps
            return
    print(f"⚠️ no matching ritual found for: {task}")
    log_event(f"unmatched ritual: {task}")
