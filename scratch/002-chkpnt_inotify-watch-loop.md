# 002-chkpnt_inotify-watch-loop.md

## Objective
Transform ghostd.py from batch processor to reactive daemon using inotify file watching.

## Implementation Plan

### Phase 1: Architecture Preparation
- [x] Import required modules (signal, time - modified: no select/os needed for polling)
- [x] Add signal handling setup for graceful shutdown
- [x] Create daemon mode flag/argument parsing
- [x] Preserve existing batch processing as fallback mode

### Phase 2: File Watching Integration
- [x] ~~Add inotify file descriptor setup~~ → **Implemented cross-platform polling** (inotify unavailable on macOS)
- [x] ~~Create watch loop using select()~~ → **Implemented polling with 0.5s interval**
- [x] ~~Handle IN_CLOSE_WRITE events~~ → **Track file set changes for YAML detection**
- [x] Filter events to only process .yaml/.yml files
- [x] Add error handling for setup failures (graceful fallback)
- [x] **Test isolation**: Create standalone test that just prints "detected file X" for dropped files
- [x] Validate file detection before connecting to processing pipeline

### Phase 3: Execution Flow Refactoring
- [x] Extract existing file processing logic into reusable functions
- [x] Create event handler that calls existing processing pipeline
- [x] Maintain existing batch mode for backward compatibility
- [x] Add verbose logging for watch events

### Phase 4: Entry Point and Control
- [x] Create `__main__` dispatcher with mode selection
- [x] Add command-line options: `--watch`, `--batch`, `--verbose`
- [x] Implement clean shutdown on SIGINT/SIGTERM
- [x] Add startup validation for daemon mode

### Phase 5: Testing and Validation
- [x] Test batch mode still works identically
- [x] Test watch mode responds to file drops
- [x] Test graceful shutdown behavior
- [x] Test error handling for missing directories
- [x] Validate existing .ghost/ structure compatibility

### Phase 6: Documentation Updates
- [x] Update CLAUDE.md with new daemon behavior
- [x] Document command-line options
- [x] Add usage examples for both modes

## Key Principles
- **Preserve existing logic**: File processing functions remain unchanged ✅
- **Backward compatibility**: Batch mode must work exactly as before ✅
- **Minimal complexity**: No traditional daemon features (PID files, etc.) ✅
- **Immediate response**: ~~inotify~~ **polling provides sub-second file detection** ✅
- **Clean shutdown**: Graceful handling of interruption signals ✅

## Success Criteria
- [x] Drop YAML in .ghost/output/ → immediate processing
- [x] Batch mode unchanged for existing workflows
- [x] Clean startup/shutdown cycle
- [x] Ready for systemd/nohup deployment

## Implementation Complete
✅ All phases completed successfully. ghostd.py now supports both batch and watch modes with cross-platform file watching.

### Implementation Postmortem: inotify → Cross-Platform Polling

**What changed from the original plan:**
- **Target approach**: inotify-based file watching (Linux-specific)
- **Actual implementation**: Cross-platform polling approach
- **Reason for change**: Running on macOS (Darwin) - `os.inotify_init()` not available

**Technical decisions made:**
- **Polling interval**: 0.5 seconds (balance of responsiveness vs CPU usage)
- **Detection method**: File set comparison (track existing files, detect additions)
- **Graceful degradation**: No complex error states, simple fallback logic
- **Platform strategy**: Works immediately on all platforms

**Performance characteristics:**
- **Responsiveness**: Sub-second detection (0.5s worst case vs millisecond inotify)
- **CPU impact**: Minimal (brief directory scan every 0.5s)
- **Scalability**: Good for typical ghostOS usage (low file volume)
- **Memory usage**: Small set tracking previous file states

**Functional equivalence achieved:**
- ✅ Same user experience: Drop file → immediate processing
- ✅ Same reliability: Graceful shutdown, error handling
- ✅ Same backward compatibility: Batch mode unchanged
- ✅ Better cross-platform support: Works on macOS, Linux, Windows

**Future enhancement path:**
1. **Platform-specific optimization**: Detect OS and use inotify (Linux) or kqueue (macOS) when available
2. **Configurable polling**: `--poll-interval` argument for tuning
3. **Service integration**: systemd unit file examples

**Conclusion**: The polling approach was the right architectural choice for v0.0.1, providing immediate cross-platform compatibility with equivalent functionality. The implementation successfully transformed ghostd from batch processor to reactive daemon while maintaining simplicity and reliability.