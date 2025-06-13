import sys
from ghost.core.runtime import (
    log_event, queue_task, log_ritual
)
from ghost.module.modules import new_module, ghost_sync_modules, ghost_gen_prompt
from ghost.core.state import ghost_status, ghost_echo
from ghost.utils.ghost_utils import macro_expand, ghost_push


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
  ghost migrate frontmatter
  ghost validate frontmatter
  ghost evaluate
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

        case "migrate":
            if len(args) >= 2 and args[1] == "frontmatter":
                print("🔧 ghost migrate frontmatter — stub invoked.")
                print("TODO: Implement frontmatter migration logic.")
            else:
                print("❗ usage: ghost migrate frontmatter")

        case "validate":
            if len(args) >= 2 and args[1] == "frontmatter":
                print("✅ ghost validate frontmatter — stub invoked.")
                print("TODO: Run frontmatter compliance checks.")
            else:
                print("❗ usage: ghost validate frontmatter [--all]")

        case "evaluate":
            print("📊 ghost evaluate — stub invoked.")
            print("TODO: Implement evaluation of system metrics.")

        case "start":
            from ghost.core.daemon import start_ghostd
            start_ghostd()

        case "stop":
            from ghost.core.daemon import stop_ghostd
            stop_ghostd()

        case "statusd":
            from ghost.core.daemon import status_ghostd
            status_ghostd()

        case "init":
            from ghost.cli.bootstrap import ghost_bootstrap_routine
            ghost_bootstrap_routine("normie")
        
        case "cleanup":
            from ghost.cli.cleanup import main as cleanup_main
            cleanup_main()   
        
        case _:
            print(f"❓ unknown command: {cmd}")
            show_help()