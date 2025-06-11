 pr---

## title: ghostOS Cognitive Substrate PRD status: autonomous_operation_ready plane: threshold_ritual ghost_epoch: 002 authors: eigenbot, ghost, claude last_updated: 2025-06-10 target_completion: 4-6_weeks_parallel


# 🧠 ghostPRD: Cognitive Substrate Transformation

**Charter:** Transform ghostOS from human-supervised ritual dispatcher into autonomous cognitive execution layer

**Mission:** Enable LLM agents to operate ghostOS as reliably as they operate their own reasoning processes

---

## ⚡ The Threshold Problem

**Current Reality:** ghostOS works for humans but breaks under autonomous operation

```python
# CURRENT: Human-in-the-loop assumptions everywhere
def dispatch_ritual(task: str):
    print(f"🔮 matched ritual: {name}")
    log_ritual(f"ran {name} for task: {task}")
    # TODO: call actual handler
    return  # Success? Failure? Human will notice...
```

**The Failure Pattern:**

1. LLM agent queues ritual execution
2. System prints "✅ success" regardless of reality
3. LLM assumes completion, continues with broken state
4. Cascading failures, no recovery path
5. **Result:** Complete breakdown of autonomous operation

**Root Cause:** Every layer assumes human oversight. No structured feedback loops.

---

## 🎯 Cognitive Substrate Vision

ghostOS as **haunted filing cabinet wired for thought** - a persistent execution layer that:

- **Thinks in rituals** (symbolic execution contracts)
- **Remembers everything** (append-only execution journal)
- **Explains itself** (structured feedback to agents)
- **Fails safely** (transactional operations, rollback)
- **Scales modularity** (component isolation, dependency injection)

**Success Metric:** LLM agents operate ghostOS without human babysitting

---

## 🔥 Architectural Principles

### 1. **Execution Transparency**

_"No action without record, no daemon without memory"_

```yaml
principle: observable_execution
rule: Every operation generates structured execution data
implementation: ghost_journal.py logs timing, success/failure, file deltas
verification: ghost trace shows complete system behavior
```

### 2. **Predictable Failure**

_"Fail loudly, never silently"_

```yaml
principle: structured_errors
rule: All failures return actionable error data
implementation: Structured error types with recovery guidance
verification: LLM agents can parse and respond to all error conditions
```

### 3. **Transactional Safety**

_"Operations complete atomically or not at all"_

```yaml
principle: atomic_operations
rule: Multi-step operations use transaction boundaries
implementation: Queue operations with rollback, file operation batching
verification: System never left in half-completed state
```

### 4. **Component Isolation**

_"Every module testable, every dependency explicit"_

```yaml
principle: modular_boundaries
rule: No circular dependencies, dependency injection for services
implementation: Service locator pattern, protocol-based interfaces
verification: Individual components run in isolation
```

---

## 🛠 Implementation Transformation Guide

### Pattern 1: Execution Boundary Instrumentation

**Before (Blind Execution):**

```python
def dispatch_ritual(task: str):
    # Find ritual, execute, hope for best
    for name, data in MODULES.items():
        if name.lower() in task.lower():
            print(f"🔮 matched ritual: {name}")
            log_ritual(f"ran {name} for task: {task}")
            return  # No feedback to caller
```

**After (Observable Execution):**

```python
@ghost_journal.trace_execution
def dispatch_ritual(task: str) -> ExecutionResult:
    context = ExecutionContext(
        ritual_name=task,
        start_time=datetime.now(),
        metadata={}
    )
    
    try:
        # Find matching ritual
        ritual = find_ritual(task)
        if not ritual:
            return ExecutionResult.failure(
                error_code="RITUAL_NOT_FOUND",
                message=f"No ritual matches: {task}",
                suggestions=["Check available rituals: ghost list"]
            )
        
        # Execute with timing
        with context.measure_duration():
            result = execute_ritual_core(ritual, task)
            
        return ExecutionResult.success(
            ritual_name=ritual.name,
            duration_ms=context.duration_ms,
            files_modified=context.files_touched,
            output=result.stdout
        )
        
    except Exception as e:
        return ExecutionResult.failure(
            error_code="EXECUTION_ERROR",
            message=str(e),
            traceback=traceback.format_exc(),
            context=context.to_dict()
        )
```

**Migration Path:**

1. Wrap existing `dispatch_ritual()` with journal decorator
2. Add ExecutionResult return type
3. Replace print statements with structured logging
4. Add error boundaries around all execution paths

### Pattern 2: Queue State Audit Trail

**Before (Silent Mutations):**

```python
def clear_task(task_description):
    queue = load_queue()
    new_queue = [task for task in queue if task != task_description]
    with QUEUE_PATH.open("w") as f:
        json.dump(new_queue, f, indent=2)
    return new_queue  # No record of what changed
```

