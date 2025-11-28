# Test Plan

| Level | Scenario | Steps | Expected Result |
| --- | --- | --- | --- |
| Unit | Session duration never negative | Recompute `(EndDT-StartDT)` inside `app.enrich_sessions` | All durations ≥ 0 and match the CSV values |
| Unit | Tab switch bounds respected | Call `enrich_sessions` with fabricated 40-tab rows | Output clips values to ≤25 |
| Unit | DeepWork guardrails | Feed short/low sessions through `enrich_sessions` | `DeepWorkFlag` stays 0 unless duration ≥45 & tab ≤5 |
| Unit | App usage labeling | Validate `AppUsage.csv` rows -> Label (Productive vs Distracting) | Labels match category mapping |
| Integration | `.ics` busy windows align to sessions | Upload sample `.ics`, inspect timeline + focus window | Busy events display on correct day/hour and update recommendation |
| Integration | Pareto totals reconcile | Compare Pareto bar sum to interruption total metric | Totals match overall `DurationMin` |
| Integration | Wasted time KPI | Verify `Time Wasted` = social app minutes + interruption minutes | KPI equals underlying calculation |
| Functional | FR1–FR4 Streamlit tabs | Interact with Overview, Focus, Distraction, Calendar, and Goals tabs | KPIs, charts, and summaries render without errors |
| Functional | Goals & recommendations | Update goals/app files and reload | Goal progress/proposals refresh without errors |
| Functional | Acceptance criteria adherence | Validate against `docs/ACCEPTANCE_CRITERIA.md` inside Streamlit | All ACs satisfied using mock data |
| Regression | Data regeneration stability | Regenerate data then restart Streamlit | App reloads cleanly with new datasets |
