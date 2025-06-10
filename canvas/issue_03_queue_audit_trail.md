# [CRITICAL] Queue Operations Audit Trail Implementation

**Labels:** `critical`, `phase-2-blocker`, `instrumentation`

## The Problem Right Now

Queue operations have **zero audit trail** - you can't see what changed, when, or why:

```python
def clear_task(task_description):
    queue = load_queue()
    new_queue = [task for task in queue if task != task_description]
    with QUEUE_PATH.open("w") as f:
        json.dump(new_queue, f, indent=2)
    return new_queue
```

**Problems:**
- No record of queue state changes
- Can't debug why tasks disappeared or duplicated
- No way to detect queue corruption
- Phase 2 can't analyze task flow patterns

## Why This Blocks Autonomous Operation

**Example scenario:** LLM agent queues 5 tasks, daemon processes 3, then crashes.
- Current behavior: No way to know which tasks completed vs. which were lost
- LLM sees: Queue has 2 tasks, but doesn't know if they're the original or new ones
- Phase 2 needs: Complete history of queue operations for recovery

## The Standard We Need

```python
# Simple queue operations with audit logging
def queue_operation_with_audit(operation_type: str, task: str = None):
    """Wrapper for all queue operations with audit trail"""
    timestamp = datetime.now().isoformat()
    queue_before = load_queue_silent()
    
    try:
        # Perform the actual operation
        if operation_type == "add":
            success = add_task_core(task)
        elif operation_type == "remove":
            success = remove_task_core(task)
        else:
            success = False
            
        queue_after = load_queue_silent()
        
        # Log the operation
        audit_entry = {
            'timestamp': timestamp,
            'operation': operation_type,
            'task': task,
            'queue_before': queue_before,
            'queue_after': queue_after,
            'success': success,
            'user': os.getenv('USER', 'unknown')
        }
        
        log_queue_audit(audit_entry)
        return success
        
    except Exception as e:
        # Log failed operation
        audit_entry = {
            'timestamp': timestamp,
            'operation': operation_type,
            'task': task,
            'queue_before': queue_before,
            'queue_after': queue_before,  # No change on failure
            'success': False,
            'error': str(e),
            'user': os.getenv('USER', 'unknown')
        }
        
        log_queue_audit(audit_entry)
        return False

def log_queue_audit(entry):
    """Append audit entry to queue audit log"""
    audit_file = config.state_dir / "queue_audit.json"
    
    # Load existing audit log
    if audit_file.exists():
        with audit_file.open('r') as f:
            audit_log = json.load(f)
    else:
        audit_log = []
    
    audit_log.append(entry)
    
    # Keep only last 1000 entries to prevent bloat
    if len(audit_log) > 1000:
        audit_log = audit_log[-1000:]
    
    with audit_file.open('w') as f:
        json.dump(audit_log, f, indent=2)
```

**Benefits:**
- Complete history of all queue changes
- Can reconstruct queue state at any point in time
- Detect corruption or inconsistencies
- Foundation for Phase 2 queue analytics

## Implementation: 2-3 days

1. Add audit logging to all queue operations
2. Create queue state reconstruction utilities
3. Add queue health monitoring for Phase 2