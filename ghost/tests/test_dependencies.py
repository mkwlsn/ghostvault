#!/usr/bin/env python3
"""
Test Issue #4: Dependency resolution
Observable before/after state verification
"""
import sys
from pathlib import Path

# Add ghost root for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_config_import():
    """Verify config module imports correctly"""
    try:
        from config.config import VAULT, DAEMON_PID, QUEUE_JSON, EVENTS_MD
        print("✅ Config import successful")
        print(f"   VAULT: {VAULT}")
        print(f"   DAEMON_PID: {DAEMON_PID}")
        print(f"   QUEUE_JSON: {QUEUE_JSON}")
        return True
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        return False

def test_daemon_import():
    """Verify daemon module handles psutil gracefully"""
    try:
        from daemon import daemon
        print("✅ Daemon import successful")
        print(f"   PSUTIL_AVAILABLE: {daemon.PSUTIL_AVAILABLE}")
        
        if not daemon.PSUTIL_AVAILABLE:
            print("   💡 Daemon correctly detects missing psutil dependency")
        
        return True
    except ImportError as e:
        print(f"❌ Daemon import failed: {e}")
        return False

def main():
    print("🧪 Testing Issue #4: Dependency Resolution")
    print("=" * 50)
    
    config_ok = test_config_import()
    daemon_ok = test_daemon_import()
    
    print("=" * 50)
    if config_ok and daemon_ok:
        print("✅ Issue #4 PASSED: Dependencies resolved correctly")
        return True
    else:
        print("❌ Issue #4 FAILED: Dependency issues remain")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)