import os
import redis
import psutil
import sys
import time

# --- Configuration ---
SERVICE_PROCESS_MAP = {
    "Broker": "broker/router.py",
    "ChatGPT Worker": "agents/chatgpt/worker.py",
    "Grok Worker": "agents/grok/worker.py",
    "Judge Worker": "agents/judge/worker.py",
    "Results Listener": "sim/grok_results_listener.py",
}

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
ALLOW_STOPPED = os.environ.get("FUSION_HEALTH_ALLOW_STOPPED", "").lower() in ("1", "true", "yes")


def get_process_status(script_name):
    """Find a running python process by its command line script name."""
    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        name = (proc.info["name"] or "").lower()
        if name.startswith("python") and script_name in " ".join(proc.info["cmdline"]):
            return "✅ RUNNING", proc.info["pid"]
    return "❌ STOPPED", "---"


def check_redis_heartbeat():
    """Check if the Redis server is up and if the broker has sent a recent heartbeat."""
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        r.ping()
    except redis.exceptions.ConnectionError:
        return "❌ OFFLINE", "---"

    last_heartbeat = r.get("broker_heartbeat")
    if last_heartbeat:
        age = time.time() - float(last_heartbeat)
        status = "✅ ALIVE" if age < 15 else "⚠️ STALE"
        return status, f"{age:.1f}s ago"
    else:
        return "⚠️ NO HEARTBEAT", "---"


def run_healthcheck():
    """Prints a formatted table of service statuses."""
    print("--- MCP-FUSION Healthcheck ---")

    redis_status, heartbeat_time = check_redis_heartbeat()
    print(f"{'Redis Server:':<20} {redis_status:<15} (Last broker heartbeat: {heartbeat_time})")

    print("-" * 60)
    print(f"{'Service':<20} {'Status':<15} {'PID':<10}")
    print("=" * 60)

    all_ok = redis_status.startswith("✅") or ALLOW_STOPPED

    for service_name, script_path in SERVICE_PROCESS_MAP.items():
        status, pid = get_process_status(script_path)
        print(f"{service_name:<20} {status:<15} {pid:<10}")
        if "STOPPED" in status and not ALLOW_STOPPED:
            all_ok = False

    print("-" * 60)

    if all_ok:
        print("\n✅ All systems nominal.")
        sys.exit(0)
    else:
        print("\n❌ One or more services are down.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        run_healthcheck()
    except ImportError:
        print("\n[ERROR] The 'psutil' library is not installed.")
        print("Please activate your virtual environment and run:")
        print("pip install psutil")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")
        sys.exit(1)
