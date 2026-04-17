"""
Command-Line To-Do List App with File Persistence
===================================================
A feature-rich CLI application that lets users manage their tasks
with full CRUD operations and persistent JSON file storage.

Features:
  - Add tasks with title, description, and priority
  - View all tasks (with filtering by status)
  - Update existing tasks
  - Mark tasks as complete
  - Delete tasks
  - Persistent storage using a JSON file
"""

import json
import os
from datetime import datetime

# ─── Constants ────────────────────────────────────────────────────────────────

DATA_FILE = "tasks.json"

PRIORITIES = {"1": "Low", "2": "Medium", "3": "High"}

MENU = """
+----------------------------------------------+
|        TO-DO LIST APPLICATION                |
+----------------------------------------------+
|  1. Add Task                                 |
|  2. View All Tasks                           |
|  3. View Pending Tasks                       |
|  4. View Completed Tasks                     |
|  5. Update Task                              |
|  6. Mark Task as Complete                    |
|  7. Delete Task                              |
|  8. Search Tasks                             |
|  9. Exit                                     |
+----------------------------------------------+
"""

# ─── File Persistence Helpers ─────────────────────────────────────────────────


def load_tasks():
    """Load tasks from the JSON file. Returns an empty list if file doesn't exist."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as file:
            tasks = json.load(file)
            return tasks
    except (json.JSONDecodeError, IOError):
        print("[WARNING] Could not read tasks file. Starting with an empty list.")
        return []


def save_tasks(tasks):
    """Save the current task list to the JSON file."""
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(tasks, file, indent=4)
    except IOError:
        print("[ERROR] Could not save tasks to file.")


# ─── Task ID Generator ───────────────────────────────────────────────────────


def generate_id(tasks):
    """Generate the next unique task ID."""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


# ─── Core Features ───────────────────────────────────────────────────────────


def add_task(tasks):
    """Add a new task to the list."""
    print("\n-- Add New Task ------------------------------------")

    title = input("  Enter task title: ").strip()
    if not title:
        print("[ERROR] Task title cannot be empty.")
        return

    description = input("  Enter task description (optional): ").strip()

    print("  Select priority:")
    for key, value in PRIORITIES.items():
        print(f"    {key}. {value}")
    priority_choice = input("  Enter choice (1/2/3) [default: 2]: ").strip()
    priority = PRIORITIES.get(priority_choice, "Medium")

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
    print(f"[OK] Task '{title}' added successfully! (ID: {task['id']})")


def display_tasks(task_list):
    """Display a formatted table of tasks."""
    if not task_list:
        print("  No tasks found.")
        return

    # Header
    print(
        f"\n  {'ID':<5} {'Title':<25} {'Priority':<10} {'Status':<18} {'Created':<20}"
    )
    print("  " + "-" * 78)

    for task in task_list:
        status_icon = "[DONE]" if task["status"] == "Completed" else "[....]"
        print(
            f"  {task['id']:<5} {task['title']:<25} {task['priority']:<10} "
            f"{status_icon} {task['status']:<12} {task['created_at']:<20}"
        )
    print()


def view_all_tasks(tasks):
    """View all tasks."""
    print("\n-- All Tasks ---------------------------------------")
    display_tasks(tasks)


def view_pending_tasks(tasks):
    """View only pending tasks."""
    print("\n-- Pending Tasks -----------------------------------")
    pending = [t for t in tasks if t["status"] == "Pending"]
    display_tasks(pending)


def view_completed_tasks(tasks):
    """View only completed tasks."""
    print("\n-- Completed Tasks ---------------------------------")
    completed = [t for t in tasks if t["status"] == "Completed"]
    display_tasks(completed)


def find_task_by_id(tasks, task_id):
    """Find and return a task by its ID, or None if not found."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def update_task(tasks):
    """Update an existing task's title, description, or priority."""
    print("\n-- Update Task -------------------------------------")
    display_tasks(tasks)

    if not tasks:
        return

    try:
        task_id = int(input("  Enter task ID to update: ").strip())
    except ValueError:
        print("[ERROR] Invalid ID. Please enter a number.")
        return

    task = find_task_by_id(tasks, task_id)
    if not task:
        print(f"[ERROR] Task with ID {task_id} not found.")
        return

    print(f"\n  Current Title      : {task['title']}")
    print(f"  Current Description: {task['description']}")
    print(f"  Current Priority   : {task['priority']}")

    new_title = input(f"  New title (press Enter to keep '{task['title']}'): ").strip()
    new_desc = input(
        f"  New description (press Enter to keep current): "
    ).strip()

    print("  New priority (press Enter to keep current):")
    for key, value in PRIORITIES.items():
        print(f"    {key}. {value}")
    new_priority_choice = input("  Enter choice (1/2/3): ").strip()

    if new_title:
        task["title"] = new_title
    if new_desc:
        task["description"] = new_desc
    if new_priority_choice in PRIORITIES:
        task["priority"] = PRIORITIES[new_priority_choice]

    save_tasks(tasks)
    print(f"[OK] Task ID {task_id} updated successfully!")


