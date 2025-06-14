---
title: docops-changelog
type: changelog
version: 1.0
status: active
owner: ghost
updated: 2025-06-13
description: All notable changes to the GhostOS documentation system, including specs, PRDs, and infrastructure
---

# 📓 DocOps Changelog

All notable changes to the semantic documentation system will be tracked in this file.

---

## [2025-06-13] doc-ops system stabilized

- Created narrative onboarding doc at `doc-ops/README.md` to guide new contributors
- Clarified purpose of `INDEX.md` as structural map, not onboarding path
- Linked `README.md` from `INDEX.md` as recommended starting point
- Finalized and documented reading path for core spec, roadmap, and rituals

- Replaced outdated naming patterns (`--*.md`) with clean semantic filenames
- Updated `INDEX.md`, directory tree, and internal references to match new structure
- Added frontmatter to all previously missing files
- Promoted INDEX to stable, versioned canonical index
- Verified and cleaned references in spec/unified-docops-system.md

## [2025-06-12] semantic markdown PRD system v1.0

- Finalized markdown + YAML hybrid spec
- Defined story/task structure with fenced blocks
- Established success criteria formatting
- Validated LLM compatibility via GPT + Claude
- Integrated spec with `/doc-ops/spec/changelog.md`, `/doc-ops/prds/`, and `/doc-ops/personas/`

---

## [2025-06-11] docops persona + ritual delivery

- Generated structured markdown for 9 personas
- Bundled and zipped 5 evaluation rituals
- Created simulation-ready CLI and doc templates
- Authored persona README and ritual README in `/doc-ops/personas/` and `/doc-ops/rituals/`

---

## [2025-06-11] docops PRD + validator strategy

- Authored `epic-docops-prd.md` in `/doc-ops/prds/` and linked to semantic spec
- Outlined schema validation, ID registry, and structure parsing
- Scoped downstream tools for `ghost validate`, `ghost simulate`, and `ghost commit`

---

## [2025-06-11] docops planning pivot (semantic-surge)

- Scoped full documentation infrastructure as XL feature
- Defined long-term value and integration strategy
- Prioritized spec-first approach to bootstrap AI-native workflows
