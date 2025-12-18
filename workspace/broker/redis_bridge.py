import json
import time
import redis

CHANNEL_IN = "fusion.tasks"
CHANNEL_SIM = "fusion.sim"
CHANNEL_LLAMA = "fusion.llama"

def connect_redis():
    while True:
        try:
            r = redis.Redis(host="redis", port=6379, decode_responses=True)
            r.ping()
            print("Redis connected.")
            return r
        except Exception as e:
            print(f"Redis connection failed: {e}")
            time.sleep(2)

def main():
    r = connect_redis()
    pubsub = r.pubsub()
    pubsub.subscribe(CHANNEL_IN)
    print("Redis bridge running...")

    for msg in pubsub.listen():
        if msg["type"] != "message":
            continue

        raw = msg["data"]
        try:
            data = json.loads(raw)
        except:
            print("Invalid JSON:", raw)
            continue

        target = data.get("target")

        if target == "sim":
            r.publish(CHANNEL_SIM, json.dumps(data))
            print("→ forwarded to SIM:", data)

        elif target == "llama":
            r.publish(CHANNEL_LLAMA, json.dumps(data))
            print("→ forwarded to LLAMA:", data)

        else:
            print("⚠️ Unknown target:", data)

if __name__ == "__main__":
    main()