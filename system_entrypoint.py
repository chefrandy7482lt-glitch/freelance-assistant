from fastapi import FastAPI
from freelance_assistant_api import app as freelance_app
from tdu_orchestrator import app as orchestrator_app

# -----------------------------
# TDU SYSTEM ENTRYPOINT (ROOT)
# -----------------------------

system = FastAPI(title="TDU Unified System")

# Mount freelance system
system.mount("/freelance", freelance_app)

# Mount orchestrator system
system.mount("/orchestrator", orchestrator_app)


@system.get("/")
def root():
    return {
        "system": "TDU ACTIVE",
        "layers": [
            "freelance_assistant",
            "pricing_engine",
            "value_engine",
            "domain_registry",
            "orchestrator"
        ],
        "status": "GEOMETRICALLY ALIGNED"
    }