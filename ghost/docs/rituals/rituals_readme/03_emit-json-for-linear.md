---
title: Emit JSON for Linear
id: wishlist-003
status: wishlist
owner: ghostOS
tags: [linear, json, integration, export]
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
