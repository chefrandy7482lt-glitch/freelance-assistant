from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/", StaticFiles(directory="static", html=True), name="static")

class TaskRequest(BaseModel):
    task: str

@app.post("/orchestrate/task")
async def orchestrate_task(request: TaskRequest):
    task = request.task
    return {
        "task_received": task,
        "value_score": 82,
        "recommended_price": "",
        "deliverable": f"Structured output for: {task}"
    }
