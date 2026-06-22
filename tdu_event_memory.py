from datetime import datetime
import json
import os
import uuid

EVENT_FILE = "tdu_event_log.json"


# -----------------------------
# LOAD EVENTS
# -----------------------------
def load_events():
    if os.path.exists(EVENT_FILE):
        with open(EVENT_FILE, "r") as f:
            return json.load(f)
    return []


# -----------------------------
# SAVE EVENTS
# -----------------------------
def save_events(events):
    with open(EVENT_FILE, "w") as f:
        json.dump(events, f, indent=2)


# -----------------------------
# CORE EVENT LOGGER
# -----------------------------
def log_event(event_type, payload=None, related_id=None):
    events = load_events()

    event = {
        "id": str(uuid.uuid4()),
        "event_type": event_type,
        "payload": payload or {},
        "related_id": related_id,
        "timestamp": str(datetime.utcnow())
    }

    events.append(event)
    save_events(events)

    return event


# -----------------------------
# QUERY EVENTS (TIME-BASED MEMORY)
# -----------------------------
def get_events(event_type=None):
    events = load_events()

    if event_type:
        return [e for e in events if e["event_type"] == event_type]

    return events


# -----------------------------
# EVENT STATE SNAPSHOT
# -----------------------------
def get_system_state():
    events = load_events()

    return {
        "total_events": len(events),
        "last_event": events[-1] if events else None,
        "event_types": list(set(e["event_type"] for e in events))
    }