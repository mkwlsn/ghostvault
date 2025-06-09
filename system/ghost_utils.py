import subprocess
from  pathlib import Path
from datetime import datetime

VAULT = Path.home() / "ghostvault"
SYSTEM = VAULT / "system"

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

def ghost_push(custom_msg=None):
    subprocess.run(["git", "add", "."], cwd=str(VAULT))
    msg = custom_msg or f"🧠 ghost sync: {datetime.today().isoformat()}"
    subprocess.run(["git", "commit", "-m", msg], cwd=str(VAULT))
    subprocess.run(["git", "push"], cwd=str(VAULT)) 


""" future functionality for local repo sync to ghost web endpoint """
# def ghost_seance()