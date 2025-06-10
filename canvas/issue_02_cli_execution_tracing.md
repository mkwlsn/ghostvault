# [CRITICAL] CLI Command Execution Tracing Infrastructure

**Labels:** `critical`, `phase-2-blocker`, `instrumentation`, `cli`, `technical-debt`

## Problem Statement

The CLI system in `ghost/cli/cli.py` lacks execution tracing infrastructure, making it impossible to monitor command performance, debug issues, or provide meaningful introspection data for Phase 2 development.

## Current State Analysis

```python
def main():
    args = sys.argv[1:]
    if not args:
        show_help()
        sys.exit(0)

    cmd = args[0]

    match cmd:
        case "new":
            if len(args) >= 3 and args[1] == "module":
                new_module(args[2])
            else:
                print("❗ usage: ghost new module <name>")
        case "log":
            if len(args) >= 2:
                log_event(macro_expand(" ".join(args[1:])))
            else:
                print("❗ usage: ghost log \"<msg>\"")
        # ... more cases
```

### Issues Identified:

1. **No command execution timing** - Cannot measure CLI performance
2. **No execution context tracking** - Missing user, environment, argument metadata
3. **No error boundaries** - CLI failures are not systematically captured
4. **No audit trail** - Cannot track what commands were executed when
5. **No introspection hooks** - Phase 2 cannot inject monitoring code
6. **No structured logging** - Print statements provide poor debugging data

## Impact on Phase 2

The introspection suite requires:
- **Command execution metrics** for performance analysis
- **User behavior tracking** for usage patterns
- **Error rate monitoring** for reliability assessment
- **Execution context** for debugging support

Without CLI tracing, Phase 2 cannot provide insights into ghost system usage.

## Proposed Solution

### 1. Create CLI Instrumentation Framework

```python
# ghost/cli/instrumentation.py
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
import time
import os
import sys
import traceback

@dataclass
class CLIExecutionContext:
    command: str
    args: List[str]
    user: str = field(default_factory=lambda: os.getenv('USER', 'unknown'))
    cwd: str = field(default_factory=os.getcwd)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    duration_ms: Optional[float] = None
    exit_code: int = 0
    success: bool = True
    error: Optional[str] = None
    output_lines: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

class CLITracer:
    def __init__(self):
        self.contexts = []
        self.hooks = {
            'pre_command': [],
            'post_command': [],
            'on_error': [],
            'on_output': []
        }
        self.enabled = True
    
    def register_hook(self, event: str, callback):
        if event in self.hooks:
            self.hooks[event].append(callback)
    
    def start_command(self, command: str, args: List[str]) -> CLIExecutionContext:
        if not self.enabled:
            return None
            
        context = CLIExecutionContext(command=command, args=args)
        
        # Add environment metadata
        context.metadata.update({
            'python_version': sys.version,
            'platform': sys.platform,
            'ghost_version': self._get_ghost_version(),
            'virtual_env': os.getenv('VIRTUAL_ENV'),
            'path_length': len(os.getenv('PATH', '').split(':')),
        })
        
        self.contexts.append(context)
        
        # Execute pre-command hooks
        for hook in self.hooks['pre_command']:
            try:
                hook(context)
            except Exception as e:
                print(f"⚠️ Hook error: {e}")
        
        return context
    
    def finish_command(self, context: CLIExecutionContext, exit_code: int = 0, error: str = None):
        if not context:
            return
            
        context.end_time = datetime.now()
        context.duration_ms = (context.end_time - context.start_time).total_seconds() * 1000
        context.exit_code = exit_code
        context.success = exit_code == 0 and error is None
        context.error = error
        
        # Execute post-command hooks
        for hook in self.hooks['post_command']:
            try:
                hook(context)
            except Exception as e:
                print(f"⚠️ Hook error: {e}")
    
    def capture_output(self, context: CLIExecutionContext, line: str):
        if context:
            context.output_lines.append(line)
            
            # Execute output hooks
            for hook in self.hooks['on_output']:
                try:
                    hook(context, line)
                except Exception as e:
                    print(f"⚠️ Hook error: {e}")
    
    def _get_ghost_version(self):
        # Attempt to get version from git or package info
        try:
            import subprocess
            result = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], 
                                  capture_output=True, text=True, cwd=os.getcwd())
            if result.returncode == 0:
                return f"git-{result.stdout.strip()}"
        except:
            pass
        return "unknown"

# Global CLI tracer
cli_tracer = CLITracer()
```

### 2. Enhanced CLI Main Function

