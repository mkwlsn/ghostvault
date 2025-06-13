---
title: Frontmatter Schema
type: spec
status: stable
version: 1.1
owner: ghost
updated: 2025-06-13
invokes: ghost validate frontmatter
audience: [contributor, ci, system]
---

# 🧾 Frontmatter Schema

This document defines the canonical frontmatter structure for all documentation files in the GhostOS system. It ensures structural consistency, supports CLI automation, and enables lifecycle and type-based workflows.

---

## 🎯 Core Schema (Required for All Docs)

| Field     | Type   | Description                                   |
| --------- | ------ | --------------------------------------------- |
| `title`   | string | Human-readable document title                 |
| `type`    | enum   | Classification (`spec`, `prd`, `guide`, etc.) |
| `status`  | enum   | Lifecycle status (`draft`, `active`, etc.)    |
| `version` | string | Semantic version (e.g. `1.0`)                 |
| `owner`   | string | Responsible agent or author                   |
| `updated` | string | Last modified (YYYY-MM-DD)                    |

---

## 🧩 Type-Specific Extensions

### For PRDs and Stories

- `id`: unique identifier
- `epic_id`: optional parent epic
- `bundle_id`: groupings for related work
- `authors`: contributors list
- `created`: creation date
- `tags`: topic labels

### For Health Docs and Specs

- `invokes`: CLI command this file connects to
- `audience`: intended users or agents
- `description`: summary of purpose

### For Whitepapers

- `stage`: `pre-threshold`, `active`, `post-threshold`
- `purpose`: strategic objective
- `supersedes`: ID of document replaced

### For Personas

- `mode`: either `symbolic` (conceptual anchor) or `operational` (used in simulation)

---

## 🔒 Validation Rules

- All docs MUST include the core schema
- `status` must use canonical values
- `version` must be semver format
- `updated` must use YYYY-MM-DD
- `type` must match directory context
- `mode` is required for `type: persona` and must be either `symbolic` or `operational`

---

## ✅ Enforcement

- `ghost validate frontmatter` runs compliance checks
- CI can block merges for invalid metadata
- LLMs and bots use this schema to evaluate, sort, or act on docs
