# Task Tracker CLI

A simple command-line task tracker built with Python.  
It allows you to add, list, update, and manage tasks with different statuses.

## Features
- Add new tasks
- List all tasks
- Filter tasks by status (`todo`, `in-progress`, `done`)
- Mark tasks as in progress
- Mark tasks as done
- Update task descriptions
- Delete tasks
- Persistent storage using a JSON file

## Requirements
- Python 3.x

## How to Run

Navigate to the project folder and use the following commands:

```bash

Commands
py task_tracker.py help
py task_tracker.py add "Task description"
py task_tracker.py list
py task_tracker.py list todo
py task_tracker.py list in-progress
py task_tracker.py list done
py task_tracker.py start <id>
py task_tracker.py done <id>
py task_tracker.py update <id> "New description"
py task_tracker.py delete <id>

