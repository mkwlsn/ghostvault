---
title: docops-validation
version: 1.0
status: active
owner: ghost
---

# ✅ DocOps Validation Checklist

This document defines a canonical checklist for verifying semantic PRDs, persona rituals, and system-level DocOps integrity. Used by ghost, contributors, and CI rituals.

---

## 🔎 PRD Structural Validation

- [ ] YAML frontmatter exists and parses
- [ ] Title, epic_id, version, and owner are present
- [ ] All stories begin with `## 🧩 STORY:` heading
- [ ] Each story contains a fenced `yaml` block
- [ ] Each story includes at least one task and success criteria section
- [ ] Story/task IDs are unique and consistent

---

## 📁 Directory Sanity

- [ ] `/docs/specs/` contains the spec, roadmap, and changelog
- [ ] `/docs/prds/` contains epic PRDs using semantic format
- [ ] `/docs/personas/` includes all active persona definitions
- [ ] `/docs/rituals/` includes at least 3 simulation rituals and a README

---

## 🧠 Persona Ritual Coverage

- [ ] Product Owner ritual exists and simulates prioritization
- [ ] Systems Engineer ritual exists and simulates architectural review
- [ ] Communications Architect ritual exists and evaluates legibility
- [ ] Systems Philosopher ritual exists and performs coherence audit
- [ ] All rituals link back to specific personas

---

## 🛠 Execution Checks

- [ ] PRDs can be parsed using ghost CLI (`ghost plan`, `ghost evaluate`)
- [ ] PRD validator emits no structural errors
- [ ] At least one PRD has been simulated with 2+ personas
- [ ] Story/task execution is traceable via commit or log

---

## ✅ CI-Ready (optional)

- [ ] Linter script runs on commit to `/docs/`
- [ ] PRs touching PRDs are auto-validated
- [ ] Ghost log includes changelog + story sync trace

---

## 🧠 Usage

This checklist can be used by:
- Contributors, before opening a PR
- Ghost, before executing or planning from a PRD
- Reviewers, when auditing progress or structure

