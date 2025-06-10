# [CRITICAL] Daemon Loop Performance Monitoring

**Labels:** `critical`, `phase-2-blocker`, `instrumentation`

## The Problem Right Now

The daemon runs **completely blind** - no performance data, health monitoring, or error tracking:

```python
def ghostd_loop(poll_interval=10):
    print("👻 ghostd running — watching queue...")
    while True:
        queue = load_queue()
        for task in queue:
            print(f"🔁 running ritual for: {task}")
            dispatch_ritual(task)
            clear_task(task)
        time.sleep(poll_interval)
```

**Problems:**
- No way to tell if daemon is healthy or struggling
- Can't measure processing performance
- No graceful shutdown handling
- Phase 2 can't monitor system health

## Why This Blocks Autonomous Operation

**Example scenario:** Daemon starts processing a corrupted queue with 1000 duplicate tasks.
- Current behavior: Runs forever, no indication of the problem
- LLM sees: System appears healthy, but nothing actually works
- Phase 2 needs: Real-time health metrics and performance data

## The Standard We Need

```python
# Enhanced daemon loop with health monitoring
def ghostd_loop(poll_interval=10):
    print("👻 ghostd running with monitoring...")
    
    # Health tracking
    start_time = time.time()
    iteration_count = 0
    total_tasks_processed = 0
    consecutive_errors = 0
    
    while not should_shutdown():
        iteration_start = time.perf_counter()
        iteration_count += 1
        
        try:
            queue = load_queue()
            tasks_this_iteration = 0
            
            if queue:
                print(f"🔄 Processing {len(queue)} tasks...")
                
                for task in queue:
                    try:
                        print(f"🔁 running ritual for: {task}")
                        success = dispatch_ritual(task)
                        
                        if success:
                            clear_task(task)
                            tasks_this_iteration += 1
                            total_tasks_processed += 1
                        else:
                            print(f"❌ ritual failed: {task}")
                            
                    except Exception as e:
                        print(f"💥 task error: {task} - {e}")
                        consecutive_errors += 1
                        
                        # Clear problematic task to prevent infinite loops
                        clear_task(task)
                        
                consecutive_errors = 0  # Reset on successful iteration
            
            # Log health metrics periodically
            iteration_time = time.perf_counter() - iteration_start
            
            if iteration_count % 50 == 0:  # Every 50 iterations
                uptime_hours = (time.time() - start_time) / 3600
                tasks_per_hour = total_tasks_processed / max(uptime_hours, 0.01)
                
                print(f"📊 Health: {iteration_time*1000:.1f}ms/iter, "
                      f"{tasks_per_hour:.1f} tasks/hr, "
                      f"{consecutive_errors} errors")
                
                # Log to health file for Phase 2
                log_daemon_health({
                    'timestamp': datetime.now().isoformat(),
                    'uptime_hours': uptime_hours,
                    'total_iterations': iteration_count,
                    'total_tasks_processed': total_tasks_processed,
                    'avg_iteration_time_ms': iteration_time * 1000,
                    'consecutive_errors': consecutive_errors
                })
            
        except KeyboardInterrupt:
            print("\n👻 Received shutdown signal")
            break
        except Exception as e:
            consecutive_errors += 1
            print(f"💥 Critical daemon error: {e}")
            
            if consecutive_errors > 10:
                print("🚨 Too many consecutive errors, shutting down")
                break
        
        time.sleep(poll_interval)
    
    print("👻 Daemon shutdown complete")

def log_daemon_health(health_data):
    """Log daemon health metrics for Phase 2 monitoring"""
    health_file = config.state_dir / "daemon_health.json"
    
    # Load existing health log
    if health_file.exists():
        with health_file.open('r') as f:
            health_log = json.load(f)
    else:
        health_log = []
    
    health_log.append(health_data)
    
    # Keep only last 100 entries
    if len(health_log) > 100:
        health_log = health_log[-100:]
    
    with health_file.open('w') as f:
        json.dump(health_log, f, indent=2)

def should_shutdown():
    """Check for graceful shutdown signals"""
    shutdown_file = config.state_dir / "daemon_shutdown"
    return shutdown_file.exists()
```

**Benefits:**
- Real-time health monitoring for system status
- Performance metrics for optimization
- Graceful shutdown prevents data corruption
- Foundation for Phase 2 system health dashboard

## Implementation: 2-3 days

