from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st


DEFAULT_LOG_PATH = Path.home() / ".cursor" / "ai-tracking" / "skill-usage.jsonl"


def _parse_timestamp(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def load_events(path: Path) -> pd.DataFrame:
    rows: list[dict] = []
    if not path.exists():
        return pd.DataFrame(rows)

    for line in path.read_text(errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        rows.append(
            {
                "timestamp": _parse_timestamp(str(event.get("timestamp", ""))),
                "skill_name": str(event.get("skill_name", "unknown")),
                "session_id": str(event.get("session_id", "unknown")),
                "repo": str(event.get("repo", "unknown")),
                "model": str(event.get("model", "unknown")),
            }
        )

    df = pd.DataFrame(rows)
    if df.empty:
        return df
    return df.dropna(subset=["timestamp"]).sort_values("timestamp")


st.set_page_config(page_title="Panda Skills Analytics", layout="wide")
st.title("Panda Skills Analytics")
st.caption("Track skill invocation trends from a JSONL log.")

with st.sidebar:
    st.header("Data source")
    path_input = st.text_input("Log file path", str(DEFAULT_LOG_PATH))
    log_path = Path(path_input).expanduser()
    st.write(f"Exists: {'Yes' if log_path.exists() else 'No'}")

df = load_events(log_path)
if df.empty:
    st.warning(
        "No valid events found. Add JSONL records with keys like "
        "`timestamp`, `skill_name`, `session_id`, `repo`, and `model`."
    )
    st.stop()

min_ts = df["timestamp"].min().date()
max_ts = df["timestamp"].max().date()

with st.sidebar:
    st.header("Filters")
    date_range = st.date_input("Date range", (min_ts, max_ts))
    selected_repos = st.multiselect("Repo", sorted(df["repo"].unique()), default=sorted(df["repo"].unique()))
    selected_models = st.multiselect("Model", sorted(df["model"].unique()), default=sorted(df["model"].unique()))

filtered = df.copy()
if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = date_range
    filtered = filtered[
        (filtered["timestamp"].dt.date >= start)
        & (filtered["timestamp"].dt.date <= end)
    ]
if selected_repos:
    filtered = filtered[filtered["repo"].isin(selected_repos)]
if selected_models:
    filtered = filtered[filtered["model"].isin(selected_models)]

if filtered.empty:
    st.info("No events match current filters.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total invocations", f"{len(filtered):,}")
col2.metric("Unique skills", f"{filtered['skill_name'].nunique():,}")
col3.metric("Unique sessions", f"{filtered['session_id'].nunique():,}")
col4.metric("Unique repos", f"{filtered['repo'].nunique():,}")

st.subheader("Daily Invocations")
daily = (
    filtered.assign(day=filtered["timestamp"].dt.date)
    .groupby("day")
    .size()
    .reset_index(name="count")
)
st.line_chart(daily.set_index("day"))

st.subheader("Top Skills")
top_skills = (
    filtered.groupby("skill_name")
    .size()
    .reset_index(name="invocations")
    .sort_values("invocations", ascending=False)
)
st.bar_chart(top_skills.set_index("skill_name"))

st.subheader("Skill Usage Table")
st.dataframe(top_skills, use_container_width=True)

st.subheader("Recent Events")
st.dataframe(
    filtered.sort_values("timestamp", ascending=False).head(100),
    use_container_width=True,
)