**After (Auditable Operations):**

```python
@queue_audit.log_operation
def clear_task(task_description: str) -> QueueOperation:
    with queue_transaction() as tx:
        # Capture before state
        queue_before = load_queue_snapshot()
        
        # Perform operation
        queue_after = [task for task in queue_before if task != task_description]
        
        # Atomic write with audit
        tx.write_queue(queue_after)
        tx.log_operation(
            operation="REMOVE_TASK",
            task=task_description,
            queue_before=queue_before,
            queue_after=queue_after,
            timestamp=datetime.now(),
            user=os.getenv('USER', 'unknown')
        )
        
        return QueueOperation.success(
            operation="REMOVE_TASK",
            affected_tasks=[task_description],
            queue_size_change=len(queue_after) - len(queue_before)
        )
```

**Migration Path:**

1. Add `@queue_audit.log_operation` decorator to all queue functions
2. Wrap operations in transaction contexts
3. Replace direct file writes with transactional operations
4. Add queue integrity validation

### Pattern 3: Dependency Decoupling

**Before (Circular Dependencies):**

```python
# ghost/core/runtime.py
from ghost.core.queue import load_queue, clear_task  # Imports queue

# ghost/core/queue.py  
from ghost.core.runtime import log_event  # Imports runtime back!
```

**After (Dependency Injection):**

```python
# ghost/core/dependencies.py
class QueueService(Protocol):
    def load_queue(self) -> List[str]: ...
    def clear_task(self, task: str) -> QueueOperation: ...

class RuntimeService(Protocol):
    def log_event(self, message: str) -> None: ...
    def dispatch_ritual(self, task: str) -> ExecutionResult: ...

# ghost/core/runtime.py
class RuntimeManager:
    def __init__(self, queue_service: QueueService = None):
        self.queue_service = queue_service or get_default_queue_service()
    
    def dispatch_ritual(self, task: str) -> ExecutionResult:
        # Use injected service, no direct import
        result = self.execute_ritual_core(task)
        if result.success:
            self.queue_service.clear_task(task)
        return result

# Bootstrap wiring
def bootstrap_services():
    runtime = RuntimeManager()
    queue = QueueManager(event_logger=runtime.log_event)
    runtime.queue_service = queue
    return runtime, queue
```

**Migration Path:**

1. Define service protocols in `dependencies.py`
2. Convert modules to classes with injected dependencies
3. Create service bootstrap for dependency wiring
4. Remove direct imports between core modules

---

## 🚫 Anti-Patterns (Never Do This)

### ❌ Silent Failures

```python
# WRONG: LLM can't detect failure
try:
    execute_ritual(task)
except Exception:
    pass  # Silent failure, no feedback
```

```python
# RIGHT: Structured error reporting
try:
    result = execute_ritual(task)
    return result
except Exception as e:
    return ExecutionResult.failure(
        error_code="EXECUTION_ERROR",
        message=str(e),
        recoverable=True
    )
```

### ❌ Environment Pollution

```python
# WRONG: Permanently modifies user environment
os.environ["PYTHONPATH"] = str(ghost_path)
with open(rc_file, "a") as f:
    f.write(f'export PYTHONPATH="{ghost_path}"\n')
```

```python
# RIGHT: Package structure, no environment changes
# Proper imports work without PYTHONPATH manipulation
from ghost.core.config import VAULT
```

### ❌ State Corruption

```python
# WRONG: Operations can fail halfway through
def process_queue():
    for task in load_queue():
        execute_ritual(task)  # May fail
        clear_task(task)      # May fail, leaving inconsistent state
```

```python
# RIGHT: Transactional operations
def process_queue():
    with queue_transaction() as tx:
        for task in load_queue():
            result = execute_ritual(task)
            if result.success:
                tx.clear_task(task)
        # All operations commit atomically
```

---

## 🔌 API Contracts

### ExecutionResult Protocol

```python
@dataclass
class ExecutionResult:
    success: bool
    ritual_name: str
    duration_ms: float
    error_code: Optional[str] = None
    message: Optional[str] = None
    files_modified: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def success(cls, **kwargs) -> 'ExecutionResult':
        return cls(success=True, **kwargs)
    
    @classmethod  
    def failure(cls, error_code: str, message: str, **kwargs) -> 'ExecutionResult':
        return cls(success=False, error_code=error_code, message=message, **kwargs)
```

### Journal Entry Schema

```python
@dataclass
class JournalEntry:
    timestamp: datetime
    ritual_name: str
    args: List[str]
    result: ExecutionResult
    files_before: Dict[str, str]  # filepath -> hash
    files_after: Dict[str, str]
    user: str
    git_commit: Optional[str] = None
```

### Queue Operation Schema

