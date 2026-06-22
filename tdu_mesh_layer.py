from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# -------------------------
# INPUT MODEL
# -------------------------
class Task(BaseModel):
    task: str


# -------------------------
# SIMPLE "DIGIPRINT"
# (identity fingerprint placeholder)
# -------------------------
def get_digiprint(task: str):
    return {
        "identity": "user_local",
        "task_hash": hash(task) % 10000,
        "timestamp": str(datetime.now())
    }


# -------------------------
# LANGUAGE LAYER (intent simplification)
# -------------------------
def language_layer(task: str):
    t = task.lower()

    if "price" in t:
        return "pricing_request"
    if "proposal" in t:
        return "proposal_request"
    if "task" in t:
        return "task_request"

    return "general_request"


# -------------------------
# DOMAIN LAYER
# -------------------------
def domain_layer(intent: str):
    if intent == "pricing_request":
        return "pricing_domain"
    if intent == "proposal_request":
        return "freelance_domain"
    return "system_domain"


# -------------------------
# AGENTS (MESH NODES)
# -------------------------
def pricing_agent(task):
    return {"agent": "pricing", "price": len(task) * 2}


def value_agent(task):
    return {"agent": "value", "value": len(task) * 3}


def memory_agent(task):
    return {"agent": "memory", "memory_score": len(task.split())}


# -------------------------
# MESH ORCHESTRATOR
# -------------------------
def cognitive_mesh(task: str):
    digiprint = get_digiprint(task)
    intent = language_layer(task)
    domain = domain_layer(intent)

    results = {
        "digiprint": digiprint,
        "intent": intent,
        "domain": domain,
        "agents": []
    }

    # activate agents based on domain
    if domain == "pricing_domain":
        results["agents"].append(pricing_agent(task))

    elif domain == "freelance_domain":
        results["agents"].append(value_agent(task))
        results["agents"].append(memory_agent(task))

    else:
        results["agents"].append(memory_agent(task))

    return results


# -------------------------
# API ENDPOINT
# -------------------------
@app.post("/mesh")
def run_mesh(task: Task):
    return cognitive_mesh(task.task)