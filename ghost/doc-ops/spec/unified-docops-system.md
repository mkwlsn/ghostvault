---
title: unified-docops-system
version: 1.1
status: stable
owner: mike
description: unified documentation and planning system for ghostOS development
updated: 2025-06-12
---

# 📘 Unified DocOps System

The Unified DocOps System standardizes how planning, documentation, and task execution are encoded and understood within the ghostOS project. It supports:

- Human-readable, Git-native planning workflows
- Seamless LLM parsing, interpretation, and execution
- Synchronization with external tools (e.g. Linear, GitHub)
- Interoperability with persona rituals and CLI-driven workflows

---

## 🔧 Key Features

- **Semantic Markdown PRD Spec**  
  Lintable, agent-friendly planning format in Markdown

- **Agent Personas**  
  Ritualized judgment protocols for roles like product owner, systems engineer, and others

- **DocOps Specs**  
  Machine- and human-readable specifications for validation and intent

- **Checklist-Driven Validation**  
  Ritual and CLI-compatible system health verification

- **Planning ↔ Action Duality**  
  All documentation is structured to support both reading and execution

- **LLM-Aware Pathing and Structure**  
  Predictable file layout and naming conventions to reduce cognitive overhead

---

## 📂 Directory Layout

@ghost: check for updates, this section is a living part of the doc

```
/ghost/doc-ops/
  INDEX.md
  changelog.md
  docops-roadmap.md
  prd/
    build-doc-ops.md
    frontmatter.md
  spec/
    semantic-markdown.md
    unified-docops-system.md
    frontmatter-schema.md
  health/
    README.md
    validation.md
    metrics.md
  guide/
    ghostOS_implementation_playbook.md
  whitepaper/
    ghostOS-familiarity-whitepaper.md
    ghostOS-introspection-whitepaper.v0.1.md
    ghostOS-introspection-whitepaper.v0.2.md
    ghostOS-introspection-whitepaper.v0.3.md
    ghostOS_doc_ops_whitepaper_v0.3.md
```

---

## 📌 Planning Principles

- Every doc is both a working plan and an execution substrate
- Contributors and agents should reason across time and context
- Inter-file reference is expected and encouraged
- Binary conditions should use checkboxes `[ ]` for clarity

---

## ✅ Success Criteria

- [ ] All docs are parseable and contextually linked
- [ ] Persona rituals simulate plausible agent decision-making
- [ ] LLMs can reason over structure without prompt hacks
- [ ] Git integration supports tagging, versioning, and CLI workflows
- [ ] No doc needs to be rewritten when introducing automation

---

## 🧠 Rationale

Building a unified system for planning and documentation:

- Reduces cognitive switching for human contributors
- Prevents planning drift across tools and agents
- Enables scalable, automation-ready execution without fragility
- Establishes a durable, audit-friendly org memory
