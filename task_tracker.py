import json
import os
import sys 

FILE_NAME = "tasks.json"
VALIDSTATUSES = {"todo", "in-progress", "done"}

def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []    

def save_tasks(tasks):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def next_id(tasks):
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1

def print_help():
    print(
        """
Commands:
  py task_tracker.py add "task description"
  py task_tracker.py list
  py task_tracker.py list todo
  py task_tracker.py list in-progress
  py task_tracker.py list done
  py task_tracker.py start <id>
  py task_tracker.py done <id>
  py task_tracker.py help

Examples:
  py task_tracker.py add "Buy milk"
  py task_tracker.py list
  py task_tracker.py start 1
  py task_tracker.py done 1
""".strip()
    )

def cmd_add(tasks, description):
    task = {
        "id": next_id(tasks),
        "description": description,
        "status": "todo",
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f'Added: [{task["id"]}] {task["status"]:<11} {task["description"]}')

def cmd_list(tasks, status=None):
    if status is not None and status not in VALIDSTATUSES:
        print(f"Unknown status: {status}")
        print("Valid statuses: todo, in-progress, done")
        return

    shown = [t for t in tasks if status is None or t["status"] == status]

    if not shown:
        print("No tasks yet." if status is None else f"No tasks with status '{status}'.")
        return

    for t in sorted(shown, key=lambda x: x["id"]):
        print(f'[{t["id"]}] {t["status"]:<11} {t["description"]}')

def find_task(tasks, task_id):
    for t in tasks:
        if t["id"] == task_id:
            return t
    return None

def cmd_set_status(tasks, task_id, new_status):
    task = find_task(tasks, task_id)
    if not task:
        print(f"Task not found: {task_id}")
        return
    task["status"] = new_status
    save_tasks(tasks)
    print(f'Updated: [{task["id"]}] {task["status"]:<11} {task["description"]}')

def cmd_delete(tasks, task_id):
    task = find_task(tasks, task_id)
    if not task:
        print(f"Task not found: {task_id}")
        return
    tasks.remove(task)
    save_tasks(tasks)
    print(f"Deleted task {task_id}")

def cmd_update(tasks, task_id, new_description):
    task = find_task(tasks, task_id)
    if not task:
        print(f"Task not found: {task_id}")
        return
    task["description"] = new_description
    save_tasks(tasks)
    print(f'Updated: [{task["id"]}] {task["status"]:<11} {task["description"]}')

def main():
    args = sys.argv[1:]
    tasks = load_tasks()

    if not args or args[0] in {"help", "-h", "--help"}:
        print_help()
        return

    cmd = args[0].lower()

    if cmd == "add":
        if len(args) < 2:
            print('Usage: py task_tracker.py add "task description"')
            return
        description = " ".join(args[1:]).strip().strip('"').strip("'")
        if not description:
            print("Task description cannot be empty.")
            return
        cmd_add(tasks, description)

    elif cmd == "list":
        if len(args) == 1:
            cmd_list(tasks)
        else:
            cmd_list(tasks, args[1].lower())

    elif cmd == "start":
        if len(args) != 2 or not args[1].isdigit():
            print("Usage: py task_tracker.py start <id>")
            return
        cmd_set_status(tasks, int(args[1]), "in-progress")

    elif cmd == "done":
        if len(args) != 2 or not args[1].isdigit():
            print("Usage: py task_tracker.py done <id>")
            return
        cmd_set_status(tasks, int(args[1]), "done")             

    elif cmd == "delete":
        if len(args) != 2 or not args[1].isdigit():
            print("Usage: py task_tracker.py delete <id>")
            return
        cmd_delete(tasks, int(args[1]))

    elif cmd == "update":
        if len(args) < 3 or not args[1].isdigit():
            print('Usage: py task_tracker.py update <id> "new description"')
            return
        new_desc = " ".join(args[2:]).strip().strip('"').strip("'")
        cmd_update(tasks, int(args[1]), new_desc)

    else:
        print(f"Unknown command: {cmd}")
        print_help()

if __name__ == "__main__":
    main()