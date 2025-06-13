---
title: "README"
type: guide
owner: ghostOS
updated: 2025-06-13
description: "Narrative entrypoint into the doc-ops subsystem—what it enables, how it works, and why it matters."
tags: [docops, onboarding, learning-path, guide]
---

# 📚 understanding doc-ops (the documentation system of ghostOS)

ghostOS isn’t just code—it’s a system that documents, evaluates, and evolves itself.

the `/doc-ops/` subsystem is how that happens.

this guide explains:

1. **what doc-ops enables** – rituals, personas, structured documentation, self-evaluation  
2. **how it enables it** – semantic markdown, scoped schemas, validation tools, roadmap scaffolding  
3. **why it matters to you** – because ghostOS reasons through documents. understanding doc-ops is how you understand *how it thinks*

---

## 🧭 recommended reading path

### 1. Start Here – Foundation (15 min)  
*Begin with the what, why, and where.*

- [📄 `INDEX.md`](./INDEX.md) — *Directory map + top-level orientation*
- [📄 `unified-docops-system.md`](./spec/unified-docops-system.md) — *Why doc-ops exists and what it standardizes*
- [📄 `changelog.md`](./changelog.md) — *Recent progress and structural evolution*

---

### 2. Core Concepts (20 min)  
*Understand how ghostOS reads and reasons about documents.*

- [📄 `semantic-markdown.md`](./spec/semantic-markdown.md) — *How markdown becomes executable knowledge*
- [📄 `README.md`](./rituals/README.md) — *How rituals and personas evaluate documents*
- [📄 `docops-roadmap.md`](./docops-roadmap.md) — *Phase-based plan for building and stabilizing doc-ops*

---

### 3. Practical Understanding (25 min)  
*See how it works in context.*

- [📄 `build-doc-ops.md`](./prd/build-doc-ops.md) — *A real PRD that walks through doc-ops implementation*
- [📄 `product-owner.md` (persona)](./rituals/persona/product-owner.md) — *An example of role-based evaluation*
- [📄 `product-owner.md` (procedure)](./rituals/procedure/product-owner.md) — *A procedural walk through a documentation task*

---

### 4. Deep Dive (30 min)  
*The system’s philosophy, implementation path, and QA layer.*

- [📄 `ghostOS_doc_ops_whitepaper_v0.3.md`](./whitepaper/ghostOS_doc_ops_whitepaper_v0.3.md) — *Strategic vision + architectural foundation*
- [📄 `validation.md`](./health/validation.md) — *QA model for semantic doc health*
- [📄 `ghostOS_implementation_playbook.md`](./guide/ghostOS_implementation_playbook.md) — *How to deploy ghostOS in your own system*

---

## 🎯 Quick Navigation by Intent

| If you want to...                     | Read this                                      |
|--------------------------------------|------------------------------------------------|
| Understand what doc-ops *is*         | [`unified-docops-system.md`](./spec/unified-docops-system.md) |
| See how it's implemented             | [`build-doc-ops.md`](./prd/build-doc-ops.md)   |
| Learn how it evaluates documents     | [`README.md`](./rituals/README.md)             |
| Understand system health + QA        | [`validation.md`](./health/validation.md)      |
| See where it’s going next            | [`docops-roadmap.md`](./docops-roadmap.md)     |

---

## 🚀 Shortcut: 10-Minute Orientation

Read these 3 files if you want the fast take:

1. [📄 `INDEX.md`](./INDEX.md)
2. [📄 `build-doc-ops.md`](./prd/build-doc-ops.md)
3. [📄 `docops-roadmap.md`](./docops-roadmap.md)

That’ll give you the map, an example, and a sense of trajectory.

---
