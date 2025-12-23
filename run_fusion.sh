#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"
WORKSPACE="$REPO_ROOT/workspace"
VENV="$WORKSPACE/.venv"
PY="$VENV/bin/python"
ENV_FILE="$WORKSPACE/.env"
ENV_EXAMPLE="$WORKSPACE/.env.example"
PID_DIR="$WORKSPACE/.run"
LOG_DIR="$WORKSPACE/logs"
mkdir -p "$PID_DIR" "$LOG_DIR"
MODE="${FUSION_MODE:-demo}"

SERVICES=(
  "broker/router.py"
  "agents/chatgpt/worker.py"
  "agents/grok/worker.py"
  "agents/judge/worker.py"
  "sim/grok_results_listener.py"
)

print_header() {
  echo "== MCP-FUSION =="
}

enter_workspace() {
  cd "$WORKSPACE"
}

ensure_env_file() {
  if [[ ! -f "$ENV_FILE" ]]; then
    echo "[ERROR] Missing $ENV_FILE"
    if [[ -f "$ENV_EXAMPLE" ]]; then
      echo "[HINT] Copy the template: cp \"$ENV_EXAMPLE\" \"$ENV_FILE\" and fill in your keys."
    fi
    exit 1
  fi
}

ensure_venv() {
  if [[ ! -x "$PY" ]]; then
    echo "[BOOTSTRAP] Creating venv at $VENV"
    python3 -m venv "$VENV"
  fi
  echo "[BOOTSTRAP] Installing python deps"
  "$PY" -m pip install -q --upgrade pip
  "$PY" -m pip install -q -r "$REPO_ROOT/requirements.txt"
}

load_env() {
  ensure_env_file
  # shellcheck source=/dev/null
  source "$REPO_ROOT/scripts/load_env.sh"
}

validate_keys() {
  if [[ "${FUSION_OFFLINE:-0}" == "1" ]]; then
    echo "[LAUNCH] Offline mode enabled; skipping API key validation."
    return
  fi
  local ok=1
  if [[ -z "${OPENAI_API_KEY:-}" ]]; then
    echo "[ERROR] OPENAI_API_KEY is not set."
    ok=0
  elif [[ "$OPENAI_API_KEY" == "YOUR_REAL_OPENAI_KEY_HERE" ]]; then
    echo "[ERROR] OPENAI_API_KEY still has placeholder value."
    ok=0
  fi

  if [[ -z "${XAI_API_KEY:-}" ]]; then
    echo "[ERROR] XAI_API_KEY is not set."
    ok=0
  elif [[ "$XAI_API_KEY" == "YOUR_REAL_XAI_KEY_HERE" ]]; then
    echo "[ERROR] XAI_API_KEY still has placeholder value."
    ok=0
  fi

  if [[ $ok -eq 0 ]]; then
    echo "[LAUNCH] Key validation failed."
    exit 1
  fi
}

ensure_redis() {
  if "$PY" - <<'PY' >/dev/null 2>&1
import redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)
r.ping()
PY
  then
    echo "[REDIS] Redis reachable on localhost:6379"
    return
  fi

  if command -v docker >/dev/null 2>&1; then
    echo "[REDIS] Starting redis via docker compose..."
    docker compose up -d redis >/dev/null
    sleep 1
    if "$PY" - <<'PY' >/dev/null 2>&1
import redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)
r.ping()
PY
    then
      echo "[REDIS] redis container online."
      return
    fi
  fi

  echo "[ERROR] Redis not reachable on 6379. Start it manually or install redis."
  exit 1
}

