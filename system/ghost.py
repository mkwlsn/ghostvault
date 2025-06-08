#!/usr/bin/env python3

import sys
import subprocess
import os
from datetime import datetime
from pathlib import Path

VAULT = Path.home() / "ghostvault"
sys.path.append(str(VAULT / "system"))

from Ghost_Os import MODULES # exact file name, case-sensitive


def log_event(msg):
    path = VAULT / "memory" / "events.md"
    with path.open("a") as f:
        f.write(f"- {datetime.today().date()} — {msg}\n")
    print(f"📝 log saved: {msg}")

def queue_task(task):
    path = VAULT / "system" / "ghost-queue.md"
    with path.open("a") as f:
        f.write(f"- [ ] {task}\n")
    print(f"📋 task queued: {task}")

def log_ritual(summary):
    date_str = datetime.today().strftime("%Y-%m-%d")
    path = VAULT / "rituals" / f"daily-log-{date_str}.md"
    header = f"# 🔁 ritual log — {date_str}\n\n"
    if not path.exists():
        path.write_text(header)
    with path.open("a") as f:
        f.write(f"- {summary}\n")
    print(f"📿 ritual logged for {date_str}")

    
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
    ghost_sync_modules() # 👈🏾 awareness ritual

def ghost_sync_modules():
    print("🔁 syncing modules from markdown…")

    module_dir = VAULT / "modules"
    new_modules = {}

    for file in module_dir.glob("*.md"):
        name = file.stem
        content = file.read_text()

        def extract(label):
            prefix = f"**{label}**:"
            if prefix in content:
                section = content.split(prefix)[1].split("\n\n")[0]
                return [line.strip("- ").strip() for line in section.splitlines() if line.strip().startswith("-")]
            return []

        desc = content.split("**description**:")[1].split("**inputs**:")[0].strip().strip("(tbd)")
        new_modules[name] = {
            "description": desc.strip(),
            "inputs": extract("inputs"),
            "outputs": extract("outputs"),
            "interoperability": extract("interoperability")
        }

    print(f"📦 found {len(new_modules)} modules:")
    for name in new_modules:
        print(f"• {name}")

    # write to Ghost_Os.py
    module_path = VAULT / "system" / "Ghost_Os.py"
    with module_path.open("w") as f:
        f.write("MODULES = {\n")
        for name, data in new_modules.items():
            f.write(f'    "{name}": {{\n')
            for key in ["description", "inputs", "outputs", "interoperability"]:
                val = data[key]
                if isinstance(val, list):
                    f.write(f'        "{key}": {val},\n')
                else:
                    f.write(f'        "{key}": "{val}",\n')
            f.write("    },\n")
        f.write("}\n")

    print("✅ Ghost_Os.py updated")

def ghost_gen_prompt(module_name):
    print(f"📦 generating prompt for module: {module_name}")
    module = MODULES.get(module_name)
    if not module:
        print(f"❗ unknown module: {module_name}")
        return

    # pull recent queue items (optional pre-seed)
    queue_path = VAULT / "system" / "ghost-queue.md"
    tasks = []
    if queue_path.exists():
        with queue_path.open() as f:
            for line in f:
                if module_name in line and line.startswith("- [ ]"):
                    tasks.append(line[6:].strip())

    print("\n--- BEGIN PROMPT ---\n")
    print(f"You are operating as the `{module_name}` module inside a larger AI-native operating system (GhostOS).")
    print(f"Your purpose: {module['description']}\n")

    if tasks:
        print("Relevant queued tasks:")
        for t in tasks:
            print(f"- {t}")
        print()

    print("Expected inputs:")
    for i in module['inputs']:
        print(f"- {i}")

    print("\nExpected outputs:")
    for o in module['outputs']:
        print(f"- {o}")

    print("\nInstructions:")
    print(f"Please behave as a stateless agent. Accept your inputs, return outputs, and remain within scope of the `{module_name}` function.\n")
    print("--- END PROMPT ---\n")


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
    if ritual_dir.exists():
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

def ghost_echo():
    print("🪞 ghost echo — most recent memory")

    # last ritual
    ritual_dir = VAULT / "rituals"
    ritual_files = sorted(ritual_dir.glob("daily-log-*.md"), reverse=True)
    if ritual_files:
        last_ritual = ritual_files[0]
        lines = [line.strip() for line in last_ritual.open() if line.startswith("- ")]
        if lines:
            print(f"\n🔁 last ritual: {lines[-1][2:]}")
    else:
        print("\n🔁 no rituals found")

    # last task
    queue_path = VAULT / "system" / "ghost-queue.md"
    if queue_path.exists():
        tasks = [line.strip() for line in queue_path.open() if line.startswith("- [ ]")]
        if tasks:
            print(f"📋 last task: {tasks[-1][6:].strip()}")
        else:
            print("📋 no open tasks")
    else:
        print("📋 queue file missing")

    # last log
    log_path = VAULT / "memory" / "events.md"
    if log_path.exists():
        lines = [line.strip() for line in log_path.open() if line.startswith("- ")]
        if lines:
            print(f"📝 last log: {lines[-1][2:]}")
        else:
            print("📝 no logs found")
    else:
        print("📝 memory file missing")        


def macro_expand(text):
    macros = {
        ":ritual:": "🔁",
        ":summon:": "📡",
        ":haunt:": "🪄",
        ":mirror:": "🪞",
        ":bind:": "🧷",
        ":drift:": "🌫️"
    }
    for k, v in macros.items():
        text = text.replace(k, v)
    return text

def show_help():
    print("""ghost.py — local ghost CLI

usage:        
  ghost.py new module <name>
  ghost.py gen prompt <module_name>        
  ghost.py log "<msg>"
  ghost.py queue "<task>"
  ghost.py ritual "<summary>"
  ghost.py push [--message "<msg>"]
  ghost.py status
  ghost.py echo                
""")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        show_help()
        sys.exit(0)

    cmd = args[0]

    if cmd == "new":
        if len(args) >= 3 and args[1] == "module":
            new_module(args[2])
        else:
            print("❗ usage: ghost.py new module <name>")
    elif cmd == "log":
        if len(args) >= 2:
            log_event(macro_expand(" ".join(args[1:])))
        else:
            print("❗ usage: ghost.py log \"<msg>\"")
    elif cmd == "queue":
        if len(args) >= 2:
            queue_task(macro_expand(" ".join(args[1:])))
        else:
            print("❗ usage: ghost.py queue \"<task>\"")
    elif cmd == "ritual":
        if len(args) >= 2:
            log_ritual(macro_expand(" ".join(args[1:])))
        else:
            print("❗ usage: ghost.py ritual \"<summary>\"")
    elif cmd == "push":
        custom_msg = None
        if len(args) > 2 and args[1] == "--message":
            custom_msg = " ".join(args[2:])
        ghost_push(custom_msg)
    elif cmd == "gen":
        if len(args) >= 3 and args[1] == "prompt":
            ghost_gen_prompt(macro_expand(args[2]))
        else:
            print("❗ usage: ghost.py gen prompt <module_name>")
    elif cmd == "status":
        ghost_status()
    elif cmd == "echo":
        ghost_echo()
    elif cmd == "sync":
        if len(args) > 1 and args[1] == "modules":
            ghost_sync_modules()
        else:
            print("❗ usage: ghost.py sync modules")
    else:
        print(f"❓ unknown command: {cmd}")
        show_help()