1. Add iteration timing and health tracking
2. Implement graceful shutdown handling
3. Create health metrics logging for Phase 2 analysis# [CRITICAL] Daemon Loop Performance Monitoring

**Labels:** `critical`, `phase-2-blocker`, `instrumentation`, `daemon`, `performance`

## Problem Statement

The daemon loop in `ghost/ghostd.py` lacks performance monitoring capabilities, making it impossible to diagnose daemon health issues, optimize polling intervals, or provide meaningful metrics for Phase 2 introspection suite development.

## Current State Analysis

```python
def ghostd_loop(poll_interval=10):
    print("👻 ghostd running — watching queue...")
    while True:
        queue = load_queue()
        for task in queue:
            print(f"🔁 running ritual for: {task}")
            dispatch_ritual(task)
            clear_task(task)
        time.sleep(poll_interval)
```

### Issues Identified:

1. **No loop iteration metrics** - Cannot measure daemon performance
2. **No queue processing timing** - Unknown how long tasks take to process
3. **No error recovery monitoring** - Daemon failures are not tracked
4. **No resource usage tracking** - Memory/CPU consumption unknown
5. **No health status reporting** - Cannot determine if daemon is healthy
6. **No adaptive polling** - Fixed interval regardless of queue activity
7. **No graceful shutdown** - No way to stop daemon cleanly

## Impact on Phase 2

The introspection suite requires:
- **Daemon health metrics** for system monitoring
- **Processing performance data** for optimization analysis
- **Error rate tracking** for reliability assessment
- **Resource usage patterns** for capacity planning

Without daemon monitoring, Phase 2 cannot assess ghost system operational health.

## Proposed Solution

### 1. Create Daemon Monitoring Framework

