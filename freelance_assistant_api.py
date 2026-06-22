from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from datetime import datetime
import json
import os

app = FastAPI()

TASK_FILE = "tasks.json"


# ----------------------------
# DATA HELPERS
# ----------------------------
def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


# ----------------------------
# HOME PAGE (UI)
# ----------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    tasks = load_tasks()

    items = ""
    for t in tasks:
        items += f"<li>{t['task']} ({t['created']})</li>"

    return f"""
    <html>
        <head>
            <title>Freelance Assistant</title>
        </head>

        <body style="font-family: Arial; padding: 40px;">
            <h1>Freelance Assistant</h1>

            <h3>Add Task</h3>

            <form method="post" action="/tasks">
                <input name="task" placeholder="Enter task" />
                <button type="submit">Add</button>
            </form>

            <h3>Tasks</h3>
            <ul>
                {items}
            </ul>
        </body>
    </html>
    """


# ----------------------------
# GET TASKS (API)
# ----------------------------
@app.get("/tasks")
def get_tasks():
    return load_tasks()


# ----------------------------
# ADD TASK (FIXED FOR FORM INPUT)
# THIS FIXES YOUR "python-multipart" ERROR + JSON ERROR
# ----------------------------
@app.post("/tasks")
def add_task(task: str = Form(...)):
    tasks = load_tasks()

    tasks.append({
        "task": task,
        "created": str(datetime.now())
    })

    save_tasks(tasks)

    return {"status": "added", "task": task}


# ----------------------------
# OPTIONAL: JSON ENDPOINT (for API tools)
# ----------------------------
@app.post("/tasks/json")
def add_task_json(data: dict):
    tasks = load_tasks()

    task_text = data.get("task", "")

    tasks.append({
        "task": task_text,
        "created": str(datetime.now())
    })

    save_tasks(tasks)

    return {"status": "added", "task": task_text}


# ----------------------------
# LOCAL RUN SUPPORT
# ----------------------------
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)