---
title: docops-roadmap
version: 2.0
status: active
owner: ghost
updated: 2025-06-12
description: Structured roadmap for the DocOps runtime system in ghostOS.
---

# 🛣️ DocOps Roadmap v2.0

Outlines the design, buildout, and execution sequence for the semantic documentation and planning layer in ghostOS.

---

## ✅ Phase 1 — Bootstrap (COMPLETE)

- [x] Defined semantic markdown PRD spec (v1.0)
- [x] Authored `build-docops.md` with scoped roadmap + stories
- [x] Created canonical persona definitions for simulation
- [x] Exported ritual stubs for core planning affordances
- [x] Initialized `/ghost/doc-ops/` as system runtime surface
- [x] Integrated vault snapshot with synced local dev

---

## 🔄 Phase 2 — Runtime Integration (ACTIVE)

- [ ] Migrate all PRDs into `/ghost/doc-ops/prd/` with canonical frontmatter
- [ ] Relocate spec to `/ghost/doc-ops/spec/semantic-markdown.md`
- [ ] Scaffold `/ghost/doc-ops/schema/types.yaml` for validation engine
- [ ] Patch ghost CLI with `ghost plan`, `ghost simulate`, `ghost evaluate`
- [ ] Enable bundling logic for epics, stories, and tasks
- [ ] Output traceable log entries per PRD object via CLI

---

## 🧪 Phase 3 — Simulation & Planning Loop

- [ ] Simulate planning using persona rituals
- [ ] Evaluate ghost/Claude alignment on structured PRDs
- [ ] Perform meta-evaluations on roadmap accuracy
- [ ] Trigger multi-agent task queues from PRD surface

---

## 🛰️ Phase 4 — Contributor Enablement

- [ ] Author `CONTRIBUTING.md` for PRD-based workflows
- [ ] Publish example epics and story bundles
- [ ] Generate index view for all docops modules
- [ ] Define versioning policy and changelog format
- [ ] Validate local dev + agent onboarding flow

---

## 📈 Phase 5 — Externalization + Interop

- [ ] Open source docops runtime
- [ ] Add support for Linear/GitHub sync rituals
- [ ] Integrate cross-agent simulation runner
- [ ] Document handoff format for external systems
- [ ] Enable web-accessible dashboards and CI validation

---

## Meta

This roadmap is a versioned PRD and governed by the docops system itself.  
Filepath: `/ghost/doc-ops/spec/roadmap.md`
