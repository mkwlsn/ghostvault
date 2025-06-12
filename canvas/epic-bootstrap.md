---
epic: bootstrap
status: planned
owner: ghostOS
description: >
  Establish a minimal autonomous system presence by interleaving core daemon lifecycle
  features with validation, liveness, and introspection capabilities. This includes the
  creation of a persistent execution loop, state tracking, system validation, and CLI visibility.
---

```yaml
story: define ritual and ghost_state schemas
tags: [schema, validation]
tasks:
  - draft JSON schema for ghost_state
  - draft JSON schema for rituals
  - add schema validation hooks to ritual executor
success_criteria:
  - schemas are defined and versioned
  - invalid rituals/state are rejected with clear errors
```

```yaml
story: build core daemon and execution loop
tags: [daemon, core]
tasks:
  - create ghostd runner script
  - implement queue read → ritual execute → state write cycle
  - ensure daemon starts/stops cleanly
success_criteria:
  - ghostd persists and executes rituals as expected
  - logs ritual transitions and errors
```

```yaml
story: implement daemon heartbeat
tags: [daemon, liveness]
tasks:
  - implement periodic heartbeat event in ghostd
  - write to heartbeat log or state timestamp
success_criteria:
  - system can confirm daemon is alive in real time
```

```yaml
story: implement ghost check CLI
tags: [cli, validation]
tasks:
  - build CLI tool to validate schema conformity
  - check ghost_state, queue, and rituals
success_criteria:
  - ghost check returns pass/fail status with details
```

```yaml
story: implement ghost status CLI
tags: [cli, liveness]
tasks:
  - build CLI to surface ghost_state summary and queue status
  - display daemon heartbeat and idle/active state
success_criteria:
  - `ghost status` gives snapshot of current operational state
```

```yaml
story: add integration test harness
tags: [testing]
tasks:
  - define full-cycle ritual execution test case
  - test daemon recovery from invalid ritual
success_criteria:
  - test suite passes all bootstrap-phase conditions
```

```yaml
story: implement idle daemon behavior
tags: [daemon, core]
tasks:
  - define idle wait strategy for empty queue
  - ensure heartbeat still updates during idle
success_criteria:
  - daemon remains responsive with empty queue
```

```yaml
story: add daemon recovery affordance
tags: [resilience]
tasks:
  - detect and recover from corrupted queue/state
  - log recovery attempts and outcomes
success_criteria:
  - daemon can restart into a known-safe operational state
```
"""