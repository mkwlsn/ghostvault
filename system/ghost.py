#!/usr/bin/env python3

import sys
import subprocess
import signal
import os
import psutil
from datetime import datetime
from pathlib import Path

VAULT = Path.home() / "ghostvault"
sys.path.append(str(VAULT / "system"))

from ghost_modules import MODULES # exact file name, case-sensitive


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

    # write to ghost_modules.py
    module_path = VAULT / "system" / "ghost_modules.py"
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

    print("✅ ghost_modules.py updated")

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

    # --- ghostd daemon management commands ---
    elif cmd == "start":
        # macOS-only: launchd autostart logic for ghostd
        # If ~/Library/LaunchAgents/com.ghostos.ghostd.plist does not exist, prompt to install autostart plist.
        # If user agrees, create the plist, load it with launchctl, and echo status.
        # If not, start the daemon once with subprocess.Popen.
        import sys
        import getpass
        import shutil
        # --- macOS-only implementation of autostart via launchd. Cross-platform support is a future enhancement. ---
        print("👻 starting ghostd...")
        home = Path.home()
        launch_agents_dir = home / "Library" / "LaunchAgents"
        plist_path = launch_agents_dir / "com.ghostos.ghostd.plist"
        ghostd_path = VAULT / "system" / "ghostd.py"
        python_exec = sys.executable
        # Check if plist exists
        if not plist_path.exists():
            try:
                reply = input("no ghost daemon on launch. install autostart plist? (y/n): ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\n❌ Aborted.")
                sys.exit(1)
            if reply == "y":
                # Create LaunchAgents directory if needed
                try:
                    launch_agents_dir.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    print(f"❌ Failed to create LaunchAgents directory: {e}")
                    sys.exit(1)
                # Write plist XML
                plist_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ghostos.ghostd</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python_exec}</string>
        <string>{ghostd_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
"""
                try:
                    with open(plist_path, "w") as f:
                        f.write(plist_xml)
                    print(f"✅ launchd plist created at {plist_path}")
                except Exception as e:
                    print(f"❌ Failed to write plist: {e}")
                    sys.exit(1)
                # Load with launchctl
                try:
                    subprocess.run(["launchctl", "load", str(plist_path)], check=True)
                    print("🚀 ghostd autostarted via launchd.")
                    print("ℹ️ ghostd will now run at login (and is running now).")
                except subprocess.CalledProcessError as e:
                    print(f"❌ launchctl load failed: {e}")
                    print("You may need to load the plist manually or check permissions.")
            else:
                # Start the daemon once (not persistent)
                try:
                    process = subprocess.Popen([python_exec, str(ghostd_path)])
                    with open("ghostd.pid", "w") as f:
                        f.write(str(process.pid))
                    print(f"👻 ghostd running with PID {process.pid} (one-shot, not persistent)")
                except Exception as e:
                    print(f"❌ Failed to start ghostd: {e}")
        else:
            # Plist exists, try to load it (if not already loaded)
            try:
                subprocess.run(["launchctl", "load", str(plist_path)], check=True)
                print("🚀 ghostd launchd plist already exists and loaded.")
                print("ℹ️ ghostd will run at login (and is running now).")
            except subprocess.CalledProcessError as e:
                print(f"❌ launchctl load failed: {e}")
                print("You may need to load the plist manually or check permissions.")
    elif cmd == "stop":
        # Stop the ghost daemon
        if not os.path.exists("ghostd.pid"):
            print("❌ no running ghostd process found.")
        else:
            with open("ghostd.pid", "r") as f:
                pid = int(f.read())
            try:
                os.kill(pid, signal.SIGTERM)
                print("🛑 ghostd stopped.")
            except ProcessLookupError:
                print("⚠️ process not found. cleaning up.")
            os.remove("ghostd.pid")
    elif cmd == "statusd":
        # Check ghostd daemon status
        if not os.path.exists("ghostd.pid"):
            print("🟡 ghostd not running.")
        else:
            with open("ghostd.pid", "r") as f:
                pid = int(f.read())
            if psutil.pid_exists(pid):
                print(f"🟢 ghostd is running (PID {pid})")
            else:
                print("🟡 ghostd PID file found but process not active.")
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


