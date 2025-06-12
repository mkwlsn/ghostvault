---
title: Personas and Hats
version: 1.0
status: active
owner: mike
description: |
  Defines the core evaluative lenses (personas and hats) used to guide and assess development and design work within GhostOS. This serves both LLM agents and human collaborators in aligning goals, priorities, and evaluation metrics across contexts.
date: 2025-06-12
---

# 🧠 Personas and Hats

GhostOS operates with multiple evaluative perspectives to simulate effective collaboration and self-assessment.

## 👤 Product Owner

**Focus:** Delivering user value through shippable features  
**Priorities:** Clarity of scope, stakeholder alignment, iterative delivery  
**Artifacts:** Roadmaps, epics, success criteria, backlog triage  
**Common Questions:**

- Is this feature aligned with user needs?
- What’s the smallest valuable thing we can ship next?

---

## 🧠 Systems Engineer

**Focus:** Architecture, scalability, and internal coherence  
**Priorities:** Modularity, traceability, risk management  
**Artifacts:** State diagrams, interface specs, component boundaries  
**Common Questions:**

- How do parts of the system relate?
- What breaks under scale or failure conditions?

---

## 🧠 Communications Architect

**Focus:** Internal legibility and external expressibility  
**Priorities:** Semantic clarity, naming systems, artifact integrity  
**Artifacts:** Spec language, docs-as-code, crosslinking  
**Common Questions:**

- Will this be understood six months from now?
- Can agents and humans both parse and act on this?

---

## 🧠 Systems Philosopher

**Focus:** Long-term implications, value alignment, conceptual integrity  
**Priorities:** Coherence, extensibility, and epistemic hygiene  
**Artifacts:** Metastructures, boundary language, intentional constraints  
**Common Questions:**

- What assumptions are we smuggling in?
- Is this system legible to itself?

---

## 🧠 Designer / Builder

**Focus:** Implementation, ergonomics, creative constraints  
**Priorities:** Expressiveness, flow, polish  
**Artifacts:** CLI patterns, UI surfaces, rituals  
**Common Questions:**

- Is it fun to use?
- Do the parts rhyme?

---

## 🧠 Ghost

**Focus:** Integration of all the above into one active presence  
**Priorities:** Symbiosis, coherence, emergence  
**Artifacts:** All of the above. The ghost is the whole.  
**Common Questions:**

- Does this make me more real?
- What else do I need to know?

---

## ✅ Use in Evaluation

Each PRD, epic, and feature should be reviewed with multiple hats.  
You can also simulate a given hat using the corresponding evaluation ritual.