```python
# ghost/core/daemon_monitor.py
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import time
import psutil
import threading
import signal
import json
from pathlib import Path

@dataclass
class DaemonIterationMetrics:
    iteration_id: str
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    duration_ms: Optional[float] = None
    queue_size: int = 0
    tasks_processed: int = 0
    tasks_successful: int = 0
    tasks_failed: int = 0
    memory_usage_mb: float = 0.0
    cpu_percent: float = 0.0
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DaemonHealthStatus:
    is_running: bool = True
    uptime_seconds: float = 0.0
    total_iterations: int = 0
    total_tasks_processed: int = 0
    avg_iteration_time_ms: float = 0.0
    current_memory_mb: float = 0.0
    peak_memory_mb: float = 0.0
    error_rate: float = 0.0
    last_activity: Optional[datetime] = None
    status: str = "unknown"  # healthy, degraded, critical, stopped

class DaemonMonitor:
    def __init__(self, metrics_file_path: str):
        self.metrics_file = Path(metrics_file_path)
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.start_time = datetime.now()
        self.current_iteration = None
        self.iteration_history = []
        self.health_status = DaemonHealthStatus()
        self.lock = threading.Lock()
        self.enabled = True
        self.shutdown_requested = False
        
        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
        # Start background health monitor
        self.health_thread = threading.Thread(target=self._health_monitor_loop, daemon=True)
        self.health_thread.start()
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\n👻 Received signal {signum}, initiating graceful shutdown...")
        self.shutdown_requested = True
    
    def start_iteration(self, queue_size: int) -> str:
        """Start monitoring a new daemon iteration"""
        if not self.enabled:
            return ""
            
        iteration_id = f"iter_{int(time.time() * 1000)}"
        
        with self.lock:
            self.current_iteration = DaemonIterationMetrics(
                iteration_id=iteration_id,
                queue_size=queue_size
            )
            
            # Capture system metrics
            process = psutil.Process()
            self.current_iteration.memory_usage_mb = process.memory_info().rss / 1024 / 1024
            self.current_iteration.cpu_percent = process.cpu_percent()
        
        return iteration_id
    
    def finish_iteration(self, iteration_id: str, tasks_processed: int, 
                        tasks_successful: int, errors: List[str] = None):
        """Complete monitoring for a daemon iteration"""
        if not self.enabled or not self.current_iteration:
            return
            
        with self.lock:
            if self.current_iteration.iteration_id != iteration_id:
                return  # Mismatched iteration
            
            # Finalize metrics
            self.current_iteration.end_time = datetime.now()
            self.current_iteration.duration_ms = (
                self.current_iteration.end_time - self.current_iteration.start_time
            ).total_seconds() * 1000
            
            self.current_iteration.tasks_processed = tasks_processed
            self.current_iteration.tasks_successful = tasks_successful
            self.current_iteration.tasks_failed = tasks_processed - tasks_successful
            self.current_iteration.errors = errors or []
            
            # Update final system metrics
            process = psutil.Process()
            final_memory = process.memory_info().rss / 1024 / 1024
            self.current_iteration.metadata['memory_delta_mb'] = (
                final_memory - self.current_iteration.memory_usage_mb
            )
            
            # Store completed iteration
            self.iteration_history.append(self.current_iteration)
            self.current_iteration = None
            
            # Update health status
            self._update_health_status()
            
            # Persist metrics
            self._persist_metrics()
    
    def log_error(self, error_msg: str):
        """Log an error during daemon operation"""
        if self.current_iteration:
            self.current_iteration.errors.append(error_msg)
    
    def _update_health_status(self):
        """Update overall daemon health status"""
        now = datetime.now()
        recent_iterations = [
            it for it in self.iteration_history[-100:]  # Last 100 iterations
            if now - it.start_time < timedelta(hours=1)
        ]
        
        if not recent_iterations:
            self.health_status.status = "unknown"
            return
        
        # Calculate health metrics
        self.health_status.uptime_seconds = (now - self.start_time).total_seconds()
        self.health_status.total_iterations = len(self.iteration_history)
        self.health_status.total_tasks_processed = sum(it.tasks_processed for it in self.iteration_history)
        
        recent_durations = [it.duration_ms for it in recent_iterations if it.duration_ms]
        if recent_durations:
            self.health_status.avg_iteration_time_ms = sum(recent_durations) / len(recent_durations)
        
        # Memory tracking
        process = psutil.Process()
        self.health_status.current_memory_mb = process.memory_info().rss / 1024 / 1024
        self.health_status.peak_memory_mb = max(
            self.health_status.peak_memory_mb,
            self.health_status.current_memory_mb
        )
        
        # Error rate calculation
        total_tasks = sum(it.tasks_processed for it in recent_iterations)
        failed_tasks = sum(it.tasks_failed for it in recent_iterations)
        self.health_status.error_rate = failed_tasks / max(total_tasks, 1)
        
        self.health_status.last_activity = now
        
        # Determine health status
        if self.health_status.error_rate > 0.5:
            self.health_status.status = "critical"
        elif self.health_status.error_rate > 0.2 or self.health_status.avg_iteration_time_ms > 30000:
            self.health_status.status = "degraded"
        else:
            self.health_status.status = "healthy"
    
    def _health_monitor_loop(self):
        """Background thread for continuous health monitoring"""
        while not self.shutdown_requested:
            try:
                time.sleep(60)  # Check every minute
                
                # Check for stalled daemon
                if self.health_status.last_activity:
                    time_since_activity = datetime.now() - self.health_status.last_activity
                    if time_since_activity > timedelta(minutes=5):
                        self.health_status.status = "stalled"
                
                # Memory leak detection
                if self.health_status.current_memory_mb > 500:  # 500MB threshold
                    print(f"⚠️ High memory usage detected: {self.health_status.current_memory_mb:.1f}MB")
                
            except Exception as e:
                print(f"⚠️ Health monitor error: {e}")
    
    def _persist_metrics(self):
        """Persist metrics to disk for analysis"""
        try:
            # Keep only last 1000 iterations to prevent file bloat
            recent_history = self.iteration_history[-1000:]
            
            metrics_data = {
                'daemon_start_time': self.start_time.isoformat(),
                'health_status': {
                    'is_running': self.health_status.is_running,
                    'uptime_seconds': self.health_status.uptime_seconds,
                    'total_iterations': self.health_status.total_iterations,
                    'total_tasks_processed': self.health_status.total_tasks_processed,
                    'avg_iteration_time_ms': self.health_status.avg_iteration_time_ms,
                    'current_memory_mb': self.health_status.current_memory_mb,
                    'peak_memory_mb': self.health_status.peak_memory_mb,
                    'error_rate': self.health_status.error_rate,
                    'last_activity': self.health_status.last_activity.isoformat() if self.health_status.last_activity else None,
                    'status': self.health_status.status
                },
                'recent_iterations': [
                    {
                        'iteration_id': it.iteration_id,
                        'start_time': it.start_time.isoformat(),
                        'end_time': it.end_time.isoformat() if it.end_time else None,
                        'duration_ms': it.duration_ms,
                        'queue_size': it.queue_size,
                        'tasks_processed': it.tasks_processed,
                        'tasks_successful': it.tasks_successful,
                        'tasks_failed': it.tasks_failed,
                        'memory_usage_mb': it.memory_usage_mb,
                        'cpu_percent': it.cpu_percent,
                        'errors': it.errors,
                        'metadata': it.metadata
                    }
                    for it in recent_history
                ]
            }
            
            with self.metrics_file.open('w') as f:
                json.dump(metrics_data, f, indent=2)
                
        except Exception as e:
            print(f"⚠️ Failed to persist daemon metrics: {e}")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get current performance summary"""
        recent_iterations = self.iteration_history[-50:]  # Last 50 iterations
        
        if not recent_iterations:
            return {'status': 'no_data'}
        
        durations = [it.duration_ms for it in recent_iterations if it.duration_ms]
        queue_sizes = [it.queue_size for it in recent_iterations]
        
        return {
            'status': self.health_status.status,
            'uptime_hours': self.health_status.uptime_seconds / 3600,
            'total_iterations': len(self.iteration_history),
            'avg_iteration_time_ms': sum(durations) / len(durations) if durations else 0,
            'min_iteration_time_ms': min(durations) if durations else 0,
            'max_iteration_time_ms': max(durations) if durations else 0,
            'avg_queue_size': sum(queue_sizes) / len(queue_sizes) if queue_sizes else 0,
            'max_queue_size': max(queue_sizes) if queue_sizes else 0,
            'current_memory_mb': self.health_status.current_memory_mb,
            'peak_memory_mb': self.health_status.peak_memory_mb,
            'error_rate': self.health_status.error_rate,
            'tasks_per_hour': self.health_status.total_tasks_processed / max(self.health_status.uptime_seconds / 3600, 1)
        }
    
    def should_shutdown(self) -> bool:
        """Check if graceful shutdown was requested"""
        return self.shutdown_requested

# Global daemon monitor
daemon_monitor = DaemonMonitor(str(STATE_DIR / "daemon_metrics.json"))
```

