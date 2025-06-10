#!/usr/bin/env python3

import sys
from pathlib import Path

args = sys.argv[1:]
command = args[0] if args else None

try:
    from ghost_cli import main
except ModuleNotFoundError:
    if command in {"install", "init"}:
        from ghost_bootstrap import bootstrap_main as main
    else:
        print("❗ system modules unavailable — run `ghost init` to configure your environment.")
        exit(1)

if __name__ == "__main__":
    main()
