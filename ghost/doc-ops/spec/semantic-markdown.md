---
title: Semantic Markdown PRD Spec
type: spec
version: 1.1
status: stable
owner: ghost
updated: 2025-06-13
---

# Semantic Markdown Spec v1.0

this document defines a semantic markdown convention optimized for:

- human readability in editors and git diffs
- machine parseability for llm agents
- git‑based doc‑ops and version control
- seamless integration with cli task runners & agent workflows

---

## 📐 structure overview

1. **yaml front‑matter** — global metadata for the prd
2. **markdown headings** — logical document structure
3. **story sections**  
     - `## 🧩 story: {{title}}` as heading  
     - fenced `yaml` block for story metadata  
     - regular `-` bullets for narrative or informational items  
     - `[ ]` checkboxes MUST be used for tasks or success criteria that can be completed or verified  
     - **note:** Any list item representing a binary condition **must** be written as a checkbox `[ ]` to enforce semantic clarity.

---

## 🧱 canonical types

The spec defines a set of canonical types to structure the documentation and workflows consistently. Each type has a defined format and purpose:

- **epic**: Top-level container representing a large feature or initiative. Typically includes frontmatter with `title`, `id`, `status`, `owner`, and optional fields like `version` or `threshold`.
- **story**: A unit of work or feature within an epic. Denoted by `## 🧩 story: {{title}}` headings with a fenced YAML block containing metadata.
- **task**: Individual actionable items, usually listed as bullet points under stories.
- **ritual**: Recurring tasks or procedures, documented similarly to stories but denoting repeated workflows.
- **bundle**: A collection of related stories or tasks grouped together, identified by a `bundle_id`.
- **insight**: Notes, learnings, or observations that provide context or rationale, often included as prose or metadata.

---

## 🧾 frontmatter schema

The following fields are part of the canonical frontmatter schema used across all GhostOS documentation. These fields enable consistent parsing, lifecycle tracking, and CLI integration.

### 🧩 Core Schema (All Documents)

- `title`: Human-readable title of the document
- `type`: Classification of the document (e.g. `spec`, `prd`, `health`, `whitepaper`, `guide`, `planning`)
- `status`: Lifecycle status (`draft`, `active`, `stable`, `deprecated`, `archived`)
- `version`: Semantic version (e.g. `1.0`)
- `owner`: Responsible party or system (e.g. `ghost`)
- `updated`: Last modification date (`YYYY-MM-DD`)

### 🔁 Type-Specific Fields

#### PRDs and Stories

- `id`: Unique identifier (e.g. `frontmatter-unification`)
- `epic_id`: Optional link to parent epic or initiative
- `bundle_id`: Related grouping of stories/tasks
- `authors`: List of contributors
- `created`: Original authorship date
- `tags`: List of relevant keywords

#### Specs and Health Docs

- `invokes`: CLI command this document connects to (e.g. `ghost validate`)
- `audience`: List of target users (`contributor`, `ci`, `operator`, etc.)
- `description`: Optional summary of purpose

#### Whitepapers

- `stage`: `pre-threshold`, `active`, or `post-threshold`
- `purpose`: Strategic intent or objective
- `supersedes`: Reference to document it replaces

---

## status values

The `status` field must be one of the following standardized values:

- `draft`: The item is in an incomplete or speculative state. Not ready for active work.
- `active`: The item is ready to be picked up, but no work has started yet.
- `in-progress`: Work has begun; some checklist items are complete but not all.
- `complete`: All checklist items are finished and verified.
- `threshold`: A blocker or decision gate—work cannot proceed until this is cleared.
- `shipped`: Work is fully complete and has been deployed, published, or delivered.
- `deprecated`: No longer in use or relevant. Retained for historical or reference reasons.

---

## fenced YAML block parsing

Fenced YAML blocks are used to provide structured metadata within story sections. These blocks:

- Follow a `## 🧩 story: {{title}}` heading
- Are enclosed in triple backticks with `yaml` specified
- Contain key-value pairs that describe story attributes such as `id`, `status`, `effort`, and `tags`
- Enable automated parsing by tools to extract story metadata separately from prose and task lists
- **Note:** If a list item represents a binary condition (e.g., a task or success criterion that can be completed or verified), it **must** be written using `[ ]` checkboxes to enforce semantic clarity.

---

## ✅ benefits

- markdown stays readable **and** git‑friendly
- front‑matter can be extracted for dashboards
- fenced yaml blocks enable trivial per‑story parsing
- supports ai task runners & autonomous agents
- clear boundaries between metadata and prose
- enforces visual and semantic clarity through checkbox usage

---

## 🧠 future extensions

- optional `rationale:` or `objective:` fields in story yaml
- `dependencies:` field for story/epic graphing
- localizable aliases for headings & keys

---

## lifecycle rules

The lifecycle status of stories and epics can be automatically updated based on checklist progress within each story section. For example:

- When no checklist items are checked, status remains `active`.
- When some checklist items are checked but not all, status updates to `in-progress`.
- When all checklist items are checked, status updates to `complete`.

This checklist-driven logic ensures the semantic markdown reflects the current state of work without manual status edits, improving accuracy and reducing overhead.

---

## 🧪 schema validation

To enforce structural integrity and consistency, a JSON Schema or Pydantic schema is used to validate the semantic markdown files. Validation ensures required fields are present, values conform to expected types and enums, and relationships between items are maintained.

A CLI tool, `ghost validate prd path/to/file.md`, is provided to run validation checks on PRD files, reporting errors and warnings to assist authors in maintaining compliance with the spec.

**Note:** The validation process also supports the automatic updating of lifecycle statuses based on checklist completion, enabling dynamic and accurate tracking of work progress within the markdown documents.
