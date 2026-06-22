from tdu_state_reconstructor import reconstruct_state
from tdu_event_memory import load_events
from copy import deepcopy
from datetime import datetime


# -----------------------------
# PREDICTION ENTRY POINT (GATED)
# -----------------------------
def predict_state(user_request: str):
    """
    Only runs when explicitly called by user intent.
    No background prediction allowed.
    """

    state = reconstruct_state()

    # HARD PRIVACY GATE
    if not is_prediction_request(user_request):
        return {
            "status": "prediction_blocked",
            "message": "Prediction layer is inactive unless explicitly requested."
        }

    return simulate_future_states(state)


# -----------------------------
# DETECT USER INTENT
# -----------------------------
def is_prediction_request(text: str):
    triggers = [
        "predict",
        "future",
        "simulate",
        "what will happen",
        "forecast",
        "projection",
        "next state"
    ]

    text = text.lower()
    return any(t in text for t in triggers)


# -----------------------------
# SIMULATION ENGINE
# -----------------------------
def simulate_future_states(state):
    scenarios = []

    # Scenario 1: Normal continuation
    s1 = deepcopy(state)
    s1["system_health"] = "ACTIVE_CONTINUING"
    s1["projection_type"] = "baseline"
    scenarios.append(s1)

    # Scenario 2: High load (more tasks)
    s2 = deepcopy(state)
    s2["task_count"] += 5
    s2["system_health"] = "HIGH_ACTIVITY"
    s2["projection_type"] = "stress"
    scenarios.append(s2)

    # Scenario 3: Idle decay
    s3 = deepcopy(state)
    s3["system_health"] = "IDLE_DEGRADATION"
    s3["projection_type"] = "decay"
    scenarios.append(s3)

    return {
        "timestamp": str(datetime.utcnow()),
        "base_state": state,
        "predictions": scenarios
    }