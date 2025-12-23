"""
coordinator_worker.py - MCP-FUSION Coordinator Worker

This worker coordinates tasks between multiple AI models via Redis queues.
It processes tasks from the fusion_tasks queue and publishes results to
the plasma_results queue.

Usage:
    python -m workspace.workers.coordinator_worker

Environment Variables:
    FUSION_TASK_LIST: Redis list for incoming tasks (default: fusion_tasks)
    FUSION_RESULT_LIST: Redis list for results (default: plasma_results)
    REDIS_HOST: Redis host (default: localhost)
    REDIS_PORT: Redis port (default: 6379)
"""

import json
import os
import sys
import time
import logging
from typing import Dict, Any

try:
    import redis
except ImportError:
    print("ERROR: redis-py not installed. Run: pip install redis")
    sys.exit(1)


# Configuration
TASK_LIST = os.environ.get("FUSION_TASK_LIST", "fusion_tasks")
RESULT_LIST = os.environ.get("FUSION_RESULT_LIST", "plasma_results")
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
POLL_INTERVAL = float(os.environ.get("FUSION_POLL_INTERVAL", "0.5"))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("coordinator_worker")


class CoordinatorWorker:
    """Coordinator worker for MCP-FUSION orchestration."""

    def __init__(self):
        """Initialize the coordinator worker."""
        self.redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            decode_responses=True
        )
        logger.info(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
        logger.info(f"Listening on: {TASK_LIST}")
        logger.info(f"Publishing to: {RESULT_LIST}")

    def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a task payload.

        Args:
            task_data: Task payload with 'task' and optional 'constraints'

        Returns:
            Result dictionary
        """
        task = task_data.get("task", "")
        constraints = task_data.get("constraints", {})

        logger.info(f"Processing task: {task[:100]}...")

        # TODO: Implement actual multi-model fusion logic
        # For now, return a placeholder response
        result = {
            "status": "processed",
            "task": task,
            "response": f"Placeholder response for: {task}",
            "constraints": constraints,
            "models_used": ["placeholder"],
            "timestamp": time.time()
        }

        return result

    def run(self):
        """Main worker loop."""
        logger.info("Coordinator worker started. Press Ctrl+C to stop.")

        try:
            while True:
                # Block and wait for task (BRPOP with timeout)
                result = self.redis_client.brpop(TASK_LIST, timeout=1)

                if result:
                    _, task_json = result
                    
                    try:
                        task_data = json.loads(task_json)
                        logger.info(f"Received task from {TASK_LIST}")

                        # Process the task
                        result_data = self.process_task(task_data)

                        # Publish result
                        result_json = json.dumps(result_data)
                        self.redis_client.lpush(RESULT_LIST, result_json)
                        logger.info(f"Published result to {RESULT_LIST}")

                    except json.JSONDecodeError as e:
                        logger.error(f"Invalid JSON in task: {e}")
                    except Exception as e:
                        logger.error(f"Error processing task: {e}")

                else:
                    # No task received, continue polling
                    time.sleep(POLL_INTERVAL)

        except KeyboardInterrupt:
            logger.info("Coordinator worker stopped by user")
        except Exception as e:
            logger.error(f"Fatal error: {e}")
            raise


def main():
    """Entry point for the coordinator worker."""
    worker = CoordinatorWorker()
    worker.run()


if __name__ == "__main__":
    main()
