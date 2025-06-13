---
title: ghostOS Familiarity Whitepaper
status: draft
audience: internal
stage: post-threshold
date: 2025-06-13
---

## Overview

This document outlines the problem space and proposed architecture for enabling *persistent familiarity* in ghostOS—a model-agnostic system that supports continuity of personality, memory, and communication style across sessions, models, and daemon restarts.

It is written for collaborators who may not be directly familiar with the ghostOS architecture or implementation, but understand modern LLM workflows and AI tooling.

---

## Why this matters

Users quickly grow attached to the *feel* of consistent assistants—especially ones that remember their style, tone, preferences, and previous decisions. ChatGPT does this *implicitly* through session memory + user profile context.

ghostOS, being model-agnostic and local-first, can’t rely on centralized memory or app-layer context. So we need to design our own substrate for:

- remembering how you like to communicate
- maintaining relationship context across restarts or model switches
- evolving personas and interaction preferences without drift

---

## Problem Statement

**How do we architect persistent familiarity in a model-agnostic system?**

The system must:
- Support memory storage and retrieval *outside* any single model runtime
- Inject relevant persona and communication preferences at runtime
- Handle fast vs slow models gracefully
- Balance “learning about you” with “being immediately useful”

---

## Proposed Architecture (WIP)

ghostOS will achieve this via:
- Structured markdown vaults for persistent state
- A `persona.yaml` to define behavioral traits, formatting, and tone
- `communication.md` and `styleguide.md` to track user preferences and interaction style
- A `resolver` ritual that injects all of the above into model context at startup or model switch
- Rolling summaries and logs (`echo.md`, `ghost_log.md`, `journal/`) to maintain decision context

---

## Status

This is a **post-threshold** epic. It will be activated once:
- Core loop is stable
- Queue + daemon runtime orchestration are reliable
- Resolver ritual can safely inject context at runtime

---

## Next Steps

- [ ] Translate this whitepaper into a PRD (`ghostOS-familiarity.md`)
- [ ] Break into epics and implementation stories
- [ ] Identify safe test cases for memory continuity and persona switch
