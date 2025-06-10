#!/usr/bin/env python3
"""
GhostOS CLI Entry Point
Delegates to ghost.cli.ghost for actual CLI functionality
"""

import sys
from pathlib import Path

# Add ghost package to path
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    from ghost.cli.cli import main
    main()
