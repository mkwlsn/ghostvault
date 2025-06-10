# [CRITICAL] dispatch_ritual() Execution Boundary Instrumentation

**Labels:** `critical`, `phase-2-blocker`, `instrumentation`

## The Problem Right Now

The core ritual execution function has **zero visibility** into what actually happens during execution:

```python
def dispatch_ritual(task: str):
    from ghost.core.registry import MODULES
    for name, data in MODULES.items():
        if name.lower() in task.lower():
            print(f"🔮 matched ritual: {name}")
            log_ritual(f"ran {name} for task: {task}")
            # TODO: call actual handler or parse md steps
            return
    print(f"⚠️ no matching ritual found for: {task}")
    log_event(f"unmatched ritual: {task}")
```

**Problems:**
- LLM agents can't see execution timing or success/failure
- No error boundaries - exceptions kill the daemon  
- No hooks for monitoring or debugging
- Phase 2 introspection suite has nothing to introspect

## Why This Blocks Autonomous Operation

**Example scenario:** LLM queues a ritual that takes 30 seconds to run.
- Current behavior: Function returns immediately (fake execution)
- LLM sees: Instant success, assumes ritual completed
- Reality: Nothing actually happened, but LLM continues with broken assumptions

## The Standard We Need

```python
# Simple execution wrapper with timing and error capture
def dispatch_ritual(task: str) -> bool:
    start_time = time.perf_counter()
    matched_ritual = None
    
    try:
        # Find matching ritual
        for name, data in MODULES.items():
            if name.lower() in task.lower():
                matched_ritual = name
                break
        
        if not matched_ritual:
            log_event(f"unmatched ritual: {task}")
            return False
        
        print(f"🔮 executing ritual: {matched_ritual}")
        
        # Execute with timing (TODO: replace with actual execution)
        success = execute_ritual_core(matched_ritual, task)
        
        duration_ms = (time.perf_counter() - start_time) * 1000
        
        if success:
            log_ritual(f"completed {matched_ritual} in {duration_ms:.1f}ms")
            return True
        else:
            log_event(f"ritual failed: {matched_ritual}")
            return False
            
    except Exception as e:
        duration_ms = (time.perf_counter() - start_time) * 1000
        log_event(f"ritual error: {matched_ritual or 'unknown'} - {str(e)} (after {duration_ms:.1f}ms)")
        return False
```

**Benefits:**
- LLM gets clear success/failure signals
- Execution timing enables performance optimization
- Error boundaries prevent daemon crashes
- Foundation for Phase 2 monitoring hooks

## Implementation: 2-3 days

1. Add execution timing and error boundaries
2. Create structured logging for ritual operations  
3. Add hooks for Phase 2 instrumentation framework