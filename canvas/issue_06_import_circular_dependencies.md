# [HIGH] Import System Circular Dependency Resolution

**Labels:** `high`, `code-quality`, `imports`, `reliability`

## The Problem Right Now

The import system has **circular dependency risks** that cause mysterious failures and make testing impossible:

```python
# ghost/core/runtime.py
from ghost.core.queue import load_queue, clear_task  # Imports queue module

def dispatch_ritual(task: str):
    from ghost.core.registry import MODULES  # Late import inside function
    # ... ritual logic

# ghost/core/queue.py
from ghost.core.runtime import log_event  # Imports runtime module back!

def clear_task(task):
    # ... queue logic
    log_event(f"cleared task: {task}")  # Runtime dependency
```

**Problems:**
- Runtime imports queue, queue imports runtime (circular)
- Late imports scattered everywhere make dependencies unclear
- Import failures happen randomly during module initialization
- Testing becomes impossible with tight coupling

## Why This Breaks Autonomous Operation

**Example scenario:** LLM agent tries to import the queue module for testing.
- `import ghost.core.queue` loads queue.py
- queue.py imports `log_event` from runtime.py
- runtime.py imports functions from queue.py
- Python import system deadlocks or fails randomly

**Result:** LLM can't reliably test or introspect individual components.

## The Standard We Need

```python
# Clear dependency hierarchy with injection
# Level 0: Configuration (no dependencies)
# Level 1: Core services (config only)  
# Level 2: Business logic (services only)
# Level 3: Interface (business logic only)

# ghost/core/queue.py - Level 1 (no runtime dependency)
class QueueManager:
    def __init__(self, event_logger=None):
        self.event_logger = event_logger or self._default_logger
    
    def _default_logger(self, message):
        print(f"[queue] {message}")  # No import needed
    
    def clear_task(self, task):
        # ... queue logic
        self.event_logger(f"cleared task: {task}")  # Injected dependency

# ghost/core/runtime.py - Level 2 (uses queue service)
class RuntimeManager:
    def __init__(self, queue_service=None):
        self.queue_service = queue_service or self._get_default_queue()
    
    def _get_default_queue(self):
        from ghost.core.queue import QueueManager
        return QueueManager(event_logger=self.log_event)
    
    def dispatch_ritual(self, task: str):
        # No late imports needed
        if self.queue_service:
            self.queue_service.clear_task(task)

# Wire dependencies at startup
def bootstrap_services():
    runtime = RuntimeManager()
    queue = QueueManager(event_logger=runtime.log_event)
    runtime.queue_service = queue
    return runtime, queue
```

**Benefits:**
- No circular imports possible
- Clear dependency hierarchy
- Easy to test individual components
- Predictable initialization order

## Implementation: 3-4 days

1. Map current circular dependencies
2. Create dependency injection framework
3. Refactor modules to use service injection
4. Add comprehensive import tests