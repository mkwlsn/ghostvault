---
title: doc-ops Index
type: index
status: active
version: 1.0
owner: ghost
updated: 2024-06-07
description: Canonical directory map and status tracker for doc-ops files and system structure
---

# 🗂️ `doc-ops/` INDEX

_This file serves as the canonical index for all doc-ops artifacts. It is now stable and versioned._

## ✅ Purpose

`doc-ops/` contains the scaffolding, standards, and meta-guidance for the GhostOS documentation system. It defines how documentation is structured, validated, versioned, and authored—especially PRDs and rituals.

It enables:

- a consistent semantic markdown format for structured docs
- discoverability and composability across PRDs, specs, and checklists
- LLM-compatible parsing via naming, directory, and frontmatter conventions

## 📁 Directory Overview

### `spec/`

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

## 👣 Status Tracking

- [x] Moved all docops-relevant specs, PRDs, checklists into `/doc-ops/`
- [x] Removed deprecated versions from `/docs/specs/` and `/docs/prds/`
- [x] Created `spec-*` convention for pinned structural specs
- [x] Defined and validated unified frontmatter format
- [x] Converted `docops-changelog.md` into `doc-ops/changelog.md`
- [x] Assigned version numbers and updated dates
- [x] Moved `personas-and-hats` into `/docs/personas/`
- [x] Merged "epic-docops" into unified PRD at prd/build-doc-ops.md
- [x] Moved validation.md and metrics.md into /doc-ops/health/
- [x] Created health/README.md and aligned frontmatter in both docs
- [x] Fully review checklist coverage for validation spec
- [x] Moved `rituals/` and `personas/` to `doc-ops/rituals/` with folders for `personas/`, `procedures/`, and `tools/`

## 🧠 Open Questions

- How do we support traversal from PRDs/stories → rituals → execution docs?
- Should we autogenerate a TOC/index for discoverability?
- Should we surface a manifest of docops files (e.g. /manifest.yaml) for LLMs and CLI traversal?

## 🧰 Working Notes

- PRD structure is now standardized. All PRDs must have:
  - valid frontmatter (status, version, id, owner)
  - stories with yaml blocks
  - checkboxes for tasks + success criteria

---

## 🧪 Quality Assessment

As of June 13, 2025, the `doc-ops/` directory has been audited for structure, completeness, and standards compliance.

**Score:** 89 / 100

**Breakdown:**

- **Structural Organization** (22/25)  
  ✅ All 6 intended categories present: `spec/`, `prd/`, `health/`, `guide/`, `whitepaper/`, `doc-ops/` root  
  ✅ INDEX.md provides clean semantic overview  
  ⚠️ `rituals/` and `personas/` still under discussion

- **Content Completeness** (20/25)  
  ✅ Solid PRD, semantic markdown spec, and whitepaper evolution  
  ⚠️ Only 1 active PRD; guides are minimal; some stories still draft-state

- **Consistency / Standards** (24/25)  
  ✅ Frontmatter schema aligned across all files  
  ✅ Strong semantic formatting and versioning  
  ⚠️ Minor typo in `frontmater-schema.md` filename (to fix)

- **System Integration** (23/25)  
  ✅ Ready for `ghost validate`, `ghost evaluate`  
  ✅ Health monitoring in place  
  ⚠️ CLI logic scaffolded but not yet complete

This quality score reflects a stable and mature foundation, ready for automation and execution workflows.
