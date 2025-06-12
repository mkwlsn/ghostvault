---
epic:
  - threshold
status: planned
owner: ghostOS
description:
---
## 🧩 STORY: schema-based validation

```yaml
id: schema-validation
status: threshold-blocker
effort: 3h
tags: [validation, schema, contracts]
```

### Tasks
- define `ghost_state.schema.json` for daemon state
- define `ritual.schema.yaml` for ritual metadata
- define config file schema (JSON or TOML)
- implement `ghost validate` command to check all inputs

### Success Criteria
- malformed state/config/rituals are rejected with clear errors
- schema files live in `/ghost/schemas` or equivalent dir
- validator is CLI-callable and integrated into daemon boot

---

## 🧩 STORY: system health check

```yaml
id: health-check
status: threshold-blocker
effort: 2h
tags: [introspection, validation, system-check]
```

### Tasks
- build `ghost check` command
- scan for:
  - config/schema validity
  - stale queue entries
  - dead daemon heartbeat
- emit summary with ✅/❌ indicators

### Success Criteria
- user can run `ghost check` at any time to inspect system coherence
- error messages are readable and actionable
- no valid system state causes a false failure

---

## 🧩 STORY: integration test harness

```yaml
id: threshold-tests
status: threshold-blocker
effort: 3h
tags: [testing, validation, CI]
```

### Tasks
- write `tests/test_threshold.py` with:
  - daemon boot
  - queue injection
  - log + state assertions
- create `ghost test threshold` runner
- optionally: hook into pre-push git hook

### Success Criteria
- all threshold behaviors are tested automatically
- test fails if ghost doesn’t update state/log/queue correctly
- devs can confidently refactor post-threshold

---

## 🧩 STORY: daemon heartbeat

```yaml
id: daemon-heartbeat
status: threshold-blocker
effort: 2h
tags: [daemon, liveness, monitoring]
```

### Tasks
- have daemon update a heartbeat timestamp in `ghost_state.json` every 30s
- build `ghost status` to report:
  - when ghost was last active
  - whether the daemon is alive
- detect stale heartbeats (e.g. > 2min old)

### Success Criteria
- user can see if ghost is running or stalled
- `ghost check` includes heartbeat in overall health
- ghost never silently dies

"""