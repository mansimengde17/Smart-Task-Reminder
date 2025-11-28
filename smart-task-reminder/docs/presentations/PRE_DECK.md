# Pre-Presentation Deck (20 Slides)

Each slide below lists 5 detailed bullet prompts (or 4 + visual guidance) to help you craft a thorough PPT.

1. **Title – SMART TASK REMINDER Sprint Brief**
   - Project name, sprint number/date, presenter(s).
   - Tagline: "Focus, Distraction, Calendar, Goals – unified dashboard".
   - Include course/instructor info.
   - Visual: hero screenshot of Streamlit app.
   - Footer: repo link + contact.

2. **Mission Statement**
   - One-sentence mission.
   - Why context switching hurts a single learner.
   - How the control room centralizes signals.
   - Desired transformation (reactive → proactive).
   - Icons representing focus, apps, calendar, goals.

3. **Problem Landscape**
   - Daily disruptions (Slack, social apps, meetings).
   - Data point: 5+ tab switches reduce deep work success.
   - Calendar overload + no unified telemetry.
   - Pain point: manual reporting, inconsistent reminders.
   - Quote/stat from productivity research.

4. **Vision (Unlimited Resources)**
   - Real-time ingestion (Google/Outlook calendars, Slack, device usage).
   - AI-driven nudges + auto-scheduling.
   - Cross-platform agents (desktop, mobile, wearables).
   - Personalized focus prescriptions by persona.
   - Diagram showing multiple data streams feeding an AI copilot.

5. **Current Semester Commitment**
   - Deterministic mock data pipeline.
   - Streamlit control room with FR1–FR4, UC3.1.
   - Goals + recommendation engine.
   - Documentation + sprint readiness assets.
   - Checklist visual highlighting completed scope.

6. **Architecture Snapshot**
   - Diagram: generators → Streamlit → users.
   - Mention caching layer, computation layer, UI layer.
   - Call out ICS uploader feedback loop.
   - Highlight reproducibility (fixed seeds).
   - Emphasize tab-based UX mapping to FRs.

7. **Data Generation Pipeline**
   - Sessions: 4-week coverage, 1–4/day.
   - Interruptions: 0–3 per session, referenced IDs.
   - Calendar: UTC VEVENTS, 0–3 meetings/weekday.
   - App usage: productive vs distracting minutes.
   - Goals: target vs actual with On Track/At Risk status.

8. **Focus Scoring Engine (FR1)**
   - Formula factors (duration, completion, tab penalty).
   - KPI cards shown (FocusScore, DeepWork%, Delta).
   - Daily trend line for FocusScore.
   - TaskType bar chart insights.
   - Focus Energy curve recommending best hour.

9. **Distraction Analytics (FR2)**
   - Pareto chart (CategoryLoss + cumulative line).
   - Heatmap (day vs hour disruptions).
   - App usage area chart (productive vs distracting time).
   - Top 10 distraction table.
   - Time wasted KPI (social + interruptions).

10. **Calendar Mapping (FR3)**
    - ICS upload instructions + fallback messaging.
    - Timeline of busy windows (Plotly timeline screenshot).
    - Suggested focus window banner.
    - Link between calendar events and energy curve.
    - Use case: identify low-conflict hours.

11. **Weekly Insight Story (FR4)**
    - Overview donut (social vs interruptions vs deep work).
    - Takeaways bullets auto-generated.
    - Goals tab progress bars.
    - Focus Recovery Playbook recommendations.
    - Narrative flow (Overview → Focus → Distraction → Calendar → Goals).

12. **Goals & Recommendations**
    - Goals.csv fields (GoalID, Target, Actual, DueDate, Status).
    - Visualization: progress bars with percent labels.
    - Recommendation rules (top social app, interruption minutes, energy curve, goal progress).
    - Example recommendations displayed.
    - Impact: actionable steps at the end of each sprint.

13. **UC3.1 Demonstration**
    - Step-by-step: upload ICS → parse → timeline update.
    - Handling empty/invalid files.
    - UTC conversion to local baseline.
    - Where suggestions reference calendar load.
    - Future plan: connect to live API.

14. **Azure DevOps Snapshot**
    - Board columns (Backlog, Active, Done).
    - Completed items (#101–#104, #105, bug fixes).
    - Active items (#201 Persona, #202 Export).
    - Screenshot placeholder or bullet summary.
    - Mention burndown/velocity if available.

15. **Sprint Progress Since Last Class**
    - UI overhaul (dark theme, metric cards, tabs).
    - Added recommendation engine.
    - Added app usage + goals datasets.
    - Fixed PDF encoding and Plotly hour bug.
    - Updated documentation (README, report, guide).

16. **Next-Class Objectives**
    - Persona toggles (Student/Engineer) – customize recommendations.
    - Export helper (PNG/Markdown summary).
    - Timezone regression testing for ICS variance.
    - Decide on final presentation flow.
    - Gather feedback from classmates on dashboard UX.

17. **Risks & Mitigations**
    - Unicode exports → adopt custom font package.
    - Real data availability → mock now, add connectors later.
    - Personalization complexity → incremental toggles.
    - Calendar format variability → add validation & logging.
    - Adoption → highlight quick wins + share link early.

18. **Research Inputs**
    - Deep work thresholds (Cal Newport/Pomodoro studies).
    - Productivity loss stats from Slack/email context switching.
    - Pareto principle reference for FR2.
    - Calendar fatigue research (time-of-day energy curves).
    - Cite sources or URLs (footnote style).

19. **Schedule & Milestones**
    - Week 4: Data pipeline complete.
    - Week 6: FR1–FR3 implemented.
    - Week 8: FR4 + docs + recommendations.
    - Week 11: Persona/export features.
    - Week 12: Final rehearsal & submission.

20. **Q&A / Call to Action**
    - Invite classmates to upload their ICS files live.
    - Share repo path and Streamlit run command.
    - Encourage feedback on recommendations.
    - Mention next sprint stand-up time.
    - Thank audience / contact info.
