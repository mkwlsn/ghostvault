"""
ghostOS-kernel daemon
Minimal task execution loop for Issue #5
"""
import sys
import time
import json
import subprocess
from pathlib import Path

# Check psutil dependency - graceful failure
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    print("❌ Error: psutil dependency missing")
    print("💡 Install with: pip install psutil")
    PSUTIL_AVAILABLE = False

# Import kernel config
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from config.config import DAEMON_PID, QUEUE_JSON, EVENTS_MD
except ImportError as e:
    print(f"❌ Error importing config: {e}")
    sys.exit(1)

def log_event(message):
    """Log event to events.md with timestamp"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(EVENTS_MD, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def load_queue():
    """Load tasks from queue.json"""
    try:
        with open(QUEUE_JSON, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_queue(tasks):
    """Save tasks to queue.json atomically"""
    temp_file = QUEUE_JSON.with_suffix(".tmp")
    with open(temp_file, "w") as f:
        json.dump(tasks, f, indent=2)
    temp_file.rename(QUEUE_JSON)

def execute_task(task):
    """Execute a single task via subprocess"""
    task_id = task.get("id", "unknown")
    script = task.get("script", "")
    
    log_event(f"task_id:{task_id} status:running script:{script}")
    
    try:
        # Execute script with timeout and capture output
        result = subprocess.run(
            script,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            log_event(f"task_id:{task_id} status:done returncode:0")
            return "done"
        else:
            # Truncate stderr if too long
            stderr = result.stderr[:500] if result.stderr else "no error output"
            log_event(f"task_id:{task_id} status:failed returncode:{result.returncode} stderr:{stderr}")
            return "failed"
            
    except subprocess.TimeoutExpired:
        log_event(f"task_id:{task_id} status:timeout after:300s")
        return "timeout"
    except subprocess.CalledProcessError as e:
        stderr = str(e)[:500]
        log_event(f"task_id:{task_id} status:failed error:{stderr}")
        return "failed"
    except Exception as e:
        error = str(e)[:500]
        log_event(f"task_id:{task_id} status:error exception:{error}")
        return "failed"

def daemon_loop():
    """Core daemon loop - scans queue and executes tasks"""
    log_event("daemon status:started scanning_interval:5s")
    print("[daemon] scanning queue every 5 seconds...")
    
    try:
        while True:
            tasks = load_queue()
            
            # Process tasks with status "queued"
            updated = False
            for task in tasks:
                if task.get("status") == "queued":
                    print(f"[daemon] executing task: {task.get('script', 'unknown')}")
                    
                    # Update status to running
                    task["status"] = "running"
                    save_queue(tasks)
                    
                    # Execute and update final status
                    final_status = execute_task(task)
                    task["status"] = final_status
                    task["last_run"] = time.strftime("%Y-%m-%d %H:%M:%S")
                    updated = True
            
            if updated:
                save_queue(tasks)
                
            time.sleep(5)
            
    except KeyboardInterrupt:
        log_event("daemon status:stopped reason:keyboard_interrupt")
        print("[daemon] stopped by user")
    except Exception as e:
        log_event(f"daemon status:crashed error:{str(e)[:500]}")
        print(f"[daemon] crashed: {e}")
        raise

def main():
    """Entry point for daemon execution"""
    if not PSUTIL_AVAILABLE:
        print("❌ Cannot start daemon without psutil dependency")
        sys.exit(1)
        
    daemon_loop()

if __name__ == "__main__":
    main()