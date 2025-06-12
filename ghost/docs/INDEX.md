---
title: doc-ops INDEX
status: working
updated: 2025-06-12
version: 0.4
---

# 🗂️ `doc-ops/` INDEX

_This file is temporary working memory for `ghost/docs/doc-ops/`. Once the structure stabilizes, this will be renamed `README.md` and versioned._

## ✅ Purpose

`doc-ops/` contains the scaffolding, standards, and meta-guidance for the GhostOS documentation system. It defines how documentation is structured, validated, versioned, and authored—especially PRDs and rituals.

It enables:

- a consistent semantic markdown format for structured docs
- discoverability and composability across PRDs, specs, and checklists
- LLM-compatible parsing via naming, directory, and frontmatter conventions

## 📁 Directory Overview

### `--spec/`

- Canonical specs for doc-ops primitives (e.g. `--spec-semantic-markdown.md`)
- `--` prefix = static/pinned reference

### `checklist/`

- Operational validation rules and authoring checklists
- Used during PRD + spec authoring or review

### `metrics/`

- Quantitative/qualitative targets for documentation health and observability

### `changelog.md`

- Chronological changes to docops system and structure
- Meta-log scoped to this folder

### `INDEX.md`

- This file. Temporary working scratchpad to track status, structure, and progress

## 👣 Status Tracking

- [x] Moved all docops-relevant specs, PRDs, checklists into `/doc-ops/`
- [x] Removed deprecated versions from `/docs/specs/` and `/docs/prds/`
- [x] Created `--spec-*` convention for pinned structural specs
- [x] Defined and validated unified frontmatter format
- [x] Converted `docops-changelog.md` into `doc-ops/changelog.md`
- [x] Assigned version numbers and updated dates
- [x] Moved `personas-and-hats` into `/docs/personas/`
- [x] Purged all vestigial "epic-docops" files
- [ ] Finalize and promote `INDEX.md` to `README.md`
- [ ] Fully review checklist coverage for validation spec
- [ ] Evaluate placement of `rituals/`, `personas/`, and `glossary`

## 🧠 Open Questions

- Should `rituals/` and `personas/` move to `/docs/` as general knowledgebase content?
- Does `--spec-validation.md` need to absorb checklist logic?
- How do we support traversal from PRDs/stories → rituals → execution docs?
- Should we autogenerate a TOC/index for discoverability?

## 🧰 Working Notes

- Use `--` prefix for anything that serves as structural reference, not authored narrative.
- PRD structure is now standardized. All PRDs must have:
  - valid frontmatter (status, version, id, owner)
  - stories with yaml blocks
  - checkboxes for tasks + success criteria

---

_edit this file freely until finalized_
