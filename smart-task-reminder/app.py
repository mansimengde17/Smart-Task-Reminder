"""Streamlit control room for the Smart Task Reminder experience."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA_DIR = Path(__file__).resolve().parent / "data"

st.set_page_config(
    page_title="Smart Task Reminder",
    page_icon="⏱️",
    layout="wide",
)

THEME = """
<style>
:root {
    --card-bg: rgba(17, 24, 39, 0.7);
    --accent: #7c4dff;
    --accent-soft: rgba(124, 77, 255, 0.12);
    --text-muted: #9ca3af;
}
body {
    background-color: #05080f;
    color: #f5f5f5;
}
section[data-testid="stSidebar"] {
    background-color: #0f1623;
}
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.metric-card {
    border-radius: 16px;
    padding: 1rem 1.2rem;
    background: var(--card-bg);
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 15px 35px rgba(0,0,0,0.35);
}
.metric-card__label {
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
}
.metric-card__value {
    font-size: 2rem;
    font-weight: 700;
    margin: 0.2rem 0;
}
.metric-card__sub {
    font-size: 0.9rem;
    color: var(--text-muted);
}
.metric-card__delta {
    font-size: 0.85rem;
    color: #34d399;
    margin-top: 0.3rem;
}
.recommendation-box {
    border-left: 4px solid var(--accent);
    padding: 0.8rem 1rem;
    background: var(--accent-soft);
    border-radius: 10px;
    margin-bottom: 0.6rem;
}
</style>
"""
st.markdown(THEME, unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def load_sessions() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "Sessions.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["StartDT"] = pd.to_datetime(df["Date"].dt.strftime("%Y-%m-%d") + " " + df["StartTime"])
    df["EndDT"] = pd.to_datetime(df["Date"].dt.strftime("%Y-%m-%d") + " " + df["EndTime"])
    df["DurationMin"] = df["DurationMin"].fillna((df["EndDT"] - df["StartDT"]).dt.total_seconds() / 60)
    df["DurationMin"] = df["DurationMin"].clip(lower=0)
    df["TabSwitchCount"] = df["TabSwitchCount"].clip(lower=0, upper=25)
    return df


@st.cache_data(show_spinner=False)
def load_interruptions() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "Interruptions.csv")
    df["StartDT"] = pd.to_datetime(df["StartDT"])
    return df


@st.cache_data(show_spinner=False)
def parse_calendar(text: str) -> pd.DataFrame:
    blocks = text.split("BEGIN:VEVENT")
    events = []
    for raw in blocks[1:]:
        section = raw.split("END:VEVENT", 1)[0]
        lines = [line.strip() for line in section.splitlines() if line.strip()]
        lookup = {line.split(":", 1)[0]: line.split(":", 1)[1] for line in lines if ":" in line}
        dt_start = lookup.get("DTSTART")
        dt_end = lookup.get("DTEND")
        if not dt_start or not dt_end:
            continue
        summary = lookup.get("SUMMARY", "Busy")
        description = lookup.get("DESCRIPTION", "")
        start = datetime.strptime(dt_start, "%Y%m%dT%H%M%SZ")
        end = datetime.strptime(dt_end, "%Y%m%dT%H%M%SZ")
        duration = max((end - start).total_seconds() / 60, 0)
        events.append(
            {
                "Summary": summary,
                "Description": description,
                "Start": start,
                "End": end,
                "DurationMin": duration,
                "Status": "Busy" if duration > 0 else "Free",
                "Day": start.strftime("%Y-%m-%d"),
            }
        )
    return pd.DataFrame(events)


@st.cache_data(show_spinner=False)
def load_app_usage() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "AppUsage.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["IsDistracting"] = df["Label"] == "Distracting"
    return df


@st.cache_data(show_spinner=False)
def load_goals() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "Goals.csv")
    df["DueDate"] = pd.to_datetime(df["DueDate"])
    df["ProgressPct"] = (df["ActualMinutes"] / df["TargetMinutes"]).clip(0, 1)
    return df


@dataclass
class FocusMetrics:
    focus_score: float
    deep_work_pct: float
    prod_loss_pct: float
    focus_delta: float


@dataclass
class SystemInsights:
    wasted_minutes: float
    social_minutes: float
    interruption_minutes: float
    goal_progress_pct: float


def enrich_sessions(df: pd.DataFrame) -> pd.DataFrame:
    counts = df["CompletedCount"] + df["AbandonedCount"]
    completion_rate = np.divide(
        df["CompletedCount"], counts, out=np.zeros_like(df["CompletedCount"], dtype=float), where=counts != 0
    )
    duration_factor = np.minimum(1.0, df["DurationMin"] / 60.0)
    tab_penalty = np.minimum(1.0, df["TabSwitchCount"] / 20.0)
    focus_score = 50 + 20 * completion_rate + 20 * duration_factor - 10 * tab_penalty
    df["FocusScore"] = focus_score.clip(0, 100)
    df["DeepWorkFlag"] = np.where((df["FocusScore"] >= 70) & (df["DurationMin"] >= 45) & (df["TabSwitchCount"] <= 5), 1, 0)
    df["HourOfDay"] = df["StartDT"].dt.hour
    df["Week"] = df["Date"].dt.isocalendar().week
    return df


def compute_metrics(sessions: pd.DataFrame, interruptions: pd.DataFrame) -> FocusMetrics:
    focus_score = sessions["FocusScore"].mean()
    deep_pct = sessions["DeepWorkFlag"].mean()
    work_minutes = sessions["DurationMin"].sum()
    loss_minutes = interruptions["DurationMin"].sum() if not interruptions.empty else 0
    prod_loss = loss_minutes / work_minutes if work_minutes else 0
    cutoff = sessions["Date"].max()
    this_week_mask = sessions["Date"].between(cutoff - timedelta(days=6), cutoff)
    prior_week_mask = sessions["Date"].between(cutoff - timedelta(days=13), cutoff - timedelta(days=7))
    this_week = sessions.loc[this_week_mask, "FocusScore"].mean()
    prior_week = sessions.loc[prior_week_mask, "FocusScore"].mean()
    delta = (this_week - prior_week) if not np.isnan(this_week) and not np.isnan(prior_week) else 0
    return FocusMetrics(focus_score, deep_pct, prod_loss, delta)


def compute_insights(
    interruptions: pd.DataFrame, app_usage: pd.DataFrame, goals: pd.DataFrame
) -> SystemInsights:
    social_minutes = app_usage.loc[app_usage["IsDistracting"], "Minutes"].sum()
    interruption_minutes = interruptions["DurationMin"].sum()
    wasted_minutes = social_minutes + interruption_minutes
    goal_progress = goals["ActualMinutes"].sum() / goals["TargetMinutes"].sum()
    return SystemInsights(
        wasted_minutes=wasted_minutes,
        social_minutes=social_minutes,
        interruption_minutes=interruption_minutes,
        goal_progress_pct=goal_progress,
    )


def render_metric_card(title: str, value: str, subtitle: str, delta: str | None = None) -> None:
    html = f"""
    <div class="metric-card">
        <div class="metric-card__label">{title}</div>
        <div class="metric-card__value">{value}</div>
        <div class="metric-card__sub">{subtitle}</div>
        {f'<div class="metric-card__delta">{delta}</div>' if delta else ''}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def plot_daily_focus(sessions: pd.DataFrame):
    daily = sessions.groupby("Date").agg({"FocusScore": "mean"}).reset_index()
    fig = px.line(daily, x="Date", y="FocusScore", title="Daily Focus Score", markers=True)
    fig.update_yaxes(range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)


