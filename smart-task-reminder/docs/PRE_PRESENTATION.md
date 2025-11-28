# Smart Task Reminder – Pre-Presentation Brief

## 1. Team Check-In
- **Accomplished since last session**
  - Delivered the dark-mode Streamlit control room with tabbed navigation.
  - Added deterministic generators for sessions, interruptions, calendar, app usage, and goals.
  - Implemented recommendation engine and custom CSS metric cards.
  - Closed defects: PDF encoding, Plotly Hour column mismatch.
- **Planned before next session**
  - Extend recommendations with persona knobs (e.g., "Student" vs "Engineer").
  - Add quick-win exporter (PNG snapshot or markdown summary) for stakeholders.
  - Validate ICS upload with multiple timezone variants and integrate into automated tests.
- **Obstacles**
  - Unicode-safe PDF export still pending fonts packaging.
  - Need product guidance on real calendar/app APIs for post-MVP roadmap.

## 2. Deliverable Vision
- **Goal (unlimited resources):** Always-on focus copilot that ingests real calendars, communication logs, and device usage to autoplan deep-work blocks and nudge the learner in real time.
- **In-semester commitment:** Ship the Streamlit control room with mock telemetry, UC3.1 upload, goals, recommendations, and documentation ready for handoff or future automation.

## 3. Schedule Snapshot
| Milestone | Date | Status |
| --- | --- | --- |
| Data generation toolchain | Week 4 | Complete |
| Streamlit FR1–FR3 core | Week 6 | Complete |
| FR4 narrative + recommendations | Week 8 | Complete |
| Persona knobs + exporter | Week 11 | Planned |
| Final polishing & rehearsal | Week 12 | Upcoming |

## 4. Azure DevOps Update
| Work Item | Column | Owner | Notes |
| --- | --- | --- | --- |
| #101 Focus Scoring Engine | Done | Mansi | Metrics + KPIs merged |
| #102 Distraction Radar | Done | Mansi | Pareto + heatmap + app usage |
| #103 Calendar Awareness | Done | Mansi | ICS parsing & timeline |
| #104 Weekly Story | Done | Mansi | Overview + Goals tabs |
| #201 Persona Personalization | Active | Team | Next sprint |
| #202 Export Helpers | Active | Team | Next sprint |
| Bug #33 PDF Unicode | Resolved | Team | Removed dependency |

## 5. Sprint Discussion Prompts
- **Since previous session:** Completed all FR1–FR4 functionality, refined UI, added recommendations.
- **Next session target:** Persona enhancements, exporter experiments, timezone regression tests.
- **Risks/needs:** Need approval for long-term API integration scope; confirm acceptance of Streamlit UI for final deliverable.

## 6. Supporting Links
- Repo root: `smart-task-reminder/`
- App entrypoint: `app.py`
- Docs: `docs/PROJECT_REPORT.md`, `docs/README.md`
