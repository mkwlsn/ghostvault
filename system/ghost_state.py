import subprocess
from datetime import datetime

from ghost_config import VAULT, SYSTEM

def ghost_status():
    print("🔍 ghost status report\n")

    # git status
    print("🌀 git:")
    try:
        output = subprocess.check_output(["git", "status", "-s"], text=True)
        print(output.strip())
    except subprocess.CalledProcessError:
        print("❗ git error")

    # queue
    print("\n📋 queue:")
    queue_path = SYSTEM / "ghost-queue.md"
    if queue_path.exists():
        with queue_path.open() as f:
            lines = [line.strip() for line in f if line.startswith("- [ ]")]
            for line in lines:
                print(f"• {line[6:]}")
    else:
        print("❌ no queue found")

    # last ritual
    print("\n🔁 last ritual:")
    today = datetime.today().strftime("%Y-%m-%d")
    ritual_path = VAULT / "rituals" / f"daily-log-{today}.md"
    print(f"🗓️ {ritual_path.name}")
    if ritual_path.exists():
        with ritual_path.open() as f:
            lines = [line.strip() for line in f if line.startswith("-")]
            for line in lines[-5:]:
                print(f"{line}")
    else:
        print("🔁 no rituals found")

def ghost_echo():
    print("🪞 ghost memory echo:\n")

    # uses print_last_line() helper for consistent formatting
    from datetime import datetime

    ritual_dir = VAULT / "rituals"
    ritual_files = sorted(ritual_dir.glob("daily-log-*.md"), reverse=True)
    if ritual_files:
        last_file = ritual_files[0]
        date_str = last_file.stem.replace("daily-log-", "")
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        delta_days = (datetime.today().date() - date_obj).days
        with last_file.open() as f:
            lines = [line.strip() for line in f if line.startswith("- ")]
        if lines:
            suffix = (
                ""
                if delta_days == 0 else
                " (yesterday)"
                if delta_days == 1 else
                f" ({delta_days} days ago)"
            )
            print(f"🔁 last ritual:\n{lines[-1][2:]}{suffix}")
        else:
            print("🔁 last ritual: (log was empty)")
    else:
        print("🔁 no rituals found")

    queue_path = SYSTEM / "ghost-queue.md"
    print_last_line(queue_path, "last task", "📋")

    event_path = VAULT / "memory" / "events.md"
    print_last_line(event_path, "last log", "📝")

# helper: print the last matching line from a given file, formatted with emoji + label
def print_last_line(path, label, emoji):
    if path.exists():
        with path.open() as f:
            if label == "last task":
                lines = [line.strip() for line in f if line.startswith("- [ ]")]
                if lines:
                    print(f"{emoji} {label}:\n{lines[-1][6:]}")
            else:
                lines = [line.strip() for line in f if line.startswith("- ")]
                if lines:
                    print(f"{emoji} {label}:\n{lines[-1]}")
    else:
        print(f"{emoji} no {label} found")
