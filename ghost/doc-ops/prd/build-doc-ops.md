---
id: epic-docops
title: DocOps Semantic Foundation
status: active
created: 2025-06-12
authors: [ghost, mike]
bundle_id: semantic-layer
tags: [docops, semantic-markdown, personas, rituals, contributor-experience]
epic_id: docops-001
---

# Epic: DocOps Semantic Foundation

## 🎯 Goal

Establish a complete and extensible **DocOps layer** for GhostOS that makes `.md`-based planning executable, composable, and multi-agent compatible. This system becomes the foundation for:

- authoring specs and epics in semantic markdown
- validating and parsing PRDs automatically
- running agent-based simulations from persona rituals
- integrating with CLI + external planning tools (e.g. Linear)
- onboarding new contributors through a system-native workflow

This is the OS for operating specs.

---

## 🔧 Deliverables

### 1. 📑 `semantic-markdown-spec.md`

- Defines all valid frontmatter fields, fenced block types, and structure
- Canonical types: `epic`, `story`, `task`, `ritual`, etc
- Includes schema for validation (e.g. pydantic)

### 2. 🤖 Validator + Parser

- CLI: `ghost validate prd path/to/file.md`
- Detects malformed frontmatter, unknown fields, missing sections
- Prepares PRDs for simulation and bundling

### 3. 🧠 Persona Rituals

- Executable simulations via CLI (e.g. `ghost simulate persona`)
- Persona definitions in `/docs/personas/`
- Persona-specific critique heuristics + insight memory

### 4. 📦 Bundling System

- `bundle_id` field links multiple stories/epics
- CLI: `ghost list prds --bundle foo`
- Optional: markdown index auto-generated

### 5. 🔐 ID Registry

- CLI: `ghost generate id --type story`
- Canonical unique IDs per PRD/story
- Central registry (flat file or lightweight cache)

### 6. ⏳ Lifecycle Model

- PRD statuses: `draft`, `active`, `shipped`, `deprecated`
- CLI helpers: `ghost archive prd`, `ghost transition prd`
- CI enforcement rules (e.g. deprecated PRDs can’t be active in bundles)

### 7. 🎽 Effort Modeling

- `effort:` and `size:` fields in stories/tasks
- Persona rituals simulate scoping, velocity, and workload modeling

### 8. 🧭 Contributor UX

- CLI: `ghost tutorial write-prd`
- `/docs/CONTRIBUTING.md` for spec writing
- Examples: dummy PRDs, semantic templates

### 9. 📓 Tactical Execution Stories

---

id: docops-001-story-001
title: Semantic Markdown Spec Definition
type: story
effort: 3
size: medium
status: draft
bundle_id: semantic-layer

---

Define and document all valid frontmatter fields, fenced block types, and structure for the DocOps semantic markdown specification.

**Success Criteria:**

- Complete schema for frontmatter fields
- Examples of valid and invalid markdown snippets
- Schema validation implemented in pydantic

---

id: docops-001-story-002
title: Validator and Parser CLI Tool
type: story
effort: 5
size: large
status: draft
bundle_id: semantic-layer

---

Build a CLI tool to validate PRDs against the semantic markdown spec and parse them into structured data.

**Success Criteria:**

- CLI command `ghost validate prd path/to/file.md`
- Detects malformed frontmatter, unknown fields, and missing sections
- Outputs structured parse results for downstream use

---

id: docops-001-story-003
title: Persona Rituals Execution Framework
type: story
effort: 5
size: large
status: draft
bundle_id: semantic-layer

---

Implement an executable simulation system for persona rituals, allowing agent-based testing of PRDs.

**Success Criteria:**

- CLI command `ghost simulate persona`
- Support for persona definitions in `/docs/personas/`
- Integration of critique heuristics and insight memory

---

id: docops-001-story-004
title: Bundling and ID Registry System
type: story
effort: 4
size: medium
status: draft
bundle_id: semantic-layer

---

Create a bundling system linking multiple stories and epics, with a central ID registry.

**Success Criteria:**

- `bundle_id` field support across PRDs
- CLI commands `ghost list prds --bundle foo` and `ghost generate id --type story`
- Central registry implemented as flat file or cache

---

id: docops-001-story-005
title: Contributor Experience Enhancements
type: story
effort: 3
size: medium
status: draft
bundle_id: semantic-layer

---

Improve contributor UX with tutorials, contributing guides, and example PRDs.

**Success Criteria:**

- CLI tutorial `ghost tutorial write-prd`
- `/docs/CONTRIBUTING.md` updated with spec writing guidelines
- Sample dummy PRDs and semantic templates provided

---

---

## 🛠️ Integration Points

- **ghost queue**: all stories spec’d with IDs, PRD links, status
- **Linear + Claude**: agents parse PRDs and execute stories via ID/tag
- **DocOps CI**: schema validation on commit, doc coverage enforcement

---

## 🧠 Strategic Payoff

1. **Spec Stability** — all specs become testable artifacts
2. **Agent Simulation** — rituals model real roles with memory + heuristics
3. **Scalable Collab** — onboarding = reading, simulating, contributing
4. **Agent PM** — ghost can queue, staff, and execute work from specs
5. **Infra for Everything Else** — future client work, Arcanahaus, etc

---

## 🧩 Related Work

- `epic-bootstrap` (requires story refactors post-docops)
- `epic-threshold` (re-prioritization candidate)
- `epic-semantic-layer` (early scaffolding for current work)
- `babelfish` (contributor-layer becomes testable post-docops)

---

## ⌛ Est. Delivery Time

| Phase                           | Est. Time     |
| ------------------------------- | ------------- |
| Spec + persona ritual scaffolds | 1–2 days      |
| Parsing, bundling, validation   | 2–3 days      |
| Ghost CLI integration           | 1 day         |
| Contributor DX                  | 2–4 days      |
| README + contributor guide      | 1–2 days      |
| Integration testing             | 1–2 days      |
| **Total**                       | **8–14 days** |

(optional hot-swap: compress to 5–7 days with active assistant loop)

---

## 🔁 Status

✅ Persona ritual drafts exist  
✅ Semantic spec in progress  
🚧 Parser/validator partially scaffolded  
🚧 README + CONTRIBUTING not complete  
🚧 Linear/CLI integration pending
