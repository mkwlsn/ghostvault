---
title: unified-docops-system
version: 1.0
status: draft
owner: mike
description: unified documentation and planning system for ghostOS development
---

# 📘 Unified DocOps System

The Unified DocOps System standardizes how planning, documentation, and task execution are encoded and understood within the ghostOS project. It enables:
- Human-readable, Git-native planning workflows
- Seamless LLM parsing, interpretation, and execution
- Synchronization with external tools like Linear, GitHub, and internal agents

## 🔧 Key Features

- **Semantic Markdown PRD Spec**: Flexible, LLM- and Git-friendly planning format
- **Agent Personas**: Ritualized roles like product owner, systems engineer, solution architect
- **DocOps Readmes**: Per-folder human-facing explainers
- **Planning + Action Duality**: All documentation can double as execution substrate

## 📂 Directory Layout

```
/docs/
  specs/
    semantic-markdown-spec.md
    unified-docops-system.md
  personas/
    product-owner.md
    systems-engineer.md
    ...
  rituals/
    simulate-product-owner.md
    simulate-systems-engineer.md
    ...
```

## 📌 Planning Principles

- Every plan is a working doc and an execution contract.
- Contributors and agents should be able to reason across context depth and time.
- Nothing lives in isolation—reference across the system is expected and encouraged.

## ✅ Success Criteria

- Docs are parseable, linked, and usable by both humans and agents
- Persona rituals exist and simulate judgment calls
- Git integration is seamless
- No doc ever needs to be rewritten when adding automation

---

## 🧠 Rationale

Creating a unified system for planning and documentation:
- Reduces cognitive switching for human contributors
- Prevents planning drift across tools
- Enables downstream automation without premature optimization