```python
# Modified ghost/cli/cli.py
import sys
from ghost.cli.instrumentation import cli_tracer, CLIExecutionContext
from ghost.core.runtime import log_event, queue_task, log_ritual
from ghost.module.modules import new_module, ghost_sync_modules, ghost_gen_prompt
from ghost.core.state import ghost_status, ghost_echo
from ghost.utils.ghost_utils import macro_expand, ghost_push

def traced_print(context: CLIExecutionContext, message: str):
    """Enhanced print that captures output for tracing"""
    print(message)
    if context:
        cli_tracer.capture_output(context, message)

def main():
    args = sys.argv[1:]
    context = None
    
    try:
        # Start command tracing
        command = args[0] if args else "help"
        context = cli_tracer.start_command(command, args)
        
        if not args:
            show_help_traced(context)
            cli_tracer.finish_command(context, 0)
            sys.exit(0)

        cmd = args[0]

        match cmd:
            case "new":
                if len(args) >= 3 and args[1] == "module":
                    result = new_module_traced(args[2], context)
                    cli_tracer.finish_command(context, 0 if result else 1)
                else:
                    traced_print(context, "❗ usage: ghost new module <name>")
                    cli_tracer.finish_command(context, 1)

            case "log":
                if len(args) >= 2:
                    log_event_traced(macro_expand(" ".join(args[1:])), context)
                    cli_tracer.finish_command(context, 0)
                else:
                    traced_print(context, "❗ usage: ghost log \"<msg>\"")
                    cli_tracer.finish_command(context, 1)

            case "queue":
                if len(args) >= 2:
                    queue_task_traced(macro_expand(" ".join(args[1:])), context)
                    cli_tracer.finish_command(context, 0)
                else:
                    traced_print(context, "❗ usage: ghost queue \"<task>\"")
                    cli_tracer.finish_command(context, 1)

            case "ritual":
                if len(args) >= 2:
                    log_ritual_traced(macro_expand(" ".join(args[1:])), context)
                    cli_tracer.finish_command(context, 0)
                else:
                    traced_print(context, "❗ usage: ghost ritual \"<summary>\"")
                    cli_tracer.finish_command(context, 1)

            case "status":
                ghost_status_traced(context)
                cli_tracer.finish_command(context, 0)

            case "echo":
                ghost_echo_traced(context)
                cli_tracer.finish_command(context, 0)

            case _:
                traced_print(context, f"❓ unknown command: {cmd}")
                show_help_traced(context)
                cli_tracer.finish_command(context, 1)
                
    except Exception as e:
        error_msg = f"CLI execution failed: {str(e)}"
        if context:
            context.metadata['traceback'] = traceback.format_exc()
            cli_tracer.finish_command(context, 1, error_msg)
        
        print(f"❌ {error_msg}")
        sys.exit(1)

# Traced wrapper functions
def new_module_traced(name: str, context: CLIExecutionContext) -> bool:
    try:
        new_module(name)
        traced_print(context, f"✅ module '{name}' created")
        return True
    except Exception as e:
        traced_print(context, f"❌ failed to create module '{name}': {e}")
        return False

def log_event_traced(message: str, context: CLIExecutionContext):
    try:
        log_event(message)
        traced_print(context, f"📝 log saved: {message}")
    except Exception as e:
        traced_print(context, f"❌ failed to log event: {e}")
        raise

def queue_task_traced(task: str, context: CLIExecutionContext):
    try:
        queue_task(task)
        traced_print(context, f"📋 task queued: {task}")
    except Exception as e:
        traced_print(context, f"❌ failed to queue task: {e}")
        raise

def log_ritual_traced(summary: str, context: CLIExecutionContext):
    try:
        log_ritual(summary)
        traced_print(context, f"📿 ritual logged")
    except Exception as e:
        traced_print(context, f"❌ failed to log ritual: {e}")
        raise

def ghost_status_traced(context: CLIExecutionContext):
    try:
        # Capture status output
        import io
        import contextlib
        
        output_buffer = io.StringIO()
        with contextlib.redirect_stdout(output_buffer):
            ghost_status()
        
        output = output_buffer.getvalue()
        for line in output.split('\n'):
            if line.strip():
                traced_print(context, line)
                
    except Exception as e:
        traced_print(context, f"❌ failed to get status: {e}")
        raise

def ghost_echo_traced(context: CLIExecutionContext):
    try:
        # Similar to status but for echo
        import io
        import contextlib
        
        output_buffer = io.StringIO()
        with contextlib.redirect_stdout(output_buffer):
            ghost_echo()
        
        output = output_buffer.getvalue()
        for line in output.split('\n'):
            if line.strip():
                traced_print(context, line)
                
    except Exception as e:
        traced_print(context, f"❌ failed to echo: {e}")
        raise

def show_help_traced(context: CLIExecutionContext):
    help_text = """ghost — local ghost CLI

usage:        
  ghost new module <name>
  ghost gen prompt <module_name>        
  ghost log "<msg>"
  ghost queue "<task>"
  ghost ritual "<summary>"
  ghost push [--message "<msg>"]
  ghost status
  ghost echo
  ghost start
  ghost stop
  ghost statusd
  ghost sync modules
"""
    for line in help_text.strip().split('\n'):
        traced_print(context, line)
```