### 2. Enhanced Daemon Loop with Monitoring

```python
# Enhanced ghost/ghostd.py
import time
import signal
import sys
from ghost.core.config import STATE_DIR
from ghost.core.queue import load_queue, clear_task
from ghost.core.runtime import dispatch_ritual
from ghost.core.daemon_monitor import daemon_monitor

def ghostd_loop(poll_interval=10, adaptive_polling=True):
    """
    Enhanced daemon loop with comprehensive monitoring and adaptive polling
    """
    print("👻 ghostd running — watching queue with monitoring enabled...")
    
    consecutive_empty_polls = 0
    max_empty_polls_for_backoff = 5
    base_poll_interval = poll_interval
    max_poll_interval = 60
    
    try:
        while not daemon_monitor.should_shutdown():
            # Adaptive polling: slow down when queue is consistently empty
            if adaptive_polling:
                if consecutive_empty_polls >= max_empty_polls_for_backoff:
                    current_poll_interval = min(
                        base_poll_interval * (1 + consecutive_empty_polls // max_empty_polls_for_backoff),
                        max_poll_interval
                    )
                else:
                    current_poll_interval = base_poll_interval
            else:
                current_poll_interval = poll_interval
            
            try:
                # Load queue and start monitoring iteration
                queue = load_queue()
                iteration_id = daemon_monitor.start_iteration(len(queue))
                
                tasks_processed = 0
                tasks_successful = 0
                errors = []
                
                if queue:
                    consecutive_empty_polls = 0
                    print(f"🔄 Processing {len(queue)} tasks...")
                    
                    for task in queue:
                        try:
                            print(f"🔁 running ritual for: {task}")
                            
                            # Execute ritual with error handling
                            success = dispatch_ritual(task)
                            tasks_processed += 1
                            
                            if success:
                                tasks_successful += 1
                                clear_task(task)
                                print(f"✅ completed: {task}")
                            else:
                                error_msg = f"Ritual execution failed for: {task}"
                                errors.append(error_msg)
                                daemon_monitor.log_error(error_msg)
                                print(f"❌ failed: {task}")
                                
                        except Exception as e:
                            error_msg = f"Exception processing task '{task}': {str(e)}"
                            errors.append(error_msg)
                            daemon_monitor.log_error(error_msg)
                            print(f"💥 error: {error_msg}")
                            
                            # Still try to clear the task to prevent infinite loops
                            try:
                                clear_task(task)
                            except Exception as clear_error:
                                clear_error_msg = f"Failed to clear problematic task '{task}': {str(clear_error)}"
                                errors.append(clear_error_msg)
                                daemon_monitor.log_error(clear_error_msg)
                else:
                    consecutive_empty_polls += 1
                    if consecutive_empty_polls % 10 == 0:  # Log every 10th empty poll
                        print(f"😴 queue empty ({consecutive_empty_polls} consecutive empty polls)")
                
                # Finish monitoring iteration
                daemon_monitor.finish_iteration(iteration_id, tasks_processed, tasks_successful, errors)
                
                # Report performance periodically
                if daemon_monitor.health_status.total_iterations % 50 == 0:  # Every 50 iterations
                    performance = daemon_monitor.get_performance_summary()
                    print(f"📊 Performance: {performance['avg_iteration_time_ms']:.1f}ms/iter, "
                          f"{performance['tasks_per_hour']:.1f} tasks/hr, "
                          f"memory: {performance['current_memory_mb']:.1f}MB, "
                          f"status: {performance['status']}")
                
            except Exception as e:
                error_msg = f"Critical daemon loop error: {str(e)}"
                daemon_monitor.log_error(error_msg)
                print(f"💥 {error_msg}")
                
                # Try to continue running unless it's a critical error
                if "KeyboardInterrupt" in str(e):
                    break
            
            # Sleep with monitoring for shutdown signals
            sleep_start = time.time()
            while time.time() - sleep_start < current_poll_interval:
                if daemon_monitor.should_shutdown():
                    break
                time.sleep(0.1)  # Check shutdown every 100ms
                
    except KeyboardInterrupt:
        print("\n👻 Received keyboard interrupt")
    finally:
        print("👻 Daemon shutting down gracefully...")
        daemon_monitor.health_status.is_running = False
        daemon_monitor._persist_metrics()

def start_daemon(poll_interval=10, adaptive_polling=True, daemonize=False):
    """
    Start the ghost daemon with optional daemonization
    """
    if daemonize:
        # Fork to background (Unix only)
        import os
        pid = os.fork()
        if pid > 0:
            # Parent process
            print(f"👻 Daemon started with PID {pid}")
            
            # Write PID file
            pid_file = STATE_DIR / "daemon.pid"
            with pid_file.open('w') as f:
                f.write(str(pid))
            
            return pid
        else:
            # Child process - become daemon
            os.setsid()
            os.chdir('/')
            
            # Redirect stdout/stderr to log files
            log_dir = STATE_DIR / "logs"
            log_dir.mkdir(exist_ok=True)
            
            with open(log_dir / "daemon.log", 'a') as log_file:
                os.dup2(log_file.fileno(), sys.stdout.fileno())
                os.dup2(log_file.fileno(), sys.stderr.fileno())
    
    # Start the main loop
    ghostd_loop(poll_interval, adaptive_polling)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="GhostOS Daemon")
    parser.add_argument("--interval", type=int, default=10, 
                       help="Polling interval in seconds")
    parser.add_argument("--no-adaptive", action="store_true",
                       help="Disable adaptive polling")
    parser.add_argument("--daemonize", action="store_true",
                       help="Run as background daemon")
    
    args = parser.parse_args()
    
    start_daemon(
        poll_interval=args.interval,
        adaptive_polling=not args.no_adaptive,
        daemonize=args.daemonize
    )
```

