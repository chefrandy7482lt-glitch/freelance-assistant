from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
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


@app.get("/", response_class=HTMLResponse)
def home():
    tasks = load_tasks()

    items = ""
    for t in tasks:
        items += f"<li>{t['task']} ({t['created']})</li>"

    return f"""
    <html>
        <body>
            <h1>Freelance Assistant</h1>

            <form method="post" action="/tasks">
                <input name="task" placeholder="Enter task"/>
                <button type="submit">Add</button>
            </form>

            <h3>Tasks</h3>
            <ul>
                {items}
            </ul>
        </body>
    </html>
    """


@app.get("/tasks")
def get_tasks():
    return load_tasks()


@app.post("/tasks")
def add_task(task: str = Form(...)):
    tasks = load_tasks()

    tasks.append({
        "task": task,
        "created": str(datetime.now())
    })

    save_tasks(tasks)

    return {"status": "added", "task": task}