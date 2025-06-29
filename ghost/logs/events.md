# ghostOS-kernel event log

Timestamped task execution events.
Format defined in Issue #6.[2025-06-29 06:56:03] task_id:test-001 status:running script:echo 'Hello from ghostOS-kernel daemon!'
[2025-06-29 06:56:03] task_id:test-001 status:done returncode:0
[2025-06-29 06:56:16] task_id:test-002 status:running script:false
[2025-06-29 06:56:16] task_id:test-002 status:failed returncode:1 stderr:no error output
[2025-06-29 07:06:01] daemon status:started scanning_interval:5s
[2025-06-29 07:08:31] task_id:test-003 status:running script:echo 'Clean daemon - no psutil needed!'
[2025-06-29 07:08:31] task_id:test-003 status:done returncode:0