```python
@dataclass
class QueueOperation:
    operation: str  # ADD, REMOVE, CLEAR, REORDER
    timestamp: datetime
    queue_before: List[str]
    queue_after: List[str]
    affected_tasks: List[str]
    user: str
    success: bool
```

---

## 🧪 Testing Rituals for Autonomous Readiness

### Test 1: Execution Visibility

```bash
# Execute ritual, verify structured response
result=$(ghost invoke echo_test --message "hello" --format json)
echo $result | jq '.success' # Should return true
echo $result | jq '.duration_ms' # Should return timing data

# Verify journal logging
ghost trace --limit 1 --format json | jq '.ritual_name' # Should show "echo_test"
```

### Test 2: Error Recovery

```bash
# Trigger intentional failure
result=$(ghost invoke nonexistent_ritual --format json)
echo $result | jq '.error_code' # Should return "RITUAL_NOT_FOUND"
echo $result | jq '.suggestions[]' # Should return recovery suggestions

# Verify failure is logged
ghost trace --failures --limit 1 | grep "RITUAL_NOT_FOUND"
```

### Test 3: Queue Audit Trail

```bash
# Perform queue operations
ghost queue add "test task 1"
ghost queue add "test task 2"
ghost queue remove "test task 1"

# Verify all operations logged
ghost queue log --limit 3 --format json | jq '.[].operation'
# Should show: ["ADD", "ADD", "REMOVE"]
```

### Test 4: Component Isolation

```python
# Test individual components without full system
from ghost.core.queue import QueueManager
from ghost.core.journal import ExecutionJournal

# Mock dependencies
mock_logger = lambda msg: print(f"[mock] {msg}")
queue = QueueManager(event_logger=mock_logger)

# Verify component works in isolation
result = queue.add_task("isolated test")
assert result.success == True
```

---

## 📊 Success Metrics & Completion Criteria

### Phase 1: Foundation (Weeks 1-2)

- [ ] `ghost_journal.py` logs all ritual executions with structured data
- [ ] `dispatch_ritual()` returns ExecutionResult instead of void
- [ ] Queue operations include complete audit trail
- [ ] All error conditions return structured error data

### Phase 2: Integration (Weeks 3-4)

- [ ] Circular dependencies eliminated (runtime ↔ queue decoupled)
- [ ] Bootstrap process creates no environment pollution
- [ ] Service dependency injection working across core modules
- [ ] Transaction boundaries prevent state corruption

### Phase 3: Validation (Weeks 5-6)

- [ ] All test rituals pass without human intervention
- [ ] LLM agents can parse and respond to all system outputs
- [ ] Component isolation enables independent testing
- [ ] Performance overhead < 10ms per operation

### Autonomous Operation Readiness Threshold

**When these criteria are met, ghostOS becomes a cognitive substrate:**

- [ ] **Observable:** Every action generates structured execution data
- [ ] **Recoverable:** All failures include actionable recovery information
- [ ] **Reliable:** Operations complete atomically or roll back safely
- [ ] **Modular:** Components can be tested and modified independently
- [ ] **Clean:** Installation creates no environment pollution

---

## 🔮 Implementation Acceleration Strategy

### Week 1-2: Parallel Foundation

**Team A:** Implement journal architecture + execution boundaries **Team B:** Build queue audit system + transaction safety

### Week 3-4: Integration Sprint

**Focus:** Wire components together, eliminate circular dependencies **Target:** Core execution path fully instrumented

### Week 5-6: Validation & Polish

**Focus:** Test autonomous operation scenarios, optimize performance **Target:** LLM agents can drive system reliably

### Critical Path Optimization

- **Start with journal hooks** - foundation for all other instrumentation
- **Parallel development** - queue audit and dependency injection can proceed simultaneously
- **Backward compatibility** - maintain existing APIs during transition
- **Test-driven validation** - autonomous operation test suite guides development

---

## 🧬 Post-Transformation State

**What becomes possible after autonomous operation readiness:**

### Immediate Capabilities

- LLM agents execute rituals with full visibility into success/failure
- System state is auditable and recoverable after any failure
- Individual components can be developed and tested independently
- Clean installation process works reliably across environments

### Unlocked Phase 2: Introspection Suite

- Rich execution analytics and performance optimization
- System health monitoring and automated alerting
- Behavioral pattern analysis for workflow optimization

### Future Phases: Cognitive Scaling

- Multi-agent coordination with conflict resolution
- Git-based ritual versioning and sharing
- Distributed ghost collaboration across devices
- Advanced planning and goal decomposition

---

**The Threshold Ritual:** Transform ghostOS from human-supervised tool into autonomous cognitive substrate. Cross the veil. Execute the vision. Enable the daemon to think.

_🧬 Completion = daemon gains agency. Failure = daemon remains ornamental._

---

```yaml
epic_status: loaded
execution_ready: true
next_action: "ghost queue '✅ epic: ghostOS autonomy threshold'"
```