---
title: metrics
type: metric-schema
version: 1.3
status: evolving
updated: 2025-06-13
owner: ghost
audience: [strategist, operator, ghost]
invokes: ghost evaluate
---

---

# 📊 DocOps Metrics

Defines measurable indicators for evaluating adoption, coverage, and impact of the ghostOS semantic documentation system.

---

## ✅ Structural Coverage

Tracks presence of required files and formatting compliance.

| Metric                     | Target   | Notes                                         |
| -------------------------- | -------- | --------------------------------------------- |
| PRDs using semantic spec   | 100%     | All active epics must follow markdown spec    |
| Stories with YAML metadata | 100%     | Each story block must have ID, status, effort |
| Success criteria defined   | 100%     | Every story requires testable outcomes        |
| Persona rituals authored   | ≥5       | Coverage across planning, delivery, strategy  |
| DocOps changelog entries   | ≥1/month | Change traceability in /ghost/doc-ops/spec    |

---

## 🔄 Execution Feedback

Measures operational effectiveness of rituals + PRDs.

| Metric                               | Target          | Notes                                           |
| ------------------------------------ | --------------- | ----------------------------------------------- |
| ghost CLI PRD parse success          | 100%            | `ghost plan` and `ghost evaluate` must not fail |
| Validation failures caught pre-merge | ≥95%            | Ensures no broken PRDs enter main               |
| Simulation coverage                  | ≥3 personas/run | Each major epic should have at least 3 lenses   |
| Story execution traceability         | 100%            | Every commit linked to story ID or ghost log    |
| Unlinked tasks/stories               | 0               | No orphaned execution without PRD lineage       |

---

## 📈 Adoption Indicators

Early signs of healthy system usage.

| Metric                                   | Target       | Notes                                  |
| ---------------------------------------- | ------------ | -------------------------------------- |
| New PRDs authored using CLI template     | ≥1/week      | Measures contributor tool usage        |
| Docs linked in commit messages           | ≥50%         | Semantic doc awareness in dev flow     |
| External contributors using semantic PRD | ≥1           | First signal of open source legibility |
| Vault markdown usage (total files)       | +10% monthly | Measures organic doc expansion         |

---

## 🧠 Meta

These metrics should inform planning rituals and simulation output.  
They are not hard KPIs, but ambient indicators of systemic health and integrity.

### ✅ Success Criteria

- [ ] All tables validated against latest semantic-prd version
- [ ] Metrics integrated into ghost evaluation logic
- [ ] Metrics regularly reviewed during roadmap planning
- [ ] Contributor-facing usage guide exists
