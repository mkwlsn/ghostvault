#!/usr/bin/env python3

import sys
from datetime import datetime
from pathlib import Path

import subprocess
import os

VAULT = Path.home() / "ghostvault"

def log_event(msg):
    path = VAULT / "memory" / "events.md"
    with path.open("a") as f:
        f.write(f"- {datetime.today().date()} — {msg}\n")

def queue_task(task):
    path = VAULT / "system" / "ghost-queue.md"
    with path.open("a") as f:
        f.write(f"- [ ] {task}\n")

def new_module(name):
    path = VAULT / "modules" / f"{name}.md"
    if path.exists():
        print(f"❗ module '{name}' already exists.")
        return
    content = f"""# 🧩 module: {name}

**description**:  
(tbd)

**inputs**:  
- 

**outputs**:  
- 

**interoperability**:  
- 

---

## changelog
- {datetime.today().date()} — module scaffolded
"""
    path.write_text(content)
    print(f"✅ module '{name}' created.")

def log_ritual(summary):
    date_str = datetime.today().strftime("%Y-%m-%d")
    path = VAULT / "rituals" / f"daily-log-{date_str}.md"
    header = f"# 🔁 ritual log — {date_str}\n\n"
    if not path.exists():
        path.write_text(header)
    with path.open("a") as f:
        f.write(f"- {summary}\n")
    print(f"📿 ritual logged for {date_str}")

def ghost_push(custom_msg=None):
    try:
        subprocess.run(["git", "add", "."], cwd=VAULT, check=True)

        msg = custom_msg or f"🧠 ghost update — {datetime.today().date()}"
        subprocess.run(["git", "commit", "-m", msg], cwd=VAULT, check=True)

        subprocess.run(["git", "push"], cwd=VAULT, check=True)
        print("🚀 ghost pushed")
    except subprocess.CalledProcessError:
        print("❗ git push failed — check status manually")

def ghost_status():
    print("🔍 ghost status report\n")

    # git status
    try:
        print("🌀 git:")
        subprocess.run(["git", "status", "-s"], cwd=VAULT, check=True)
        subprocess.run(["git", "branch", "--show-current"], cwd=VAULT, check=True)
    except subprocess.CalledProcessError:
        print("❗ git error")

    print("\n📋 queue:")
    queue_path = VAULT / "system" / "ghost-queue.md"
    if queue_path.exists():
        with open(queue_path) as f:
            lines = [line.strip() for line in f if line.startswith("- [ ]")]
            if lines:
                for line in lines:
                    print("•", line[6:].strip())
            else:
                print("✓ no pending tasks")
    else:
        print("⚠️ ghost-queue.md not found")

    print("\n🔁 last ritual:")
    ritual_dir = VAULT / "rituals"
    ritual_files = sorted(ritual_dir.glob("daily-log-*.md"), reverse=True)
    if ritual_files:
        last = ritual_files[0]
        print(f"🗓️ {last.name}")
        with last.open() as f:
            for line in f:
                if line.startswith("- "):
                    print("•", line.strip()[2:])
    else:
        print("⚠️ no ritual logs found")



def show_help():
    print("""ghost.py — local ghost CLI

usage:
  ghost.py new module <name>
  ghost.py log "<msg>"
  ghost.py queue "<task>"
  ghost.py ritual "<summary>"
""")

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        show_help()
        sys.exit(0)

    cmd = args[0]
    if cmd == "new" and args[1] == "module":
        new_module(args[2])
    elif cmd == "log":
        log_event(" ".join(args[1:]))
    elif cmd == "queue":
        queue_task(" ".join(args[1:]))
    elif cmd == "ritual":
        log_ritual(" ".join(args[1:]))
    elif cmd == "push":
        custom_msg = None
        if len(args) > 1 and args[1] == "--message":
            custom_msg = " ".join(args[2:])
        ghost_push(custom_msg)
    elif cmd == "status":
        ghost_status()
    else:
        show_help()

