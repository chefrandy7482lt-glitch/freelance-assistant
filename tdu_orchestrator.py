from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

from pricing_engine import calculate_price
from tdu_value_engine import calculate_value
from tdu_domain_registry import classify_domain

app = FastAPI()


# -----------------------------
# DATA MODEL
# -----------------------------
class TaskIn(BaseModel):
    task: str


# -----------------------------
# CORE ORCHESTRATION FUNCTION
# -----------------------------
def orchestrate(task_text: str):
    domain = classify_domain(task_text)
    value = calculate_value(task_text, domain)
    price = calculate_price(value, domain)

    return {
        "task": task_text,
        "domain": domain,
        "value": value,
        "price": price,
        "timestamp": str(datetime.utcnow())
    }


# -----------------------------
# API LAYER (CLEAN ENTRYPOINT)
# -----------------------------
@app.get("/")
def root():
    return {
        "system": "TDU Orchestrator Active",
        "status": "online",
        "layer": "orchestration_core"
    }


@app.post("/task")
def run_task(task: TaskIn):
    result = orchestrate(task.task)
    return result