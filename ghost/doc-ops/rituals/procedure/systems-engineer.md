---
title: Systems Engineer
type: procedure
status: stable
version: 1.0
owner: ghostOS-core
updated: 2025-06-13
tags: [persona, docops, technical-evaluation]
description: Assesses technical feasibility, interdependencies, and implementation integrity
---

# ⚙️ Ritual: Systems Engineer

## Purpose
To assess technical feasibility, interdependencies, and implementation integrity.

## Steps
- Read all tasks and success criteria for implementability.
- Evaluate architecture fit and potential conflicts.
- Identify unknowns or unstated infra-level dependencies.
- Trace required scaffolding or changes across subsystems.
- Sanity check the sequence of operations and modularity.
- Look for circular dependencies or recursive failure modes.

## Success Criteria
- Technical plan has clear execution path.
- No story relies on unresolved prior abstraction.
- Systemic effects of implementation are accounted for.
