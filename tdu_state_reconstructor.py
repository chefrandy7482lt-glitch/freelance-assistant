from tdu_event_memory import load_events
from datetime import datetime


# -----------------------------
# STATE RECONSTRUCTOR CORE
# -----------------------------
def reconstruct_state():
    events = load_events()

    state = {
        "system_health": "UNKNOWN",
        "task_count": 0,
        "last_task": None,
        "pricing_snapshot": None,
        "value_snapshot": None,
        "event_flow": [],
        "timestamp": str(datetime.utcnow())
    }

    for event in events:

        state["event_flow"].append(event["event_type"])

        # TASK TRACKING
        if event["event_type"] == "TASK_RECEIVED":
            state["task_count"] += 1
            state["last_task"] = event["payload"]

        # VALUE TRACKING
        if event["event_type"] == "VALUE_COMPUTED":
            state["value_snapshot"] = event["payload"]

        # PRICING TRACKING
        if event["event_type"] == "PRICING_COMPUTED":
            state["pricing_snapshot"] = event["payload"]

    # -----------------------------
    # SYSTEM HEALTH LOGIC
    # -----------------------------
    if state["task_count"] == 0:
        state["system_health"] = "IDLE"

    elif state["value_snapshot"] and state["pricing_snapshot"]:
        state["system_health"] = "ACTIVE"

    else:
        state["system_health"] = "PARTIAL"

    return state


# -----------------------------
# STATE INSPECTOR (DEBUG TOOL)
# -----------------------------
def get_state_summary():
    state = reconstruct_state()

    return {
        "health": state["system_health"],
        "tasks_processed": state["task_count"],
        "last_task": state["last_task"],
        "last_value": state["value_snapshot"],
        "last_pricing": state["pricing_snapshot"]
    }