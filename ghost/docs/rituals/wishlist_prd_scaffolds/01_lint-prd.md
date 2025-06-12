---
title: PRD Linter
id: wishlist-001
status: wishlist
owner: ghostOS
tags: [linting, validation, spec-compliance]
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
