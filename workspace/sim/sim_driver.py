import json
import time
import argparse
import redis

CHANNEL_SIM = "fusion.sim"
CHANNEL_RESULTS = "fusion.results"
CHANNEL_TASKS = "fusion.tasks"

def connect():
    while True:
        try:
            r = redis.Redis(host="redis", port=6379, decode_responses=True)
            r.ping()
            print("SIM connected to Redis.")
            return r
        except Exception:
            print("SIM waiting for Redis...")
            time.sleep(1)

def test_publish():
    r = connect()
    payload = {
        "target": "sim",
        "action": "multiply",
        "value": 21
    }
    r.publish(CHANNEL_TASKS, json.dumps(payload))
    print("SIM test task published.")

def worker():
    r = connect()
    pubsub = r.pubsub()
    pubsub.subscribe(CHANNEL_SIM)
    print("sim_driver running...")

    for msg in pubsub.listen():
        if msg["type"] != "message":
            continue

        data = json.loads(msg["data"])
        result = {
            "source": "sim",
            "output": data.get("value") * 2
        }
        r.publish(CHANNEL_RESULTS, json.dumps(result))
        print("SIM processed:", result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-publish", action="store_true")
    args = parser.parse_args()

    if args.test_publish:
        test_publish()
    else:
        worker()