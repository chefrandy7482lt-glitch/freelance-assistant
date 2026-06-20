from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime
import json
import os

app = FastAPI()

TASK_FILE = "tasks.json"


def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


class Task(BaseModel):
    task: str


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Freelance Assistant</title>
        </head>
        <body style="font-family: Arial; padding: 40px;">
            <h1>Freelance Assistant</h1>
            <p>System Online ✔</p>

            <h3>API</h3>
            <ul>
                <li>GET /tasks</li>
                <li>POST /tasks</li>
            </ul>
        </body>
    </html>
    """


@app.get("/tasks")
def get_tasks():
    return load_tasks()


@app.post("/tasks")
def add_task(item: Task):
    tasks = load_tasks()

    tasks.append({
        "task": item.task,
        "created": str(datetime.now())
    })

    save_tasks(tasks)

    return {"status": "added", "task": item.task}