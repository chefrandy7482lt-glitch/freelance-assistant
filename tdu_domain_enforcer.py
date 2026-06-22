from tdu_event_memory import load_events


# -----------------------------
# DOMAIN REGISTRY
# -----------------------------
DOMAIN_RULES = {
    "freelance": {
        "allowed_engines": ["value_engine", "pricing_engine"],
        "can_access_state": True,
        "can_predict": True
    },

    "accounting": {
        "allowed_engines": ["pricing_engine"],
        "can_access_state": True,
        "can_predict": False
    },

    "system": {
        "allowed_engines": ["orchestrator", "state_reconstructor"],
        "can_access_state": True,
        "can_predict": True
    }
}


# -----------------------------
# DOMAIN DETECTOR
# -----------------------------
def detect_domain(task_text: str):
    text = task_text.lower()

    if "invoice" in text or "pricing" in text:
        return "accounting"

    if "task" in text or "freelance" in text:
        return "freelance"

    return "system"


# -----------------------------
# DOMAIN ENFORCER (CORE LOGIC)
# -----------------------------
def enforce_domain(task_text: str):
    domain = detect_domain(task_text)
    rules = DOMAIN_RULES.get(domain, DOMAIN_RULES["system"])

    return {
        "domain": domain,
        "allowed_engines": rules["allowed_engines"],
        "can_access_state": rules["can_access_state"],
        "can_predict": rules["can_predict"]
    }


# -----------------------------
# SAFETY GATE (HARD BOUNDARY)
# -----------------------------
def validate_engine_access(domain, engine_name):
    rules = DOMAIN_RULES.get(domain, {})

    return engine_name in rules.get("allowed_engines", [])


# -----------------------------
# DOMAIN-AWARE ROUTING
# -----------------------------
def route_task(task_text, engine_name):
    enforcement = enforce_domain(task_text)

    if not validate_engine_access(enforcement["domain"], engine_name):
        return {
            "status": "DENIED",
            "reason": f"{engine_name} not allowed in {enforcement['domain']} domain"
        }

    return {
        "status": "ALLOWED",
        "domain": enforcement["domain"],
        "engine": engine_name
    }