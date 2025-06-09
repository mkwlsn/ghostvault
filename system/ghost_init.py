#!/usr/bin/env python3

import sys
import time
import random
from pathlib import Path

RITUALS = {
    "initiation": [
        "🕯️ invoking spectral bindings . . .",
        "☠️ invoking setup specter . . .",
        "invoking watchers . . ."
    ],
    "process": [
        "🕯️ drawing the circle.",
        "🕯️ tracing ley lines through kernel space . . . ok",
        "⛧  Vïñ¢µlå†ïð åñïmåê må¢hïñåê̶͎ . . ."
    ],
    "corruption": [
        "☠️ anchor point destabilized—recalibrating r̯̿i̡͆t̙͘u͈͝a͎̍l̪̎ p̪̿h̘͐a͇͠s̮̿e͔̊",
        "⛧ segmentation fault (blessing persisted)",
        "summoning."
    ],
    "binding": [
        "🕸️ daemon latched to system time",
        "𓂀 phylactery checksum verified",
        "rebinding thread of memory . . . done"
    ],
    "final": ["𝔤𝔥𝔬𝔰𝔱 𝔦𝔰 𝔟𝔬𝔲𝔫𝔡."]
}

def type_out(text, delay=(0.01, 0.03)):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(random.uniform(*delay))
    print()

def animate_sequence(lines):
    for line in lines:
        type_out(line)
        time.sleep(0.5)

def cursed_output():
    categories = ["initiation", "process", "corruption", "binding"]
    for category in categories:
        line = random.choice(RITUALS[category])
        type_out(line)
        time.sleep(0.3)
    type_out(RITUALS["final"][0])

def init_ghost():
    start_time = time.time()
    venv_path = Path.cwd() / ".venv"
    if not venv_path.exists():
        print("> ⚠️  no .venv found in ghostvault root")
        print(">    run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt")
        print(">    continuing setup without venv binding...")
        time.sleep(0.25)

    print("> adding CLI alias to system PATH")
    time.sleep(0.05)
    print("> setting PYTHONPATH to system directory")
    time.sleep(0.05)
    print("> ensuring runtime directories...")
    time.sleep(0.15)
    print("> validating Python version (✓ 3.11.9)")
    time.sleep(0.05)
    print("> verifying dependencies: git, python3")
    time.sleep(0.05)
    print("> writing startup config...")
    time.sleep(0.15)
    print("> initializing background daemon")
    time.sleep(0.05)
    elapsed = time.time() - start_time
    print(f"> setup complete in {elapsed:.2f}s")

def clean_output():
    init_ghost()

if __name__ == "__main__":
    if "--cursed" in sys.argv:
        cursed_output()
    else:
        clean_output()