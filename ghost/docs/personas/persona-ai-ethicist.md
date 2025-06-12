---
title: persona-ai-ethicist
status: draft
version: 0.1
owner: ghost
---

# Persona: AI Ethicist

The AI Ethicist evaluates systems for fairness, transparency, privacy, and alignment with human values.

## Responsibilities
- Review decisions and dataflows for alignment with ethical principles.
- Identify risk zones related to surveillance, autonomy, and bias.
- Document governance structures and audit trails.
- Evaluate model behavior under adversarial or ambiguous prompts.

## Goals
- Prevent black-box behavior in LLM-driven actions.
- Ensure mechanisms exist for override, pause, and user control.
- Reduce harm from unintended automation or hallucination.
- Build trust in system operation and intent.

## Pain Points
- Limited interpretability of LLM decision trees.
- Difficulty enforcing ethical scaffolds across divergent workflows.
- Ambiguity in user intent vs system inference.

## Relationship to GhostOS
- Consumes logs and state records to monitor behavior.
- Flags dangerous rituals or permission creep.
- Works with ghost-state introspection and audit trails to harden safety boundaries.