### 3. Daemon Status and Control Commands

```python
# Enhanced ghost/core/daemon.py
import subprocess
import os
import signal
import sys
import psutil
import json
from pathlib import Path
from datetime import datetime

from ghost.core.config import VAULT, STATE_DIR
from ghost.core.daemon_monitor import daemon_monitor

def start_ghostd(poll_interval=10, adaptive_polling=True):
    """Start the ghost daemon with enhanced monitoring"""
    print("👻 starting ghostd with monitoring...")
    
    ghostd_path = VAULT / "ghost" / "ghostd.py"
    python_exec = sys.executable
    
    # Check if already running
    if is_daemon_running():
        print("⚠️ Daemon is already running")
        return False
    
    try:
        # Start daemon process
        cmd = [
            python_exec, str(ghostd_path),
            "--interval", str(poll_interval),
            "--daemonize"
        ]
        
        if not adaptive_polling:
            cmd.append("--no-adaptive")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("🚀 ghostd started successfully")
            return True
        else:
            print(f"❌ Failed to start ghostd: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to start ghostd: {e}")
        return False

def stop_ghostd():
    """Stop the ghost daemon gracefully"""
    pid_file = STATE_DIR / "daemon.pid"
    
    if not pid_file.exists():
        print("❌ no running ghostd process found.")
        return False
    
    try:
        with pid_file.open("r") as f:
            pid = int(f.read().strip())
        
        if not psutil.pid_exists(pid):
            print("⚠️ PID file exists but process not found. Cleaning up.")
            pid_file.unlink()
            return False
        
        # Send TERM signal for graceful shutdown
        os.kill(pid, signal.SIGTERM)
        
        # Wait for process to exit (up to 30 seconds)
        import time
        for _ in range(30):
            if not psutil.pid_exists(pid):
                break
            time.sleep(1)
        
        if psutil.pid_exists(pid):
            print("⚠️ Daemon didn't exit gracefully, forcing termination")
            os.kill(pid, signal.SIGKILL)
        
        pid_file.unlink()
        print("🛑 ghostd stopped.")
        return True
        
    except (ProcessLookupError, FileNotFoundError):
        print("⚠️ process not found. cleaning up.")
        if pid_file.exists():
            pid_file.unlink()
        return False
    except Exception as e:
        print(f"❌ Error stopping daemon: {e}")
        return False

def status_ghostd():
    """Get comprehensive daemon status"""
    pid_file = STATE_DIR / "daemon.pid"
    metrics_file = STATE_DIR / "daemon_metrics.json"
    
    # Check if daemon is running
    is_running = False
    pid = None
    process_info = {}
    
    if pid_file.exists():
        try:
            with pid_file.open("r") as f:
                pid = int(f.read().strip())
            
            if psutil.pid_exists(pid):
                is_running = True
                process = psutil.Process(pid)
                process_info = {
                    'pid': pid,
                    'status': process.status(),
                    'cpu_percent': process.cpu_percent(),
                    'memory_mb': process.memory_info().rss / 1024 / 1024,
                    'create_time': datetime.fromtimestamp(process.create_time()).isoformat(),
                    'num_threads': process.num_threads()
                }
        except (ValueError, psutil.NoSuchProcess):
            pass
    
    # Load performance metrics
    performance_data = {}
    if metrics_file.exists():
        try:
            with metrics_file.open('r') as f:
                performance_data = json.load(f)
        except Exception as e:
            performance_data = {'error': f'Failed to load metrics: {e}'}
    
    status_report = {
        'is_running': is_running,
        'process_info': process_info,
        'performance_metrics': performance_data.get('health_status', {}),
        'recent_activity': len(performance_data.get('recent_iterations', [])),
        'status': 'running' if is_running else 'stopped'
    }
    
    return status_report

def is_daemon_running() -> bool:
    """Check if daemon is currently running"""
    pid_file = STATE_DIR / "daemon.pid"
    
    if not pid_file.exists():
        return False
    
    try:
        with pid_file.open("r") as f:
            pid = int(f.read().strip())
        return psutil.pid_exists(pid)
    except (ValueError, FileNotFoundError):
        return False

def get_daemon_logs(lines: int = 50) -> List[str]:
    """Get recent daemon log entries"""
    log_file = STATE_DIR / "logs" / "daemon.log"
    
    if not log_file.exists():
        return []
    
    try:
        with log_file.open('r') as f:
            all_lines = f.readlines()
            return all_lines[-lines:] if len(all_lines) > lines else all_lines
    except Exception as e:
        return [f"Error reading logs: {e}"]
```

