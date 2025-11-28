# Final Presentation Deck (20 Slides)

Each slide includes five detailed bullet prompts to aid PPT creation.

1. **Title – SMART TASK REMINDER Final Demo**
   - Project name, presenters, course details.
   - Tagline highlighting FR1–FR4 + UC3.1.
   - Date and sprint iteration.
   - Visual: hero shot of control room.
   - Contact info / repo URL footer.

2. **Executive Overview**
   - Summary of what the platform delivers.
   - Metrics: # datasets, # tabs, functionality highlights.
   - Map FR1–FR4 to UI tabs.
   - Mention UC3.1 support.
   - Outline structure of rest of deck.

3. **User Persona & Pain Points**
   - Persona details (name, role, schedule).
   - Key obstacles (distractions, lack of calendar insight, missed goals).
   - Example scenarios (exam week vs project week).
   - Quote or stat representing frustration.
   - Visual of persona journey.

4. **Goals & Success Metrics**
   - FocusScore target range.
   - Desired DeepWork% baseline.
   - Time wasted reduction goal.
   - Goal completion definition (≥75%).
   - Color-coded metric table.

5. **System Architecture**
   - Diagram showing generators feeding Streamlit.
   - Highlight caching, computation, UI layers.
   - Indicate ICS upload loop.
   - Mention deterministic seeds.
   - Note technologies (Python, Streamlit, Plotly).

6. **Data Generation Recap**
   - Sessions: counts, durations.
   - Interruptions: reference integrity, categories.
   - Calendar: number of VEVENTS, UTC handling.
   - App usage: productive vs distracting labels.
   - Goals: target vs actual minutes.

7. **Focus Engine Deep Dive (FR1)**
   - Formula breakdown (completion, duration, tab penalty).
   - KPI cards (FocusScore, DeepWork%, Delta).
   - Daily trend screenshot.
   - TaskType insights.
   - Focus Energy curve explanation.

8. **Distraction Radar Deep Dive (FR2)**
   - Pareto chart interpretation (top 3 categories).
   - Heatmap: busy days/hours.
   - App usage area chart.
   - Top distraction table.
   - Time wasted KPI impact.

9. **Calendar Intelligence (FR3)**
   - ICS upload steps.
   - Busy timeline visuals.
   - Suggested focus window logic.
   - Integration with Focus Energy curve.
   - Handling invalid uploads.

10. **Weekly Insight Narrative (FR4)**
     - Overview donut + takeaways.
     - Goals tab progress bars.
     - Recommendation list sample.
     - Flow across tabs (Overview→Goals).
     - How storytelling replaces PDF export.

11. **Goals & Accountability**
     - Goal dataset fields.
     - Progress thresholds (On Track vs At Risk).
     - Visual of progress bars.
     - Link to recommendations.
     - Next steps for Goal #G001–G003.

12. **Recommendations Engine**
     - Inputs: social minutes, interruption minutes, energy curve, goal progress.
     - Logic tree or pseudo-code snippet.
     - Example outputs ("Silence YouTube", "Batch Slack").
     - Future personalization toggles.
     - Impact metric (minutes recovered).

13. **UC3.1 Live Flow**
     - Step 1: Upload ICS.
     - Step 2: Parser extracts fields.
     - Step 3: Timeline updates.
     - Step 4: Suggested focus window recalculates.
     - Step 5: Recommendations mention calendar conflicts.

14. **Testing & QA**
     - Unit tests (duration, tab caps, DeepWork guards, labeling).
     - Integration tests (ICS alignment, Pareto totals, wasted-time KPI).
     - Functional tests (tab navigation, goals refresh).
     - Regression plan (re-run generators + reload app).
     - Tooling or manual checklist references.

15. **Azure DevOps & Sprint Summary**
     - List completed stories (#101–#105, bug fixes).
     - Active stories (#201 Persona, #202 Export).
     - Velocity/burndown mention.
     - Screenshot placeholder.
     - Takeaway: on-track for finals.

16. **Demo Walkthrough Plan**
     - Step 1: Overview tab (donut + takeaways).
     - Step 2: Focus tab (metrics + energy curve).
     - Step 3: Distraction tab (Pareto + apps).
     - Step 4: Calendar tab (ICS upload).
     - Step 5: Goals tab (progress + recs).

17. **Impact & Insights**
     - Example findings (Slack biggest distraction, best hour at 14:00).
     - Time wasted figure vs deep work minutes.
     - How recommendations shift behavior.
     - Takeaways per persona.
     - Metrics tracked for next iteration.

18. **Future Roadmap**
     - API integrations (Google Calendar, Slack, Screen Time).
     - Persona switches and ML anomaly detection.
     - Notification system / mobile companion.
     - Export services (PDF/email) with Unicode fonts.
     - Data privacy & security considerations.

19. **Risks & Mitigation Strategy**
     - Unicode export – adopt custom fonts.
     - Real data ingestion – staged connectors.
     - Adoption – UX feedback loop, quick wins.
     - Complexity – modular architecture to swap data sources.
     - Time constraints – prioritized backlog.

20. **Closing & Q&A**
     - Recap achievements.
     - Share next sprint goals or final submission date.
     - Provide repo link & Streamlit command.
     - Invite classmates to test ICS upload.
     - Thank you + contact info.
