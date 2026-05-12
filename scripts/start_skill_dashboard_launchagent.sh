#!/usr/bin/env bash
# macOS LaunchAgent entry: start Streamlit skill dashboard (or attach if port in use), open browser.
set -euo pipefail

REPO_ROOT="${PANDA_SKILLS_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
PYTHON="${SKILL_DASHBOARD_PYTHON:-/opt/anaconda3/bin/python3}"
PORT="${SKILL_DASHBOARD_PORT:-8501}"
HOST="127.0.0.1"
URL="http://${HOST}:${PORT}"

LOG_DIR="${HOME}/.cursor/ai-tracking"
mkdir -p "$LOG_DIR"
STLOG="${LOG_DIR}/streamlit-dashboard-launchd.log"

port_listening() {
  /usr/sbin/lsof -nP -iTCP:"${PORT}" -sTCP:LISTEN >/dev/null 2>&1
}

wait_for_http() {
  local i
  for i in $(seq 1 90); do
    if /usr/bin/curl -sf "${URL}/_stcore/health" >/dev/null 2>&1; then
      return 0
    fi
    sleep 1
  done
  return 1
}

if port_listening; then
  /usr/bin/open "${URL}" || true
  exec /usr/bin/tail -f /dev/null
fi

cd "${REPO_ROOT}"
"${PYTHON}" -m pip install -q -r dashboard/requirements.txt >>"${STLOG}" 2>&1 || true

"${PYTHON}" -m streamlit run dashboard/app.py \
  --server.headless true \
  --server.port "${PORT}" \
  --browser.gatherUsageStats false \
  >>"${STLOG}" 2>&1 &
STPID=$!

if wait_for_http; then
  /usr/bin/open "${URL}" || true
fi

wait "${STPID}"
