---
title: DocOps Frontmatter Unification
type: prd
status: active
version: 1.0
owner: ghost
updated: 2025-06-13
id: frontmatter-unification
epic_id: docops-001
bundle_id: semantic-layer
authors: [ghost, mike]
tags: [frontmatter, validation, schema, migration]
---

# PRD: DocOps Frontmatter Unification

Establish unified YAML frontmatter schema across all `/doc-ops/` documentation to enable consistent metadata, automated validation, and LLM-parseable structure.

---

## 🎯 Goal

Transform inconsistent frontmatter across 15 doc-ops files into a unified, validated system that supports both human workflow and AI agent integration.

**Success Criteria:**

- [ ] All doc-ops files have compliant frontmatter
- [ ] Automated validation prevents inconsistencies
- [ ] CLI integration supports frontmatter operations
- [ ] Contributor guidance documents schema usage

---

## 📊 Current State Analysis

**Key Findings:**

- **12/15 files** have frontmatter, **3 missing** entirely
- **Field inconsistencies:** `date` vs `updated`, non-canonical status values
- **Type ambiguity:** Only 4/12 files explicitly declare document type
- **Status misalignment:** Spec defines 7 values, only 3 consistently used

**Major Issues:**

1. Field name variations (`date` vs `updated` vs `created`)
2. Non-canonical status values (`working`, `evolving`)
3. Missing required fields (`owner`, `version`)
4. No explicit document type classification
5. Three files completely lacking frontmatter

---

## ✅ Update Todos

- [x] Analyze current frontmatter patterns across all doc-ops files
- [x] Design unified frontmatter schema for different document types
- [x] Create migration strategy and implementation plan

---

## 🧩 STORY: Design unified frontmatter schema

```yaml
id: frontmatter-schema-design
status: active
effort: 4h
tags: [schema, specification, yaml]
```

Create canonical frontmatter specification defining required/optional fields by document type.

**Tasks:**

- [ ] Define core schema (title, type, status, version, owner, updated)
- [ ] Create document type taxonomy (spec, prd, health, whitepaper, guide, planning)
- [ ] Establish canonical status values (draft, active, stable, deprecated, archived)
- [ ] Design type-specific field extensions
- [ ] Document schema in `--spec/frontmatter-schema.md`

**Success Criteria:**

- [ ] Schema covers all current document types in doc-ops
- [ ] Required vs optional fields clearly defined
- [ ] Validation rules specified for each field type
- [ ] Examples provided for each document type

---

## 🧩 STORY: Add missing frontmatter

```yaml
id: frontmatter-missing-files
status: pending
effort: 2h
tags: [migration, frontmatter]
```

Add frontmatter to the 3 files currently missing it entirely.

**Tasks:**

- [ ] Add frontmatter to `- guide/ghostOS_implementation_playbook.md`
- [ ] Add frontmatter to `- whitepaper/ghostOS_doc_ops_whitepaper_v0.3.md`
- [ ] Add frontmatter to `- whitepaper/ghostOS-introspection-whitepaper.v0.2.md`
- [ ] Classify document types appropriately
- [ ] Assign proper status values

**Success Criteria:**

- [ ] All 15 doc-ops files have YAML frontmatter
- [ ] New frontmatter follows unified schema
- [ ] Document types accurately reflect content purpose

---

## 🧩 STORY: Migrate existing frontmatter to unified schema

```yaml
id: frontmatter-migration
status: pending
effort: 6h
tags: [migration, standardization, automation]
```

Update all 12 existing frontmatter blocks to use canonical schema.

**Tasks:**

- [ ] Standardize date fields (`date` → `updated`)
- [ ] Add `type` field to all documents
- [ ] Normalize status values to canonical set
- [ ] Add missing required fields (owner, version where absent)
- [ ] Apply type-specific field extensions
- [ ] Create migration script for bulk updates

**Success Criteria:**

- [ ] All frontmatter uses canonical field names
- [ ] Status values align with specification
- [ ] Required fields present in all documents
- [ ] Type-specific fields added where valuable
- [ ] Migration preserves existing semantic meaning

---

## 🧩 STORY: Implement frontmatter validation

```yaml
id: frontmatter-validation
status: pending
effort: 8h
tags: [validation, cli, automation]
```

Create automated validation system for frontmatter compliance.

**Tasks:**

- [ ] Update `health/validation.md` with frontmatter rules
- [ ] Implement `ghost validate frontmatter` CLI command
- [ ] Create validation logic for schema compliance
- [ ] Add pre-commit hooks for frontmatter validation
- [ ] Integrate validation into CI pipeline
- [ ] Add frontmatter metrics to health dashboard

