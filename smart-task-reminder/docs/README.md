# Smart Task Reminder Dashboard

## Overview
This repository ships a production-ready Streamlit experience (no Power BI required) that showcases the four functional requirements plus extended telemetry:
- **FR1 – Intelligent Focus Scoring Engine:** Calculates FocusScore, DeepWork, and productivity KPIs directly in-app.
- **FR2 – Cognitive Distraction Analytics:** Provides Pareto loss analysis, day/hour heatmaps, and new App Usage telemetry to highlight wasted minutes by app/category.
- **FR3 – Calendar-Aware Workload Mapping:** Parses `.ics` Busy intervals, overlays a timeline, and renders a Focus Energy Curve.
- **FR4 – Automated Weekly Insight Story:** Presents a dynamic Weekly Review view with KPIs, wasted-time breakdowns, calendar callouts, and goal-based recommendations.
- **Goals & Recommendations:** Goals.csv + real-time heuristics translate the data into progress bars and concrete next steps.

UC3.1 (Upload & Parse Calendar) is implemented via the Streamlit file uploader that re-processes VEVENT blocks in real time.

## Data Generation
1. Ensure Python 3.11+ is available.
2. From the repo root run:
   ```bash
   python3 scripts/generate_sessions.py
   python3 scripts/generate_interruptions.py
   python3 scripts/generate_calendar_ics.py
   python3 scripts/generate_app_usage.py
   python3 scripts/generate_goals.py
   ```
3. Outputs land in `data/` and stay referentially consistent thanks to fixed seeds.

## Streamlit App
1. Install dependencies (ideally in a virtual environment):
   ```bash
   pip install -r requirements.txt
   ```
2. Launch the dashboard:
   ```bash
   streamlit run app.py
   ```
3. The landing page exposes tabbed sections (Overview, Focus Engine, Distraction Radar, Calendar Map, Goals & Actions). Upload an alternate `.ics` file inside the Calendar tab to validate UC3.1, then use the Goals & Actions tab to capture weekly insights (FR4).

## Feature Mapping
- **FR1:** KPI row + daily trend + TaskType bar chart use the same FocusScore math as the DAX spec.
- **FR2:** Pareto chart, heatmap, and the new App Usage trend/table expose where time is wasted (interruptions + distracting apps).
- **FR3:** VEVENT timeline plus Focus Energy Curve recommend the best Focus Window, merging calendar context with observed performance.
- **FR4:** Weekly summary copy across the Overview + Goals & Actions tabs captures KPIs, wasted time, and recommendations ready to share.

## UC3.1 Notes
- `data/Calendar.ics` and any uploaded `.ics` files are parsed into Busy rows with Start/End/Duration metadata.
- The Streamlit page shows these intervals on a Plotly timeline and feeds the focus energy recommendation.
- Inline annotations remind analysts how to join Busy windows with sessions for conflict detection.

## Known Gotchas
- **Timezone normalization:** ICS timestamps are UTC (`Z`); the app removes zones and assumes UTC for aggregation.
- **Refresh order:** Re-run the session generator before interruptions whenever regenerating data.
- **Pareto cumulative line:** Category filters still show an 80% guideline; ensure at least one category remains selected.
