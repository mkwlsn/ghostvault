---
title: Emit JSON for Linear
type: tool
id: wishlist-003
status: wishlist
version: 0.1
owner: ghostOS
updated: 2025-06-13
tags: [linear, json, integration, export]
description: Export PRD stories and tasks to Linear-compatible JSON format
---

# 🎯 Purpose

Convert any valid semantic markdown PRD into a JSON format compatible with Linear or other agent-based issue trackers.

# 🔧 Prompt

> read a PRD `.md` file
> extract epic title, stories, tasks, and success criteria
> output a JSON array of issues with structured data for:
> - title
> - description
> - tags
> - effort or priority (if present)
