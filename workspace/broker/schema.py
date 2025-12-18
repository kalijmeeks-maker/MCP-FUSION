#!/usr/bin/env python3
"""
schema.py
Message validation layer for MCP-FUSION system.

All inter-agent messages MUST conform to this schema before being accepted.
"""

import json
from typing import Any, Dict


REQUIRED_TOP_LEVEL_FIELDS = {
    "type",       # message type: "task", "heartbeat", "result"
    "task_id",    # unique ID for tracking tasks
    "source",     # name of sending agent
    "target",     # name of receiving agent
    "payload",    # detailed instructions/data
    "timestamp"   # unix timestamp
}


def validate_message(message: Dict[str, Any]) -> (bool, str):
    """
    Validates a message dict against the MCP-FUSION schema.
    
    Returns:
        (is_valid: bool, error_message: str)
    """

    # 1. Ensure it's a dict
    if not isinstance(message, dict):
        return False, "Message must be a dict."

    # 2. Check top-level required fields
    missing = REQUIRED_TOP_LEVEL_FIELDS - message.keys()
    if missing:
        return False, f"Missing required fields: {missing}"

    # 3. Validate 'type'
    if message["type"] not in ("task", "heartbeat", "result"):
        return False, f"Invalid message type '{message['type']}'."

    # 4. Validate 'payload'
    if not isinstance(message["payload"], dict):
        return False, "Payload must be a dict."

    # 5. Validate timestamp
    if not isinstance(message["timestamp"], int):
        return False, "Timestamp must be an integer (unix time)."

    return True, "OK"


def load_and_validate(raw_data: str) -> (bool, Dict[str, Any], str):
    """
    Attempts to parse a JSON string and validate it.
    
    Returns:
        (is_valid: bool, parsed_dict: dict or None, error: str)
    """

    try:
        message = json.loads(raw_data)
    except json.JSONDecodeError:
        return False, None, "Invalid JSON."

    valid, error = validate_message(message)
    return valid, message if valid else None, error
