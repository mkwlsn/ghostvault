import datetime

from ghost_config import VAULT, SYSTEM
from ghost_registry import MODULES

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
    ghost_sync_modules()  # 👈 awareness ritual

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

    # write to ghost_registry.py
    module_path = SYSTEM / "ghost_registry.py"
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
    queue_path = SYSTEM / "ghost-queue.md"
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