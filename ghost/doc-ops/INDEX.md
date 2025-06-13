---
title: doc-ops Index
type: index
status: active
version: 1.0
owner: ghost
updated: 2025-06-13
description: Canonical directory map and status tracker for doc-ops files and system structure
---

# 🗂️ `doc-ops/` INDEX

_This file serves as the canonical index for all doc-ops artifacts. It replaces `--INDEX.md` and is now stable and versioned._

## ✅ Purpose

`doc-ops/` contains the scaffolding, standards, and meta-guidance for the GhostOS documentation system. It defines how documentation is structured, validated, versioned, and authored—especially PRDs and rituals.

It enables:

- a consistent semantic markdown format for structured docs
- discoverability and composability across PRDs, specs, and checklists
- LLM-compatible parsing via naming, directory, and frontmatter conventions

## 📁 Directory Overview

### `--spec/`

- Canonical specs for doc-ops formats and frontmatter structure
- Includes: `semantic-markdown.md`, `unified-docops-system.md`
- Planned: `frontmatter-schema.md` (per frontmatter PRD)

- Executable product requirements documents (e.g. `build-doc-ops.md`, `frontmatter.md`)
- Each PRD contains embedded stories/tasks and runs through full lifecycle

### `health/`

- Quality assurance + system observability
- `validation.md`: pre-commit and CI structural checks
- `metrics.md`: adoption and structural health indicators

### `changelog.md`

- Chronological changes to docops system and structure

### `--INDEX.md`

- This file. Temporary scratchpad to track status, structure, and open questions

## 👣 Status Tracking

- [x] Moved all docops-relevant specs, PRDs, checklists into `/doc-ops/`
- [x] Removed deprecated versions from `/docs/specs/` and `/docs/prds/`
- [x] Created `--spec-*` convention for pinned structural specs
- [x] Defined and validated unified frontmatter format
- [x] Converted `docops-changelog.md` into `doc-ops/changelog.md`
- [x] Assigned version numbers and updated dates
- [x] Moved `personas-and-hats` into `/docs/personas/`
- [x] Merged "epic-docops" into unified PRD at prd/build-doc-ops.md
- [x] Moved validation.md and metrics.md into /doc-ops/health/
- [x] Created health/README.md and aligned frontmatter in both docs
- [ ] Finalize and promote `INDEX.md` to `README.md`
- [x] Fully review checklist coverage for validation spec
- [ ] Evaluate placement of `rituals/`, `personas/`, and `glossary`

## 🧠 Open Questions

- Should `rituals/` and `personas/` move to `/docs/` as general knowledgebase content?
- Does `--spec-validation.md` need to absorb checklist logic?
- How do we support traversal from PRDs/stories → rituals → execution docs?
- Should we autogenerate a TOC/index for discoverability?
- Should we surface a manifest of docops files (e.g. /manifest.yaml) for LLMs and CLI traversal?

## 🧰 Working Notes

- PRD structure is now standardized. All PRDs must have:
  - valid frontmatter (status, version, id, owner)
  - stories with yaml blocks
  - checkboxes for tasks + success criteria

---

_edit this file freely until finalized_
