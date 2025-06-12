---
title: epic-babelfish
epic_id: babelfish-001
status: planned
version: 0.1
owner: mike
threshold: false
---

# Epic: Babelfish

ghostOS supports multiple vocabularies or “themes” for commands and documentation. Contributors can write rituals, stories, and commands using alternate terms that are translated to canonical ghostOS terms during execution or contribution workflows.

## 🧩 STORY: implement theme translation layer

```yaml
id: babelfish-translate
status: planned
effort: 6h
tags: [i18n, themes, vocabulary]

Tasks:
  - define a canonical term taxonomy (term, dir, ritual, etc)
  - create a theme config file format (YAML or JSON)
  - implement translation layer in CLI
  - update help system to use canonical names, with theme aliases as hover/tip

Success Criteria:
  - contributors can use an alternate vocabulary
  - ghostOS resolves to canonical internally
  - CLI errors and help reference both forms
```

## 🧩 STORY: contributor patching workflow

```yaml
id: babelfish-patch
status: planned
effort: 4h
tags: [contrib, vocabulary, tooling]

Tasks:
  - create CLI tooling for validating theme terms
  - add contributor flow to auto-translate theme language to canonical
  - write basic validator tests
  - patch final PR with canonical vocabulary prior to merge

Success Criteria:
  - contributors can submit in theme-specific language
  - ghost auto-patches to canonical before merge
  - validation errors are clear and fixable
```

## 🧠 why this matters:

- improves ergonomics for contributors
- supports localization and onboarding paths
- unlocks themed forks (e.g. normieOS) with minimal disruption

