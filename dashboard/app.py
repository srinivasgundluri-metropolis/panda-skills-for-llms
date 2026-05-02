from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st


DEFAULT_LOG_PATH = Path.home() / ".cursor" / "ai-tracking" / "skill-usage.jsonl"


def default_claude_skill_usage_log_path() -> Path:
    """Matches auto_track_skill_usage.py defaults for layout=claude-code."""
    override = os.environ.get("CLAUDE_CONFIG_DIR", "").strip()
    root = Path(override).expanduser() if override else Path.home() / ".claude"
    return root / "ai-tracking" / "skill-usage.jsonl"


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


def load_events_from_paths(paths: list[Path]) -> pd.DataFrame:
    frames = [load_events(p) for p in paths if p]
    frames = [f for f in frames if not f.empty]
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True).sort_values("timestamp")


def _parse_extra_log_paths(raw: str) -> list[Path]:
    out: list[Path] = []
    for line in (raw or "").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        out.append(Path(s).expanduser())
    return out


st.set_page_config(page_title="Panda Skills Analytics", layout="wide")
st.title("Panda Skills Analytics")
st.caption(
    "Track skill invocation trends from JSONL logs (Cursor: ~/.cursor/ai-tracking/; "
    "Claude Code: ~/.claude/ai-tracking/)."
)

with st.sidebar:
    st.header("Data source")
    path_input = st.text_input("Primary log file path", str(DEFAULT_LOG_PATH))
    log_path = Path(path_input).expanduser()
    claude_default_log = default_claude_skill_usage_log_path()
    merge_help = (
        "Optional. Merge Claude Code (or other) JSONL with the primary log. "
        f"Default Claude watcher output: `{claude_default_log}`."
    )
    extra_raw = st.text_area(
        "Additional log paths (one per line)",
        value=str(claude_default_log) if claude_default_log.exists() else "",
        height=100,
        help=merge_help,
    )
    extra_paths = _parse_extra_log_paths(extra_raw)
    all_paths = [log_path, *[p for p in extra_paths if p != log_path]]
    st.write(
        "Paths loaded: "
        + ", ".join(f"{'✓' if p.exists() else '✗'} `{p.name}`" for p in all_paths)
    )

df = load_events_from_paths(all_paths)
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

st.subheader("Today")
today = filtered["timestamp"].max().date()
daily_total = int((filtered["timestamp"].dt.date == today).sum())
st.metric("Invocations today", f"{daily_total:,}")
st.caption(f"Top skills for {today}")
today_df = filtered[filtered["timestamp"].dt.date == today]
today_counts = (
    today_df.groupby("skill_name")
    .size()
    .reset_index(name="invocations")
    .sort_values("invocations", ascending=False)
)

if not today_counts.empty:
    top4 = today_counts.head(4).copy()
    other_count = int(today_counts["invocations"].iloc[4:].sum())
    if other_count > 0:
        top4 = pd.concat(
            [
                top4,
                pd.DataFrame([{"skill_name": "Other", "invocations": other_count}]),
            ],
            ignore_index=True,
        )
    st.plotly_chart(
        {
            "data": [
                {
                    "labels": top4["skill_name"],
                    "values": top4["invocations"],
                    "type": "pie",
                    "hole": 0.25,
                    "textinfo": "label+percent",
                }
            ],
            "layout": {"margin": {"l": 0, "r": 0, "t": 0, "b": 0}},
        },
        use_container_width=True,
    )
else:
    st.info("No events available for the selected day.")

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