cleanup() {
  echo "[LAUNCH] Shutting down MCP-FUSION services..."
  for pidfile in "$PID_DIR"/*.pid; do
    [[ -e "$pidfile" ]] || continue
    if kill -0 "$(cat "$pidfile")" 2>/dev/null; then
      kill "$(cat "$pidfile")" 2>/dev/null || true
    fi
    rm -f "$pidfile"
  done
}

start_workers() {
  export PYTHONPATH="$WORKSPACE:${PYTHONPATH:-}"
  ensure_redis
  PIDS=()
  for service in "${SERVICES[@]}"; do
    local log_name pid_file
    log_name="$LOG_DIR/$(basename "${service%.*}").log"
    pid_file="$PID_DIR/$(basename "${service%.*}").pid"
    echo "[LAUNCH] Starting $service"
    "$PY" "$WORKSPACE/$service" >"$log_name" 2>&1 &
    pid=$!
    echo "$pid" >"$pid_file"
    PIDS+=("$pid")
  done
  echo "[LAUNCH] Background workers online."
}

start_demo() {
  start_workers
  trap cleanup EXIT
  "$PY" "$WORKSPACE/sim/orchestrator.py"
}

start_daemon() {
  start_workers
  echo "[LAUNCH] Daemon mode: workers running without orchestrator; stop with ./scripts/fusion_stop.sh"
  trap - EXIT
  wait
}

stop_services() {
  echo "[LAUNCH] Stopping MCP-FUSION processes..."
  cleanup
  pkill -f "broker/router.py" 2>/dev/null || true
  pkill -f "agents/chatgpt/worker.py" 2>/dev/null || true
  pkill -f "agents/grok/worker.py" 2>/dev/null || true
  pkill -f "agents/judge/worker.py" 2>/dev/null || true
  pkill -f "sim/grok_results_listener.py" 2>/dev/null || true
  pkill -f "sim/orchestrator.py" 2>/dev/null || true
  echo "[LAUNCH] Stop signal sent."
}

run_healthcheck() {
  echo "[LAUNCH] Running healthcheck..."
  "$PY" -m pip show psutil >/dev/null 2>&1 || "$PY" -m pip install -q psutil
  "$PY" "$WORKSPACE/tools/healthcheck.py"
}

run_submit_job() {
  local prompt="$1"
  if [[ -z "$prompt" ]]; then
    echo "[ERROR] Job submission requires a prompt."
    echo "Usage: $0 submit \"Your job prompt here\""
    exit 1
  fi
  echo "[LAUNCH] Submitting job: '$prompt'"
  "$PY" "$WORKSPACE/tools/submit_job.py" "$prompt"
}

status_services() {
  local redis_status="down"
  if [[ -x "$PY" ]] && "$PY" - <<'PY' >/dev/null 2>&1
import redis
redis.Redis(host="localhost", port=6379, decode_responses=True).ping()
PY
  then
    redis_status="up"
  elif command -v redis-cli >/dev/null 2>&1 && redis-cli -p 6379 ping >/dev/null 2>&1; then
    redis_status="up"
  fi
  echo "[STATUS] redis -> $redis_status"
  for service in "${SERVICES[@]}" "sim/orchestrator.py"; do
    if pgrep -f "$service" >/dev/null 2>&1; then
      echo "[STATUS] $service : running (pid(s) $(pgrep -f "$service" | tr '\n' ' '))"
    else
      echo "[STATUS] $service : stopped"
    fi
  done
}

COMMAND="${1:-start}"
shift || true

print_header

case "$COMMAND" in
  bootstrap)
    ensure_venv
    ;;
  start)
    ensure_env_file
    ensure_venv
    load_env
    validate_keys
    enter_workspace
    if [[ "$MODE" == "daemon" ]]; then
      start_daemon
    else
      start_demo
    fi
    ;;
  reload)
    stop_services
    ensure_env_file
    ensure_venv
    load_env
    validate_keys
    enter_workspace
    if [[ "$MODE" == "daemon" ]]; then
      start_daemon
    else
      start_demo
    fi
    ;;
  stop)
    stop_services
    ;;
  health)
  ensure_env_file
  ensure_venv
  load_env
  enter_workspace
  run_healthcheck
  ;;
  submit)
  ensure_env_file
  ensure_venv
  load_env
  enter_workspace
  run_submit_job "${1:-}"
  ;;
  status)
    status_services
    ;;
  *)
    echo "Usage: $0 [bootstrap|start|reload|stop|health|submit \"prompt\"|status]"
    exit 1
    ;;
esac