def plot_tasktype_focus(sessions: pd.DataFrame):
    task = (
        sessions.groupby("TaskType").agg({"FocusScore": "mean"}).sort_values("FocusScore", ascending=False).reset_index()
    )
    fig = px.bar(task, x="TaskType", y="FocusScore", title="Focus by Task Type", text="FocusScore")
    fig.update_yaxes(range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)


def plot_pareto(interruptions: pd.DataFrame):
    if interruptions.empty:
        st.info("No interruptions captured for this period.")
        return
    agg = interruptions.groupby("Category").agg({"DurationMin": "sum"}).sort_values("DurationMin", ascending=False)
    agg["CumulativePct"] = agg["DurationMin"].cumsum() / agg["DurationMin"].sum()
    fig = go.Figure()
    fig.add_bar(x=agg.index, y=agg["DurationMin"], name="Loss minutes")
    fig.add_scatter(x=agg.index, y=agg["CumulativePct"] * 100, mode="lines+markers", name="Cumulative %", yaxis="y2")
    fig.update_layout(
        title="Interruption Pareto",
        yaxis=dict(title="Minutes"),
        yaxis2=dict(title="Cumulative %", overlaying="y", side="right", range=[0, 100]),
        shapes=[{"type": "line", "x0": -0.5, "x1": len(agg.index) - 0.5, "y0": 80, "y1": 80, "yref": "y2", "line": {"dash": "dash"}}],
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_interruption_heatmap(interruptions: pd.DataFrame):
    if interruptions.empty:
        return
    temp = interruptions.copy()
    temp["DayOfWeek"] = temp["StartDT"].dt.day_name()
    temp["Hour"] = temp["StartDT"].dt.hour
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    temp["DayOfWeek"] = pd.Categorical(temp["DayOfWeek"], categories=order, ordered=True)
    pivot = temp.pivot_table(index="DayOfWeek", columns="Hour", values="InterruptionID", aggfunc="count", fill_value=0)
    fig = px.imshow(pivot, aspect="auto", color_continuous_scale="Reds", title="Interruption Density (Day vs Hour)")
    st.plotly_chart(fig, use_container_width=True)


def plot_app_usage(app_usage: pd.DataFrame):
    summary = app_usage.groupby(["Date", "Label"])["Minutes"].sum().reset_index()
    fig = px.area(summary, x="Date", y="Minutes", color="Label", title="App Usage Trend", groupnorm="fraction")
    st.plotly_chart(fig, use_container_width=True)


def render_distraction_table(app_usage: pd.DataFrame):
    distractors = (
        app_usage[app_usage["IsDistracting"]]
        .groupby(["AppName", "Category"])
        ["Minutes"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    if distractors.empty:
        st.info("No distracting app minutes recorded.")
        return
    st.dataframe(distractors.head(10).rename(columns={"Minutes": "Minutes/Week"}), use_container_width=True)


def plot_calendar_timeline(calendar_df: pd.DataFrame):
    if calendar_df.empty:
        st.warning("Calendar file has no events.")
        return
    fig = px.timeline(calendar_df, x_start="Start", x_end="End", y="Summary", color="DurationMin", title="Calendar Busy Windows")
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)


def focus_energy_curve(sessions: pd.DataFrame) -> pd.Series:
    curve = sessions.groupby("HourOfDay")["FocusScore"].mean().reindex(range(24))
    return curve


def render_focus_curve(curve: pd.Series):
    curve_df = curve.reset_index().rename(columns={"index": "HourOfDay"})
    fig = px.line(curve_df, x="HourOfDay", y="FocusScore", title="Focus Energy Curve", markers=True)
    fig.update_xaxes(title="Hour of Day")
    fig.update_yaxes(title="Focus Score", range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)


def render_goals(goals: pd.DataFrame):
    for _, row in goals.iterrows():
        st.markdown(f"**{row['GoalName']}** · due {row['DueDate'].date():%b %d} · {row['Status']}")
        st.progress(row["ProgressPct"])
        st.caption(f"{row['ActualMinutes']} / {row['TargetMinutes']} minutes")


def generate_recommendations(
    insights: SystemInsights, app_usage: pd.DataFrame, curve: pd.Series, goals: pd.DataFrame
) -> List[str]:
    recs: List[str] = []
    top_social = (
        app_usage[app_usage["IsDistracting"]]
        .groupby("AppName")["Minutes"]
        .sum()
        .sort_values(ascending=False)
    )
    if not top_social.empty:
        recs.append(f"Silence {top_social.index[0]} notifications to reclaim {int(top_social.iloc[0])} minutes per week.")
    if insights.interruption_minutes > 0:
        recs.append(
            f"Batch communication apps to cut {int(insights.interruption_minutes)} minutes of interruption loss each week."
        )
    best_hour = curve.idxmax() if not curve.dropna().empty else None
    if best_hour is not None:
        recs.append(f"Protect {int(best_hour):02d}:00-{int(best_hour)+1:02d}:00 as a Deep Work block based on energy curve.")
    if insights.goal_progress_pct < 0.75:
        recs.append("Add an extra focus block for at-risk goals until progress exceeds 75%.")
    if len(recs) < 4:
        recs.append("Review Friday afternoon calendar clutter and mark low-value meetings as optional.")
    return recs[:4]


sessions_df = enrich_sessions(load_sessions())
interruptions_df = load_interruptions()
app_usage_df = load_app_usage()
goals_df = load_goals()
default_calendar = parse_calendar((DATA_DIR / "Calendar.ics").read_text(encoding="utf-8"))

metrics = compute_metrics(sessions_df, interruptions_df)
insights = compute_insights(interruptions_df, app_usage_df, goals_df)
curve = focus_energy_curve(sessions_df)
best_hour = int(curve.idxmax()) if not curve.dropna().empty else None

st.title("SMART TASK REMINDER")
min_date = sessions_df["Date"].min()
max_date = sessions_df["Date"].max()
range_text = f"Monitoring window: {min_date:%b %d} - {max_date.strftime('%b %d, %Y')}"
st.caption(range_text)

metric_cols = st.columns(5)
with metric_cols[0]:
    render_metric_card("Focus Score", f"{metrics.focus_score:.1f}", "Avg last 28 days")
with metric_cols[1]:
    render_metric_card("Deep Work %", f"{metrics.deep_work_pct * 100:.1f}%", "Share of sessions")
with metric_cols[2]:
    render_metric_card("Time Wasted", f"{insights.wasted_minutes:.0f} min", "Social + interruptions")
with metric_cols[3]:
    render_metric_card("Goal Progress", f"{insights.goal_progress_pct * 100:.1f}%", "Weighted across goals")
with metric_cols[4]:
    render_metric_card("Focus Delta", f"{metrics.focus_delta:+.1f}", "vs prior week")

if best_hour is not None:
    st.success(f"Suggested Focus Window: Hour {best_hour}:00 based on Focus Energy Curve")

overview_tab, focus_tab, distraction_tab, calendar_tab, goals_tab = st.tabs(
    ["Overview", "Focus Engine", "Distraction Radar", "Calendar Map", "Goals & Actions"]
)

with overview_tab:
    st.subheader("Where the minutes go")
    waste_df = pd.DataFrame(
        [
            {"Source": "Social Apps", "Minutes": insights.social_minutes},
            {"Source": "Interruptions", "Minutes": insights.interruption_minutes},
            {"Source": "Deep Work", "Minutes": sessions_df[sessions_df["DeepWorkFlag"] == 1]["DurationMin"].sum()},
        ]
    )
    fig = px.pie(waste_df, names="Source", values="Minutes", hole=0.5, color_discrete_sequence=px.colors.sequential.Aggrnyl)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top takeaways")
    takeaways = [
        f"Social apps consumed {insights.social_minutes:.0f} minutes; combine mute + scheduled checks.",
        f"Interruptions removed {insights.interruption_minutes:.0f} minutes of focus time.",
        "Deep Work coverage is {0:.1f}%".format(metrics.deep_work_pct * 100),
    ]
    for note in takeaways:
        st.markdown(f"- {note}")

with focus_tab:
    st.subheader("Focus Score Diagnostics")
    plot_daily_focus(sessions_df)
    plot_tasktype_focus(sessions_df)
    st.subheader("Focus Energy Curve")
    render_focus_curve(curve)

with distraction_tab:
    st.subheader("Interruption Drivers")
    plot_pareto(interruptions_df)
    plot_interruption_heatmap(interruptions_df)
    st.subheader("App Usage & Social Drag")
    plot_app_usage(app_usage_df)
    st.subheader("Top Distraction Apps")
    render_distraction_table(app_usage_df)

with calendar_tab:
    st.subheader("Calendar Load & Upload")
    uploaded_calendar = st.file_uploader("Upload optional .ics to overlay", type=["ics"], key="calendar_upload")
    calendar_df = default_calendar
    if uploaded_calendar is not None:
        uploaded_text = uploaded_calendar.read().decode("utf-8")
        parsed = parse_calendar(uploaded_text)
        if parsed.empty:
            st.warning("Uploaded file has no VEVENT entries; showing default calendar instead.")
        else:
            calendar_df = parsed
    plot_calendar_timeline(calendar_df)
    if best_hour is not None:
        st.info(f"Protect the hour starting at {best_hour}:00 on days with fewer Busy blocks.")

with goals_tab:
    left, right = st.columns([1, 1])
    with left:
        st.subheader("Goal Progress")
        render_goals(goals_df)
    with right:
        st.subheader("Focus Recovery Playbook")
        for rec in generate_recommendations(insights, app_usage_df, curve, goals_df):
            st.markdown(f"<div class='recommendation-box'>{rec}</div>", unsafe_allow_html=True)

st.divider()
st.caption(
    "Smart Task Reminder surfaces focus signals, distraction risks, calendar conflicts, and goal readiness in one place."
)
