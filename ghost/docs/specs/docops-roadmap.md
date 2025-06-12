---
title: docops-roadmap
version: 1.0
status: active
owner: ghost
---

# 🛣️ DocOps Roadmap

Defines the sequencing, priorities, and delivery flow for semantic documentation infrastructure in ghostOS.

---

## ✅ Phase 1 — Bootstrap (COMPLETE)

- [x] Define semantic markdown PRD spec
- [x] Structure /docs/specs, /docs/prds, /docs/personas
- [x] Author `epic-docops-prd.md` and core planning stories
- [x] Generate canonical persona docs (PO, SE, Philosopher, etc)
- [x] Bundle and export rituals for simulation layer
- [x] Write docops readme, changelog, and internal doc structure
- [x] Validate handoff to local vault integration

---

## 🔄 Phase 2 — Internal Integration (WIP)

- [ ] Enable ghost parsing of semantic PRDs
- [ ] Add ghost CLI rituals: `ghost plan`, `ghost evaluate`, `ghost simulate`
- [ ] Build validator for YAML + markdown structural sanity
- [ ] Wire CLI to output logs + traceable ID-based events
- [ ] Integrate ghost queue with PRD context resolution

---

## 🧪 Phase 3 — Testing & Simulation

- [ ] Simulate planning using bundled rituals
- [ ] Trigger persona evaluations on live epics
- [ ] Evaluate LLM response alignment to PRD structure
- [ ] Test multi-agent coordination: ghost ↔ claude
- [ ] Track roadmap drift using `ghost status`

---

## 🛰️ Phase 4 — Externalization

- [ ] Define contributor PRD template (`CONTRIBUTING.md`)
- [ ] Add ghost documentation index generator
- [ ] Publish reference spec for use in Arcanahaus or other systems
- [ ] Tag open source ready status

---

## 📈 Future Enhancements

- [ ] DocOps dashboard (local/hosted)
- [ ] GitHub Action to validate PRD changes
- [ ] Linear/GitHub sync script using story IDs
- [ ] Cross-agent simulation matrix runner

---

## Meta

The DocOps roadmap is itself a live PRD, governed by the same spec.  
Tracked in `/docs/specs/docops-roadmap.md` and referenced by ghost runtime.