### 3. Phase 2 CLI Analytics Integration

```python
# ghost/cli/analytics.py
from ghost.cli.instrumentation import cli_tracer
from collections import defaultdict, Counter
from datetime import datetime, timedelta
import json

class CLIAnalytics:
    def __init__(self):
        self.command_stats = defaultdict(list)
        self.error_patterns = Counter()
        self.usage_patterns = []
        
        # Register hooks for data collection
        cli_tracer.register_hook('post_command', self._collect_command_data)
        cli_tracer.register_hook('on_error', self._collect_error_data)
    
    def _collect_command_data(self, context):
        self.command_stats[context.command].append({
            'timestamp': context.start_time,
            'duration_ms': context.duration_ms,
            'success': context.success,
            'args_count': len(context.args),
            'user': context.user
        })
    
    def _collect_error_data(self, context, error):
        self.error_patterns[context.command] += 1
    
    def get_usage_summary(self, hours: int = 24):
        """Get usage summary for the last N hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        
        recent_commands = []
        for command, executions in self.command_stats.items():
            recent = [e for e in executions if e['timestamp'] > cutoff]
            if recent:
                recent_commands.extend(recent)
        
        return {
            'total_commands': len(recent_commands),
            'unique_commands': len(set(e['command'] for e in recent_commands)),
            'avg_duration_ms': sum(e['duration_ms'] for e in recent_commands) / len(recent_commands) if recent_commands else 0,
            'success_rate': sum(1 for e in recent_commands if e['success']) / len(recent_commands) if recent_commands else 0,
            'most_used': Counter(e['command'] for e in recent_commands).most_common(5)
        }
    
    def export_trace_data(self):
        """Export all trace data for external analysis"""
        return {
            'command_stats': dict(self.command_stats),
            'error_patterns': dict(self.error_patterns),
            'export_timestamp': datetime.now().isoformat()
        }
```

## Implementation Plan

### Phase 1: Instrumentation Framework (1-2 days)
1. Create `ghost/cli/instrumentation.py`
2. Implement CLIExecutionContext and CLITracer classes
3. Add configuration options for enabling/disabling tracing

### Phase 2: CLI Integration (2-3 days)
1. Refactor `ghost/cli/cli.py` to use instrumentation
2. Create traced wrapper functions for all commands
3. Add error boundary handling

### Phase 3: Analytics Integration (1-2 days)
1. Create `ghost/cli/analytics.py`
2. Implement data collection and analysis
3. Add export capabilities for Phase 2 suite

## Acceptance Criteria

- [ ] All CLI commands are automatically traced with execution timing
- [ ] Command arguments, user context, and environment metadata are captured
- [ ] Error boundaries capture and log all CLI failures with full context
- [ ] Output capture allows replay of command execution for debugging
- [ ] Hook system enables Phase 2 introspection suite integration
- [ ] Analytics provide insights into usage patterns and performance
- [ ] Tracing can be disabled for production use if needed
- [ ] Unit tests achieve 90%+ coverage for instrumentation code

## Files to Modify

- `ghost/cli/cli.py` - Enhanced main function with tracing
- `ghost/cli/instrumentation.py` - New CLI instrumentation framework
- `ghost/cli/analytics.py` - New CLI analytics capabilities
- `ghost/tests/test_cli.py` - Unit tests for CLI instrumentation

## Dependencies

- No external dependencies required
- Uses only Python standard library

## Risks

- **Performance impact** - Tracing adds overhead to command execution
- **Storage usage** - Long-running systems may accumulate large trace files
- **Privacy concerns** - Command arguments may contain sensitive data

## Mitigation Strategies

- **Configurable tracing** - Allow users to disable or limit tracing scope
- **Data retention policies** - Automatic cleanup of old trace data
- **Argument sanitization** - Filter sensitive data from traces
- **Asynchronous logging** - Don't block command execution for data collection