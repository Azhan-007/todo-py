"""
Flask To-Do List Application with File Persistence
====================================================
A modern web-based task management app using Flask
with persistent JSON file storage.
"""

import json
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# ─── Constants ────────────────────────────────────────────────────────────────

DATA_FILE = "tasks.json"


# ─── File Persistence Helpers ─────────────────────────────────────────────────

def load_tasks():
    """Load tasks from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_tasks(tasks):
    """Save tasks to the JSON file."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(tasks, f, indent=4)
    except IOError:
        pass


def generate_id(tasks):
    """Generate the next unique task ID."""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Main page - display all tasks."""
    tasks = load_tasks()
    filter_type = request.args.get("filter", "all")

    if filter_type == "pending":
        filtered = [t for t in tasks if t["status"] == "Pending"]
    elif filter_type == "completed":
        filtered = [t for t in tasks if t["status"] == "Completed"]
    else:
        filtered = tasks

    # Stats
    total = len(tasks)
    pending = len([t for t in tasks if t["status"] == "Pending"])
    completed = len([t for t in tasks if t["status"] == "Completed"])

    return render_template(
        "index.html",
        tasks=filtered,
        filter_type=filter_type,
        total=total,
        pending=pending,
        completed=completed,
    )


@app.route("/add", methods=["POST"])
def add_task():
    """Add a new task."""
    tasks = load_tasks()

    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    priority = request.form.get("priority", "Medium")

    if not title:
        return redirect(url_for("index"))

    task = {
        "id": generate_id(tasks),
        "title": title,
        "description": description,
        "priority": priority,
        "status": "Pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "completed_at": None,
    }

    tasks.append(task)
    save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    """Mark a task as completed."""
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "Completed"
            task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break

    save_tasks(tasks)
    return redirect(request.referrer or url_for("index"))


@app.route("/undo/<int:task_id>", methods=["POST"])
def undo_task(task_id):
    """Mark a completed task back to pending."""
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "Pending"
            task["completed_at"] = None
            break

    save_tasks(tasks)
    return redirect(request.referrer or url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    """Delete a task."""
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    return redirect(request.referrer or url_for("index"))


@app.route("/update/<int:task_id>", methods=["POST"])
def update_task(task_id):
    """Update a task's details."""
    tasks = load_tasks()

    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    priority = request.form.get("priority", "Medium")

    for task in tasks:
        if task["id"] == task_id:
            if title:
                task["title"] = title
            task["description"] = description
            task["priority"] = priority
            break

    save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/search")
def search():
    """Search tasks by keyword."""
    tasks = load_tasks()
    keyword = request.args.get("q", "").strip().lower()

    if keyword:
        results = [
            t for t in tasks
            if keyword in t["title"].lower() or keyword in t["description"].lower()
        ]
    else:
        results = tasks

    total = len(tasks)
    pending = len([t for t in tasks if t["status"] == "Pending"])
    completed = len([t for t in tasks if t["status"] == "Completed"])

    return render_template(
        "index.html",
        tasks=results,
        filter_type="search",
        search_query=keyword,
        total=total,
        pending=pending,
        completed=completed,
    )


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5050))
    app.run(debug=False, host="0.0.0.0", port=port)