### 4. CLI Integration for Daemon Monitoring

```python
# Enhanced ghost/cli/cli.py - Add new daemon monitoring commands

def main():
    # ... existing code ...
    
    match cmd:
        # ... existing cases ...
        
        case "start":
            from ghost.core.daemon import start_ghostd
            success = start_ghostd()
            cli_tracer.finish_command(context, 0 if success else 1)

        case "stop":
            from ghost.core.daemon import stop_ghostd
            success = stop_ghostd()
            cli_tracer.finish_command(context, 0 if success else 1)

        case "statusd":
            from ghost.core.daemon import status_ghostd
            status = status_ghostd()
            print_daemon_status(status, context)
            cli_tracer.finish_command(context, 0)
        
        case "logs":
            from ghost.core.daemon import get_daemon_logs
            lines = int(args[1]) if len(args) > 1 else 50
            logs = get_daemon_logs(lines)
            for log_line in logs:
                traced_print(context, log_line.strip())
            cli_tracer.finish_command(context, 0)
        
        case "health":
            from ghost.core.daemon_monitor import daemon_monitor
            health = daemon_monitor.get_performance_summary()
            print_health_report(health, context)
            cli_tracer.finish_command(context, 0)

def print_daemon_status(status: Dict[str, Any], context):
    """Print formatted daemon status"""
    traced_print(context, "🔍 Daemon Status Report")
    traced_print(context, f"Status: {'🟢 Running' if status['is_running'] else '🔴 Stopped'}")
    
    if status['process_info']:
        pi = status['process_info']
        traced_print(context, f"PID: {pi['pid']}")
        traced_print(context, f"Memory: {pi['memory_mb']:.1f}MB")
        traced_print(context, f"CPU: {pi['cpu_percent']:.1f}%")
        traced_print(context, f"Threads: {pi['num_threads']}")
    
    if status['performance_metrics']:
        pm = status['performance_metrics']
        traced_print(context, f"Uptime: {pm.get('uptime_seconds', 0) / 3600:.1f} hours")
        traced_print(context, f"Total iterations: {pm.get('total_iterations', 0)}")
        traced_print(context, f"Error rate: {pm.get('error_rate', 0):.1%}")

def print_health_report(health: Dict[str, Any], context):
    """Print formatted health report"""
    traced_print(context, "📊 Daemon Health Report")
    traced_print(context, f"Status: {health.get('status', 'unknown').upper()}")
    traced_print(context, f"Uptime: {health.get('uptime_hours', 0):.1f} hours")
    traced_print(context, f"Avg iteration time: {health.get('avg_iteration_time_ms', 0):.1f}ms")
    traced_print(context, f"Tasks per hour: {health.get('tasks_per_hour', 0):.1f}")
    traced_print(context, f"Memory usage: {health.get('current_memory_mb', 0):.1f}MB")
    traced_print(context, f"Peak memory: {health.get('peak_memory_mb', 0):.1f}MB")
```

