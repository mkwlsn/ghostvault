---
title: PRD Linter
type: tool
id: wishlist-001
status: wishlist
version: 0.1
owner: ghostOS
updated: 2025-06-13
tags: [linting, validation, spec-compliance]
description: CLI tool to validate PRD structural compliance and formatting
---

# 🎯 Purpose

Ensure all semantic markdown PRDs are structurally valid and follow the unified spec.

# 🔧 Prompt

> generate a CLI tool (`lint-prd.py`) that checks each PRD file for:
> - required frontmatter fields
> - presence + format of STORY sections
> - fenced `yaml` blocks inside stories
> - formatting rules (emoji headings, bullets, etc.)
> output a success/fail summary per file with human-readable errors
