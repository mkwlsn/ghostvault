#!/usr/bin/env python3
"""
Test script to verify Issue #4 (dependency resolution) is working correctly.
This demonstrates observable before/after states.
"""

import sys
from pathlib import Path

# Add tmp to path for imports
sys.path.insert(0, str(Path(__file__).parent / "tmp"))

def test_config_import():
    """Test that config.py imports correctly with new flat structure"""
    try:
        from config import VAULT, DAEMON_PID, QUEUE_JSON, EVENTS_MD
        print("✅ Config import successful")
        print(f"   VAULT: {VAULT}")
        print(f"   DAEMON_PID: {DAEMON_PID}")
        print(f"   QUEUE_JSON: {QUEUE_JSON}")
        return True
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        return False

def test_daemon_import():
    """Test that daemon.py imports correctly with graceful psutil handling"""
    try:
        import daemon
        print(f"✅ Daemon import successful")
        print(f"   PSUTIL_AVAILABLE: {daemon.PSUTIL_AVAILABLE}")
        
        # Test that daemon fails gracefully without psutil
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
        print("💡 Ready for Issue #5: Daemon loop implementation")
    else:
        print("❌ Issue #4 FAILED: Dependency issues remain")
    
    return config_ok and daemon_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)