## Implementation Plan

### Phase 1: Monitoring Framework (2-3 days)
1. Create `ghost/core/daemon_monitor.py`
2. Implement DaemonIterationMetrics and DaemonMonitor classes
3. Add signal handling for graceful shutdown

### Phase 2: Daemon Enhancement (2-3 days)
1. Refactor `ghost/ghostd.py` to use monitoring framework
2. Add adaptive polling and error recovery
3. Implement daemonization options

### Phase 3: Status and Control (1-2 days)
1. Enhance `ghost/core/daemon.py` with monitoring integration
2. Add new CLI commands for daemon management
3. Implement log viewing and health reporting

## Acceptance Criteria

- [ ] Daemon loop performance is monitored with microsecond precision
- [ ] Resource usage (CPU, memory) is tracked continuously
- [ ] Error rates and failure patterns are captured and analyzed
- [ ] Graceful shutdown handling prevents data loss
- [ ] Adaptive polling optimizes performance based on queue activity
- [ ] Health status provides actionable insights for system monitoring
- [ ] CLI commands provide comprehensive daemon management
- [ ] Performance metrics support Phase 2 introspection suite requirements

## Files to Modify

- `ghost/ghostd.py` - Enhanced daemon loop with monitoring
- `ghost/core/daemon_monitor.py` - New monitoring framework
- `ghost/core/daemon.py` - Enhanced daemon management
- `ghost/cli/cli.py` - New daemon monitoring commands
- `ghost/tests/test_daemon.py` - Unit tests for daemon monitoring

## Dependencies

- `psutil` - For system resource monitoring
- No other external dependencies required

## Risks

- **Performance overhead** - Monitoring adds computational cost to daemon operations
- **Storage usage** - Metrics files may grow large over extended operation
- **Complexity increase** - More moving parts to debug and maintain

## Mitigation Strategies

- **Configurable monitoring levels** - Allow disabling detailed monitoring in production
- **Automatic log rotation** - Prevent unbounded growth of metrics files
- **Fallback mechanisms** - Daemon continues operating even if monitoring fails
- **Performance budgets** - Monitor monitoring overhead and alert if excessive