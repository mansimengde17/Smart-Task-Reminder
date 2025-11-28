# Weekly Report Guide

## Required Weekly Story Elements
- KPI row: FocusScore, DeepWorkPct, ProdLossPct, FocusScore_Delta, Time Wasted, Goal Progress.
- Top 3 interruption categories plus the leading distracting app.
- Focus Energy highlights listing the highest scoring hours + suggested focus window.
- Calendar insight: busiest day or conflict callout derived from parsed `.ics`.
- Goal progress summary (On Track vs At Risk) and recommended next steps.

## Visual Origins
- KPIs originate from `enrich_sessions` metrics used in the FR1 section plus insights from app usage.
- Pareto data comes from the FR2 bar/line chart leveraging the Interruptions table and AppUsage dataset.
- Focus Energy Curve reuses the FR3 line chart (hour vs FocusScore).
- Calendar conflicts rely on the FR3 timeline built from the parsed `.ics` file (UC3.1).
- Goal progress bars reuse the Goals dataset rendered near the recommendations section.

## Insights Template
Reuse/adapt these bullets inside the Streamlit copy or exported notes:
1. **Focus Momentum:** e.g., "FocusScore rose +4.2 pts vs prior week driven by higher completion rate."
2. **Top Distractions:** e.g., "Slack interruptions consumed 38% of loss minutes—mute channels during Deep Work blocks."
3. **Energy Curve:** e.g., "Peak focus remains 10–12 UTC; schedule Study/Coding during this window."
4. **Calendar Actions:** e.g., "Decline overlapping standups on Wednesday to recover 60 mins of Focus Energy."
