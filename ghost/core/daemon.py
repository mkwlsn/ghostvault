import subprocess
import os
import signal
import sys
import psutil
from pathlib import Path

from ghost.core.config import VAULT, DAEMON_PID

def main():
    print("[ghostd] daemon.py alive. looping...")
    daemon_loop()


def start_ghostd():
    print("👻 starting ghostd...")
    home = Path.home()
    launch_agents_dir = home / "Library" / "LaunchAgents"
    plist_path = launch_agents_dir / "com.ghostos.ghostd.plist"
    ghostd_path = VAULT / "ghost" / "ghostd.py"
    python_exec = sys.executable

    if not plist_path.exists():
        try:
            reply = input("no ghost daemon on launch. install autostart plist? (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n❌ Aborted.")
            sys.exit(1)

        if reply == "y":
            try:
                launch_agents_dir.mkdir(parents=True, exist_ok=True)
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
    </array>/by
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
"""
                with open(plist_path, "w") as f:
                    f.write(plist_xml)
                subprocess.run(["launchctl", "load", str(plist_path)], check=True)
                print("🚀 ghostd autostarted via launchd.")
            except Exception as e:
                print(f"❌ Failed to set up plist: {e}")
                sys.exit(1)
        else:
            try:
                process = subprocess.Popen([python_exec, str(ghostd_path)])
                with open(DAEMON_PID, "w") as f:
                    f.write(str(process.pid))
                print(f"👻 ghostd running with PID {process.pid} (one-shot, not persistent)")
            except Exception as e:
                print(f"❌ Failed to start ghostd: {e}")
    else:
        try:
            subprocess.run(["launchctl", "load", str(plist_path)], check=True)
            print("🚀 ghostd launchd plist already exists and loaded.")
        except subprocess.CalledProcessError as e:
            print(f"❌ launchctl load failed: {e}")

def stop_ghostd():
    if not os.path.exists(STATE_DIR / "daemon.pid"):
        print("❌ no running ghostd process found.")
    else:
        with open(STATE_DIR / "daemon.pid", "r") as f:
            pid = int(f.read())
        try:
            os.kill(pid, signal.SIGTERM)
            print("🛑 ghostd stopped.")
        except ProcessLookupError:
            print("⚠️ process not found. cleaning up.")
        os.remove(STATE_DIR / "daemon.pid")

def status_ghostd():
    if not os.path.exists(STATE_DIR / "daemon.pid"):
        return "status: not running"
    else:
        with open(STATE_DIR / "daemon.pid", "r") as f:
            pid = int(f.read())
        if psutil.pid_exists(pid):
            return f"status: running (PID {pid})"
        else:
            return "status: stale PID file (process not active)"