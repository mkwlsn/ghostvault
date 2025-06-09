import sys
from ghost_runtime import (
    log_event, queue_task, log_ritual
)
from ghost_modules import new_module, ghost_sync_modules, ghost_gen_prompt
from ghost_state import ghost_status, ghost_echo
from ghost_utils import macro_expand, ghost_push


def show_help():
    print("""ghost — local ghost CLI

usage:        
  ghost new module <name>
  ghost gen prompt <module_name>        
  ghost log "<msg>"
  ghost queue "<task>"
  ghost ritual "<summary>"
  ghost push [--message "<msg>"]
  ghost status
  ghost echo
  ghost start
  ghost stop
  ghost statusd
  ghost sync modules
""")


def main():
    args = sys.argv[1:]
    if not args:
        show_help()
        sys.exit(0)

    cmd = args[0]

    match cmd:
        case "new":
            if len(args) >= 3 and args[1] == "module":
                new_module(args[2])
            else:
                print("❗ usage: ghost new module <name>")

        case "log":
            if len(args) >= 2:
                log_event(macro_expand(" ".join(args[1:])))
            else:
                print("❗ usage: ghost log \"<msg>\"")

        case "queue":
            if len(args) >= 2:
                queue_task(macro_expand(" ".join(args[1:])))
            else:
                print("❗ usage: ghost queue \"<task>\"")

        case "ritual":
            if len(args) >= 2:
                log_ritual(macro_expand(" ".join(args[1:])))
            else:
                print("❗ usage: ghost ritual \"<summary>\"")

        case "push":
            custom_msg = None
            if len(args) > 2 and args[1] == "--message":
                custom_msg = " ".join(args[2:])
            ghost_push(custom_msg)

        case "gen":
            if len(args) >= 3 and args[1] == "prompt":
                ghost_gen_prompt(macro_expand(args[2]))
            else:
                print("❗ usage: ghost gen prompt <module_name>")

        case "status":
            ghost_status()

        case "echo":
            ghost_echo()

        case "sync":
            if len(args) > 1 and args[1] == "modules":
                ghost_sync_modules()
            else:
                print("❗ usage: ghost sync modules")

        case "start":
            from ghost_runtime import start_ghostd
            start_ghostd()

        case "stop":
            from ghost_runtime import stop_ghostd
            stop_ghostd()

        case "statusd":
            from ghost_runtime import status_ghostd
            status_ghostd()

        case _:
            print(f"❓ unknown command: {cmd}")
            show_help()