def mark_complete(tasks):
    """Mark a task as completed."""
    print("\n-- Mark Task as Complete ---------------------------")
    pending = [t for t in tasks if t["status"] == "Pending"]
    display_tasks(pending)

    if not pending:
        return

    try:
        task_id = int(input("  Enter task ID to mark as complete: ").strip())
    except ValueError:
        print("[ERROR] Invalid ID. Please enter a number.")
        return

    task = find_task_by_id(tasks, task_id)
    if not task:
        print(f"[ERROR] Task with ID {task_id} not found.")
        return

    if task["status"] == "Completed":
        print(f"[INFO] Task '{task['title']}' is already completed.")
        return

    task["status"] = "Completed"
    task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    save_tasks(tasks)
    print(f"[OK] Task '{task['title']}' marked as complete!")


def delete_task(tasks):
    """Delete a task by its ID."""
    print("\n-- Delete Task -------------------------------------")
    display_tasks(tasks)

    if not tasks:
        return

    try:
        task_id = int(input("  Enter task ID to delete: ").strip())
    except ValueError:
        print("[ERROR] Invalid ID. Please enter a number.")
        return

    task = find_task_by_id(tasks, task_id)
    if not task:
        print(f"[ERROR] Task with ID {task_id} not found.")
        return

    confirm = (
        input(f"  Are you sure you want to delete '{task['title']}'? (y/n): ")
        .strip()
        .lower()
    )
    if confirm == "y":
        tasks.remove(task)
        save_tasks(tasks)
        print(f"[OK] Task '{task['title']}' deleted successfully!")
    else:
        print("  Deletion cancelled.")


def search_tasks(tasks):
    """Search tasks by title or description keyword."""
    print("\n-- Search Tasks ------------------------------------")

    keyword = input("  Enter search keyword: ").strip().lower()
    if not keyword:
        print("[ERROR] Search keyword cannot be empty.")
        return

    results = [
        t
        for t in tasks
        if keyword in t["title"].lower() or keyword in t["description"].lower()
    ]

    if results:
        print(f"  Found {len(results)} matching task(s):")
        display_tasks(results)
    else:
        print(f"  No tasks found matching '{keyword}'.")


# ─── Main Application Loop ───────────────────────────────────────────────────


def main():
    """Main application entry point."""
    tasks = load_tasks()

    print("\n  Welcome to the To-Do List App!")
    print("  Your tasks are saved automatically to", DATA_FILE)

    while True:
        print(MENU)
        choice = input("  Enter your choice (1-9): ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_all_tasks(tasks)
        elif choice == "3":
            view_pending_tasks(tasks)
        elif choice == "4":
            view_completed_tasks(tasks)
        elif choice == "5":
            update_task(tasks)
        elif choice == "6":
            mark_complete(tasks)
        elif choice == "7":
            delete_task(tasks)
        elif choice == "8":
            search_tasks(tasks)
        elif choice == "9":
            save_tasks(tasks)
            print("\n  Goodbye! Your tasks have been saved.")
            break
        else:
            print("  [ERROR] Invalid choice. Please enter a number between 1 and 9.")


if __name__ == "__main__":
    main()
