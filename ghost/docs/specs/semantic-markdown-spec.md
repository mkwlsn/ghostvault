---
title: Semantic Markdown PRD Spec
version: 1.0
status: stable
owner: ghost
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
    - regular `-` bullets for tasks & success criteria  

---

## ✨ example layout

```markdown
---
title: epic‑autonomy
epic_id: autonomy‑001
status: active
version: 0.3
owner: mike
threshold: true
---

# epic: autonomy

ghost becomes a background process with memory, task awareness, and execution capability.

## 🧩 story: persistent system state

```yaml
id: autonomy‑state
status: threshold‑blocker
effort: 3h
tags:
  - state
  - memory
  - introspection
```

- define ghost_state schema  
- implement file‑backed persistence  
- create cli for `ghost show/edit state`

**success criteria**  
- ghost retains memory across runs  
- state file is human‑editable & validated  
```

---

## ✅ benefits

- markdown stays readable **and** git‑friendly  
- front‑matter can be extracted for dashboards  
- fenced yaml blocks enable trivial per‑story parsing  
- supports ai task runners & autonomous agents  
- clear boundaries between metadata and prose  

---

## 🧠 future extensions

- optional `rationale:` or `objective:` fields in story yaml  
- `dependencies:` field for story/epic graphing  
- localizable aliases for headings & keys  