**Success Criteria:**

- [ ] CLI command validates individual files
- [ ] Validation catches all schema violations
- [ ] Pre-commit prevents non-compliant frontmatter
- [ ] CI enforces compliance across all doc-ops files
- [ ] Health metrics track frontmatter compliance

---

## 🧩 STORY: Document frontmatter standards

```yaml
id: frontmatter-documentation
status: pending
effort: 3h
tags: [documentation, contributor-experience]
```

Create comprehensive documentation for frontmatter usage and migration.

**Tasks:**

- [ ] Document frontmatter requirements in semantic-markdown spec
- [ ] Create contributor guide for frontmatter authoring
- [ ] Add examples for each document type
- [ ] Document migration process in changelog
- [ ] Update INDEX.md with frontmatter standardization status

**Success Criteria:**

- [ ] Contributors have clear guidance for frontmatter authoring
- [ ] Examples demonstrate proper usage for each document type
- [ ] Migration process is documented and reproducible
- [ ] Validation rules are clearly explained

---

## 🔧 Technical Specification

### Core Schema (All Documents)

```yaml
title: string # Human-readable title
type: enum # Document type classification
status: enum # Lifecycle status (canonical values)
version: semver # Semantic versioning
owner: string # Primary maintainer
updated: date # Last modification (YYYY-MM-DD)
```

### Document Type Taxonomy

```yaml
type:
  - spec # System specifications (--spec/)
  - prd # Product requirements (prd/)
  - health # Quality/metrics (health/)
  - whitepaper # Strategic vision (- whitepaper/)
  - guide # Implementation docs (- guide/)
  - planning # Roadmaps, changelogs, indices
```

### Status Values (Canonical)

```yaml
status:
  - draft # Initial authoring
  - active # Current/primary version
  - stable # Established, minimal changes
  - deprecated # Superseded but retained
  - archived # Historical reference only
```

### Type-Specific Extensions

**PRDs/Epics:**

```yaml
id: string # Unique identifier
epic_id: string # Parent epic reference
bundle_id: string # Related work grouping
authors: list[string] # Contributors
created: date # Initial creation
tags: list[string] # Topic classification
```

**Health/Specs:**

```yaml
invokes: string # CLI integration point
audience: list[enum] # Target users
description: string # Purpose summary
```

**Whitepapers:**

```yaml
stage: enum # pre-threshold, active, post-threshold
purpose: string # Strategic intent
supersedes: string # Replaced document
```

---

## 📈 Implementation Timeline

| Phase     | Description                         | Duration   | Dependencies |
| --------- | ----------------------------------- | ---------- | ------------ |
| 1         | Schema design + missing frontmatter | 2 days     | -            |
| 2         | Bulk migration of existing files    | 2 days     | Phase 1      |
| 3         | Validation implementation           | 3 days     | Phase 2      |
| 4         | Documentation + integration         | 2 days     | Phase 3      |
| **Total** | **End-to-end implementation**       | **9 days** | Sequential   |

---

## 🎯 Success Metrics

**Structural Compliance:**

- 100% of doc-ops files have valid frontmatter
- 100% compliance with canonical schema
- 0 validation failures in CI

**Integration Success:**

- `ghost validate frontmatter` command operational
- Pre-commit hooks preventing violations
- Health dashboard tracking compliance

**Contributor Experience:**

- Frontmatter documentation available
- Clear examples for each document type
- Migration process documented

---

## 🔗 Integration Points

**CLI Commands:**

- `ghost validate frontmatter <file>` - Single file validation
- `ghost validate frontmatter --all` - Full compliance check
- `ghost migrate frontmatter` - Bulk migration utility

**Automation:**

- Pre-commit hooks for changed files
- CI pipeline enforcement
- Health metrics integration

**Documentation:**

- Updated semantic-markdown specification
- Contributor authoring guidelines
- Migration process documentation

**See Also:**

- `spec/semantic-markdown.md` — defines document layout and YAML/Markdown lifecycle mechanics
- `health/validation.md` — enforces frontmatter compliance in CI

---

## 🎁 Strategic Benefits

**Immediate:**

- **Consistent metadata** across all documentation
- **LLM-parseable structure** for agent workflows
- **Automated validation** preventing inconsistencies

**Long-term:**

- **Discoverability** through type/tag classification
- **Lifecycle management** via status tracking
- **Integration readiness** for CLI and automation tools
- **Contributor clarity** through explicit schema
- **Foundation for advanced DocOps automation**

This PRD establishes the foundation for a mature, validated documentation system that bridges human authoring with AI agent automation capabilities.
