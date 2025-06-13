---
title: rituals
type: overview
status: active
version: 1.1
owner: mike
updated: 2025-06-13
description: Defines the symbolic execution layer of GhostOS through personas, procedures, and tools for evaluating and simulating system evolution
---

# 🧠 Ritual System Overview

This directory defines the symbolic execution layer of GhostOS. It contains rituals, personas, and tools that simulate how distributed roles contribute to evaluating, shaping, and evolving a system like Ghost.

## 🧾 Directory Structure

This ritual system follows a semantic structure where path context defines purpose:

```
/rituals/
├── README.md                    # System overview (you are here)
├── INDEX.md                     # File inventory and directory map
├── personas/                    # Role definitions (WHO)
│   ├── product-owner.md
│   ├── systems-engineer.md
│   ├── communications-architect.md
│   ├── ai-ethicist.md
│   ├── design-ops.md
│   ├── open-source-steward.md
│   └── systems-philosopher.md
├── procedures/                  # Ritual instructions (HOW)
│   ├── product-owner.md
│   ├── systems-engineer.md
│   ├── communications-architect.md
│   ├── design-ecologist.md
│   └── product-philosopher.md
└── tools/                       # CLI specifications (WHAT)
    ├── lint-prd.md
    ├── plaintext-to-prd.md
    ├── emit-json-for-linear.md
    ├── persona-reviewer.md
    └── ghost-scribe-cli.md
```

Each subdirectory represents a semantic dimension of the ritual system:

- **`personas/`** — Defines symbolic actors (WHO) such as product-owner, systems-philosopher, or design-ops. These files define motivations, responsibilities, and key questions.
- **`procedures/`** — Contains evaluative rituals (HOW) associated with each persona. These are practical, simulation-ready playbooks used to test ideas and features from distinct vantage points.
- **`tools/`** — Defines CLI commands or automation helpers (WHAT) that implement, lint, or transform artifacts referenced in rituals.

## 📐 Rationale

GhostOS rituals are not role-play. They are symbolic tools for surfacing blind spots and systemic pressure. Each persona embodies a voice in the system that can be invoked through simulation.

By pairing **procedures** with **personas**, we create structured, repeatable methods for evaluating whether a change supports the long-term coherence of the system.

## 🌀 Usage

- `ghost simulate persona product-owner`
- `ghost execute procedure design-ecologist`
- `ghost use tool ghost-scribe-cli`

## 🌱 Status

All content in this directory is active and under development. Once validated, selected rituals will be promoted to `ghost/rituals/` as canonical execution layers.
