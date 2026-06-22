from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import uuid
import json

from pricing_engine import calculate_price
from tdu_value_engine import compute_task_value
from tdu_domain_registry import get_registered_domains

app = FastAPI()

# Serve static folder (frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")


# ---------------------------------------------------------
# ROOT ENDPOINT – SERVE CUSTOMER PAGE
# ---------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    return FileResponse("static/index.html")


# ---------------------------------------------------------
# ORCHESTRATION LAYER – MAIN AI PIPELINE
# ---------------------------------------------------------
@app.post("/process_task")
async def process_task(request: Request):
    body = await request.json()
    user_task = body.get("task", "")

    # Value engine
    value_score = compute_task_value(user_task)

    # Pricing engine
    price = calculate_price(value_score)

    # Domain registry
    domains = get_registered_domains()

    response = {
        "task": user_task,
        "value_score": value_score,
        "price": price,
        "domains": domains,
        "status": "processed"
    }

    return response


# ---------------------------------------------------------
# NEW: CLOUD EVENT MIRROR ENDPOINT
# ---------------------------------------------------------
@app.post("/tdu/event")
async def tdu_event(request: Request):
    body = await request.json()

    event = {
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "source_system": body.get("source_system"),
        "event_type": body.get("event_type"),
        "payload": body.get("payload", {}),
        "vector": body.get("vector", {})
    }

    # Mirror event into Render logs
    print("\n--- CLOUD EVENT RECEIVED ---")
    print(json.dumps(event, indent=2))

    return {"status": "ok", "event": event}
