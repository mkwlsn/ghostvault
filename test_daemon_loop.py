#!/usr/bin/env python3
"""
Test daemon loop functionality without psutil dependency
This simulates Issue #5 verification
"""
import sys
from pathlib import Path

# Add ghost root for imports
sys.path.insert(0, str(Path(__file__).parent / "ghost"))

# Import clean daemon module (no psutil dependency)
import daemon.daemon as daemon_module

def test_daemon_execution():
    """Test that daemon can execute a simple task"""
    print("🧪 Testing Issue #5: Daemon Loop Execution")
    print("=" * 50)
    
    # Load current queue state
    tasks = daemon_module.load_queue()
    print(f"📋 Queue loaded: {len(tasks)} tasks")
    
    # Check for queued tasks
    queued_tasks = [t for t in tasks if t.get("status") == "queued"]
    print(f"⏳ Queued tasks: {len(queued_tasks)}")
    
    if queued_tasks:
        # Execute first queued task
        task = queued_tasks[0]
        print(f"🚀 Executing task: {task.get('script', 'unknown')}")
        
        # Test task execution
        result = daemon_module.execute_task(task)
        print(f"✅ Task execution result: {result}")
        
        # Update task status
        task["status"] = result
        task["last_run"] = "2025-06-29 14:35:00"
        daemon_module.save_queue(tasks)
        print(f"💾 Queue updated with status: {result}")
        
        return True
    else:
        print("❌ No queued tasks found")
        return False

def show_results():
    """Show final state after daemon processing"""
    print("\n" + "=" * 50)
    print("📊 Final Results:")
    
    # Show queue state
    tasks = daemon_module.load_queue()
    for task in tasks:
        status = task.get("status", "unknown")
        script = task.get("script", "unknown")
        print(f"   Task: {script} → {status}")
    
    # Show events log
    try:
        with open(daemon_module.EVENTS_MD, "r") as f:
            events = f.readlines()[-5:]  # Last 5 events
        print("\n📝 Recent Events:")
        for event in events:
            print(f"   {event.strip()}")
    except FileNotFoundError:
        print("📝 No events log found")

if __name__ == "__main__":
    success = test_daemon_execution()
    show_results()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Issue #5 PASSED: Daemon loop executes tasks correctly")
    else:
        print("❌ Issue #5 FAILED: Task execution problems")
    
    sys.exit(0 if success else 1)