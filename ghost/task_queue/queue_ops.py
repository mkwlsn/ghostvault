"""
Atomic queue operations for ghostOS-kernel
Implements tmp-file pattern for safe concurrent access
"""

import json
import os
import time
import fcntl
from typing import List, Dict, Any, Optional
from datetime import datetime

def get_queue_path() -> str:
    """Get path to queue.json file"""
    return os.path.join(os.path.dirname(__file__), 'queue.json')

def get_temp_path() -> str:
    """Get path for temporary queue operations"""
    return get_queue_path() + '.tmp'

def load_queue() -> List[Dict[str, Any]]:
    """Load queue with file locking"""
    queue_path = get_queue_path()
    
    if not os.path.exists(queue_path):
        return []
    
    with open(queue_path, 'r') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_SH)
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_queue(tasks: List[Dict[str, Any]]) -> None:
    """Save queue atomically using tmp-file pattern"""
    queue_path = get_queue_path()
    temp_path = get_temp_path()
    
    # Write to temp file first
    with open(temp_path, 'w') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        json.dump(tasks, f, indent=2)
    
    # Atomic move
    os.rename(temp_path, queue_path)

def add_task(task_id: str, script: str) -> bool:
    """Add new task to queue"""
    tasks = load_queue()
    
    # Check for duplicate ID
    if any(task['id'] == task_id for task in tasks):
        return False
    
    new_task = {
        'id': task_id,
        'script': script,
        'status': 'queued',
        'created': datetime.now().isoformat()
    }
    
    tasks.append(new_task)
    save_queue(tasks)
    return True

def update_task_status(task_id: str, status: str, **kwargs) -> bool:
    """Update task status atomically"""
    valid_statuses = {'queued', 'running', 'done', 'failed', 'timeout'}
    if status not in valid_statuses:
        return False
    
    tasks = load_queue()
    
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = status
            task['last_run'] = datetime.now().isoformat()
            
            # Add optional fields
            for key, value in kwargs.items():
                if key in ['exit_code', 'output']:
                    task[key] = value
            
            save_queue(tasks)
            return True
    
    return False

def get_queued_tasks() -> List[Dict[str, Any]]:
    """Get all tasks with status 'queued'"""
    tasks = load_queue()
    return [task for task in tasks if task['status'] == 'queued']

def cleanup_completed_tasks(max_age_hours: int = 24) -> int:
    """Remove old completed tasks, return count removed"""
    tasks = load_queue()
    cutoff = datetime.now().timestamp() - (max_age_hours * 3600)
    
    original_count = len(tasks)
    tasks = [
        task for task in tasks
        if not (task['status'] in ['done', 'failed'] and 
                datetime.fromisoformat(task.get('last_run', task['created'])).timestamp() < cutoff)
    ]
    
    if len(tasks) != original_count:
        save_queue(tasks)
    
    return original_count - len(tasks)