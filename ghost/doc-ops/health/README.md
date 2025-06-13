# 🩺 DocOps Health Monitoring

This directory contains the key documents for evaluating and enforcing the structural integrity and long-term vitality of the GhostOS documentation system.

It defines both **tactical quality gates** and **strategic health metrics**—used by contributors, agents, and system operators alike.

---

## 📊 metrics.md

**Purpose:** Strategic health monitoring

- Defines KPIs for semantic coverage, adoption, and execution success
- Used by operators during planning rituals and system evaluations
- Tracks trends, usage rates, and structure adherence

---

## ✅ validation.md

**Purpose:** Quality assurance gate

- Defines pass/fail rules for PRDs, story blocks, and doc structure
- Used by contributors and bots to validate changes before commit
- Powers `ghost validate` and preflight logic in CI/CD

---

## Usage Examples

**For Contributors:**

```bash
ghost validate prd ghost/doc-ops/prd/build-doc-ops.md
```

**For System Operators:**

```bash
ghost metrics docops
ghost evaluate
```

**For CI Pipelines:**

- Use `validation.md` to enforce structural correctness
- Compare metrics targets for regression detection

---

## Integration Notes

- `metrics.md` powers reflective evaluation (`ghost evaluate`)
- `validation.md` powers active gating (`ghost validate`)
- Both support continuous improvement of ghost-native documentation workflows

---

Together, these files define the symbolic and operational contract of documentation health in GhostOS.
