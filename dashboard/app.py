from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


def default_claude_skill_usage_log_path() -> Path:
    """Matches auto_track_skill_usage.py defaults for layout=claude-code."""
    override = os.environ.get("CLAUDE_CONFIG_DIR", "").strip()
    root = Path(override).expanduser() if override else Path.home() / ".claude"
    return root / "ai-tracking" / "skill-usage.jsonl"


DEFAULT_LOG_PATH = default_claude_skill_usage_log_path()


def _parse_timestamp(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def _event_agent(event: dict) -> str:
    """Prefer `agent`; fall back to legacy `model` field."""
    v = event.get("agent", event.get("model"))
    return str(v) if v is not None and str(v) != "" else "unknown"


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
                "agent": _event_agent(event),
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
    "Claude Code skill usage from JSONL (default: ~/.claude/ai-tracking/skill-usage.jsonl). "
    "Optionally merge more logs below."
)

with st.sidebar:
    st.header("Data source")
    path_input = st.text_input("Primary log file path", str(DEFAULT_LOG_PATH))
    log_path = Path(path_input).expanduser()
    merge_help = (
        "Optional. One path per line to merge into the same charts (e.g. a second machine’s export)."
    )
    extra_raw = st.text_area(
        "Additional log paths (one per line)",
        value="",
        height=100,
        placeholder="# ~/.claude/ai-tracking/skill-usage-other.jsonl",
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
        "No valid events found. Add JSONL lines with at least "
        "`timestamp`, `skill_name`, `session_id`, and `agent` (legacy logs may use `model` instead of `agent`)."
    )
    st.stop()

min_ts = df["timestamp"].min().date()
max_ts = df["timestamp"].max().date()

with st.sidebar:
    st.header("Filters")
    date_range = st.date_input("Date range", (min_ts, max_ts))
    selected_agents = st.multiselect(
        "Agent", sorted(df["agent"].unique()), default=sorted(df["agent"].unique())
    )

filtered = df.copy()
if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = date_range
    filtered = filtered[
        (filtered["timestamp"].dt.date >= start)
        & (filtered["timestamp"].dt.date <= end)
    ]
if selected_agents:
    filtered = filtered[filtered["agent"].isin(selected_agents)]

if filtered.empty:
    st.info("No events match current filters.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total invocations", f"{len(filtered):,}")
col2.metric("Unique skills", f"{filtered['skill_name'].nunique():,}")
col3.metric("Unique sessions", f"{filtered['session_id'].nunique():,}")
col4.metric("Unique agents", f"{filtered['agent'].nunique():,}")

st.subheader("Compare agents")
st.caption(
    "Each **agent** value comes from the watcher’s `--agent` label (or defaults like `claude-code`). "
    "Run separate watchers or merge logs to compare streams—for example `claude-code` vs `cursor`, "
    "or two machines exporting JSONL into **Additional log paths**."
)
_agent_summary = (
    filtered.groupby("agent", as_index=False)
    .agg(
        invocations=("skill_name", "size"),
        unique_skills=("skill_name", "nunique"),
        unique_sessions=("session_id", "nunique"),
    )
    .sort_values("invocations", ascending=False)
)
_agent_summary = _agent_summary.assign(
    invocations_per_session=_agent_summary["invocations"]
    / _agent_summary["unique_sessions"].replace(0, pd.NA),
    skills_per_session=_agent_summary["unique_skills"]
    / _agent_summary["unique_sessions"].replace(0, pd.NA),
)
_display = _agent_summary.copy()
for c in ("invocations_per_session", "skills_per_session"):
    _display[c] = _display[c].round(2)
st.dataframe(
    _display.rename(
        columns={
            "invocations": "Invocations",
            "unique_skills": "Distinct skills",
            "unique_sessions": "Sessions",
            "invocations_per_session": "Invocations / session",
            "skills_per_session": "Distinct skills / session",
        }
    ),
    use_container_width=True,
    hide_index=True,
)

if filtered["agent"].nunique() >= 2:
    top_n_skills = 12
    top_skill_names = (
        filtered.groupby("skill_name")
        .size()
        .nlargest(top_n_skills)
        .index.tolist()
    )
    _counts = (
        filtered[filtered["skill_name"].isin(top_skill_names)]
        .groupby(["skill_name", "agent"], as_index=False)
        .size()
        .rename(columns={"size": "invocations"})
    )
    fig = px.bar(
        _counts,
        y="skill_name",
        x="invocations",
        color="agent",
        barmode="group",
        orientation="h",
        labels={
            "skill_name": "Skill",
            "invocations": "Invocations",
            "agent": "Agent",
        },
        title=f"Top {top_n_skills} skills — invocations by agent (current filters)",
    )
    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        legend_title_text="Agent",
        margin={"l": 8, "r": 8, "t": 40, "b": 8},
        height=420,
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info(
        "Add a second **agent** label in your data to see grouped bars here—for example run another "
        "watcher with `--agent plan` or merge a second JSONL that used a different `--agent`."
    )

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
