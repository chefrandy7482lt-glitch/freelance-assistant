from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from pricing_engine import calculate_price
from tdu_value_engine import compute_task_value
from tdu_domain_registry import get_registered_domains

app = FastAPI()

# Serve static frontend
app.mount("/static", StaticFiles(directory="static"), name="static")


# ---------------------------------------------------------
# ROOT ENDPOINT – SERVE FRONTEND
# ---------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    return FileResponse("static/index.html")


# ---------------------------------------------------------
# MAIN FREELANCE ASSISTANT ENDPOINT
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

    return {
        "task": user_task,
        "value_score": value_score,
        "price": price,
        "domains": domains,
        "status": "processed"
    }
