---
title: epic-docops
epic_id: docops-001
status: active
version: 0.1
owner: mike
threshold: false
---

# Epic: DocOps

establish a robust documentation operations system that enables ghostOS to produce, interpret, and evolve its own semantic documentation — readable by humans, parseable by models, and integrable with external PM tools.

---

## 🧩 STORY: define semantic markdown spec

```yaml
id: docops-semantic-spec
status: complete
effort: 2h
tags: [spec, markdown, format]
```

- formalize a markdown-based PRD/document format for dual consumption (human + model)
- include metadata via yaml frontmatter and fenced yaml blocks
- validate against common markdown renderers

**Success Criteria**
- spec supports all use cases from ghostOS PRDs
- no formatting breaks in major markdown parsers (e.g., VSCode, GitHub, Obsidian)

---

## 🧩 STORY: establish /docs folder conventions

```yaml
id: docops-folder-structure
status: planned
effort: 1h
tags: [structure, conventions]
```

- create canonical folder structure for /docs
- include `/specs`, `/prds`, `/personas`, `/rituals`, `/references`
- ensure compatibility with existing git + vault workflows

**Success Criteria**
- markdown documents properly grouped and discoverable
- clear folder purpose documentation in README.md

---

## 🧩 STORY: publish sample PRDs

```yaml
id: docops-seed-prds
status: planned
effort: 1h
tags: [samples, ghostvault]
```

- publish fully annotated examples of:
  - epic-bootstrap
  - epic-autonomy
  - epic-threshold
- include commentary inline or in appendix

**Success Criteria**
- 3 PRD examples visible in `/docs/prds`
- markdown renders correctly in GitHub and Obsidian

---

## 🧩 STORY: ghost interpretive rituals

```yaml
id: docops-rituals
status: planned
effort: 3h
tags: [rituals, parsing, validation]
```

- write scripts/rituals to read semantic markdown files
- extract metadata, parse stories, validate structure
- output normalized object or emit CLI warnings

**Success Criteria**
- CLI call parses and validates target PRD
- errors on malformed or incomplete spec blocks

---

## 🧩 STORY: simulation personas

```yaml
id: docops-simulated-personas
status: planned
effort: 2h
tags: [personas, simulation]
```

- define ritual inputs/personas for:
  - systems engineer
  - product owner
  - comms architect
- generate opinionated evaluations of current roadmap

**Success Criteria**
- ghost can simulate each persona on PRDs
- output includes rationale, prioritization, risks

