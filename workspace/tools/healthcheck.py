# [NEW] /Users/kalimeeks/GEMINI-STACK/workspace/MCP-FUSION/workspace/tools/healthcheck.py
import os
import redis
import psutil
import sys

# Add workspace to Python path to allow for broker imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from broker.heartbeat import HEARTBEAT_CHANNEL

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

# --- Helper Functions ---

def get_process_status(script_name):
    """Find a running python process by its command line script name."""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if proc.info['name'] == 'python3' and script_name in ' '.join(proc.info['cmdline']):
            return "✅ RUNNING", proc.info['pid']
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
        return "✅ ALIVE", last_heartbeat
    else:
        return "⚠️ NO HEARTBEAT", "---"

# --- Main Execution ---

def run_healthcheck():
    """Prints a formatted table of service statuses."""
    print("--- MCP-FUSION Healthcheck ---")
    
    # Check Redis & Broker Heartbeat
    redis_status, heartbeat_time = check_redis_heartbeat()
    print(f"{ 'Redis Server:':<20} {redis_status:<15} (Last broker heartbeat: {heartbeat_time})")
    
    print("-" * 60)
    print(f"{ 'Service':<20} {'Status':<15} {'PID':<10}")
    print("=" * 60)

    all_ok = redis_status.startswith("✅")
    
    # Check Python application processes
    for service_name, script_path in SERVICE_PROCESS_MAP.items():
        status, pid = get_process_status(script_path)
        print(f"{service_name:<20} {status:<15} {pid:<10}")
        if "STOPPED" in status:
            all_ok = False
            
    print("-" * 60)

    if all_ok:
        print("\n✅ All systems nominal.")
        sys.exit(0)
    else:
        print("\n❌ One or more services are down.")
        sys.exit(1)

if __name__ == "__main__":
    # Note: This script requires the 'psutil' library.
    # Install it in your virtualenv:
    # pip install psutil
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
