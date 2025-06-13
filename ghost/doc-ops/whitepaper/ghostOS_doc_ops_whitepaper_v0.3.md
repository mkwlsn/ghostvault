---
title: ghostOS doc-ops whitepaper
type: whitepaper
status: active
version: 0.3
owner: ghost
updated: 2025-06-13
stage: active
purpose: Define doc-ops as structured memory and execution substrate
---

# ghostOS doc-ops: internal whitepaper (v0.3)

## 🧠 what is doc-ops?

doc-ops is the structured memory and execution substrate of ghostOS. it encodes system behavior, roles, and operational logic in markdown—designed to be readable by both LLMs and humans, traversable by daemons, and editable without breaking the system.

doc-ops is not just documentation—it is control surface, reasoning substrate, and executable map.

---

## 📁 core primitives

| type      | path                     | purpose                                                             |
|-----------|--------------------------|----------------------------------------------------------------------|
| PRD       | `/doc-ops/prds/`         | product/feature specs with semantically-linked artifacts            |
| spec      | `/doc-ops/--spec/`       | structural rules, schemas, validation constraints                    |
| ritual    | `/doc-ops/rituals/`      | modular executable units encoded in markdown                        |
| persona   | `/personas/`             | worldview files used to bias traversal and resolution                |
| metrics   | `/doc-ops/metrics/`      | system health, audit scaffolds, maturity models                     |
| changelog | `/doc-ops/changelog/`    | internal changes to doc-ops—not repo code                           |
| index     | `/doc-ops/INDEX.md`      | live memory map of all artifacts; eventual README candidate         |

---

## 🧠 semantic layer

the semantic layer is a lightweight relationship graph built from artifact frontmatter. it supports:

- **aliasing**: e.g. `handoff prep` → `prepare.md`
- **cross-linking**: via `related:` and markdown links
- **tag clustering**: for role-aware grouping
- **persona biasing**: scoring relevance per worldview

### frontmatter schema (enforced)

```yaml
title: prepare handoff
type: ritual
status: stable
aliases: [handoff, deliverables]
tags: [delivery, finalization]
related: [specs/review.md]
persona_bias:
  product_owner: 0.9
  engineer: 0.6
```

optional: `exports`, `fallback`, `invocation`, `locked_by`, `namespace`.

---

## 🎭 hats & personas

- **persona:** persistent worldview (e.g. product_owner, philosopher)
- **hat:** temporary role (e.g. reviewer, scribe)

### composite scoring:

```
score = 0.7 * persona_bias + 0.3 * hat_bias
```

conflict delta >0.75 = warning block post-resolution (unless `--interactive`)

### persona files include:

```yaml
persona: product_owner
biases:
  prefers: [delivery, impact]
  ignores: [purity]
traversal_depth: 1
```

hats are ephemeral and selected per request.

---

## 🧭 resolver ritual

`resolve.md` is the semantic entrypoint for task resolution.  
it accepts:

- `goal`: plain text input (e.g. “prepare handoff”)
- `context`: persona + hat
- `seed`: artifact name, if known

### output:
- markdown plan (ranked artifact list + confidence scores)
- optional `--explain` flag to include scoring rationale
- conflict warnings as blocks (bias mismatches, circular deps)

### graph mechanics:
- cycles are safe (tracked via visited set)
- broken `related:` refs are logged, not fatal
- default traversal = 2 hops; persona-defined override

---

## 🧩 ritual structure & execution

rituals are markdown files with:

```yaml
type: ritual
status: stable
exports:
  summary_output: string
```

```markdown
## Steps
1. summarize outputs
2. invoke: rituals/submit.md

## Fallback
- if: failure in prepare.md
- then: invoke: rituals/manual_review.md
```

rituals can call other rituals. `ghostd` halts on failure unless fallback is declared.  
context is passed down with namespace scoping: `{{prepare.summary_output}}`.

---

## 🔌 ghostd & task loop

`ghostd` is the runtime daemon:

1. indexes valid rituals on boot or `ghostd scan`
2. listens for task input or LLM triggers
3. executes rituals step-wise
4. records success/failure in artifact status + logs

ritual chaining is planned as DAG traversal with early termination on error unless override exists.

---

## ✅ implementation plan (phased)

### **phase 1: resolution MVP**
- artifact scanner
- tag/alias/related index
- goal → ranked artifact list (persona-weighted)
- CLI: `ghost resolve --goal "prepare handoff" --persona product_owner`

**success test:**  
> “prepare handoff” returns `rituals/prepare.md`, `specs/review.md` with explanation

---

### **phase 1.5: dry-run executor**
- plan output includes `would execute X`
- tests full pipeline without triggering real side effects

---

### **phase 2: daemon + execution**
- ghostd daemon loop
- parse + run markdown rituals
- status returns, logging, fallback chains

---

### **phase 3: persona depth, scoring, context**
- load persona files dynamically
- apply traversal depth
- interpolate context vars (`{{ritual.export}}`)
- conflict detection and `--interactive` resolution

---

### **phase 4: self-sustaining rituals**
- `verify-sync.md`: validates doc reality ↔ system state
- `bootstrap.md`: seeds folder structure
- `adopt.md`: wraps legacy scripts/docs into rituals
- `promote-index.md`: snapshots INDEX.md → README.md once >80% artifacts are stable

---

### **phase 5: audit layer + surface**
- `ghost audit` CLI (wraps `verify-sync.md`)
- future: local UI/tui for inspecting status, chains, failures

---

## 🧪 honesty mechanisms

### `verify-sync.md` spec

```markdown
## Goal
detect drift between declared system state and actual runtime.

## Checks
- ghost.config.yaml vs doc-ops declared specs
- orphaned or unreachable rituals
- broken `related:` refs
- malformed/missing frontmatter
- lock status violations
```

optional auto-repair: relink, log, or regenerate metadata.

---

## 📖 index promotion

`INDEX.md` is live, unstable memory.  
promotion to `README.md` occurs when:

- ≥80% artifacts are `status: stable`
- promotion is triggered via `promote-index.md`
- dead links are sanitized and changelog is updated

---

## 📌 conventions appendix

- **rituals:** `type: ritual`, must include steps
- **fallbacks:** markdown block with `if → then`
- **invocations:** `invoke:` paths in step list
- **context vars:** `{{ritual.namespace.key}}`
- **traversal depth:** declared in persona
- **audit tools:** `ghost audit` invokes `verify-sync.md`

---

## 🗺️ future unlocks

- ghostOS self-modification via ritual execution
- system observability from markdown surface
- role-aligned scaffolding for design, dev, ops
- doc-native daemon orchestration

---

ghostOS isn't just documented. it *knows how to describe itself*, *plan its own behavior*, and *enforce alignment between memory and action*.

this is the substrate.

let’s go build it.
