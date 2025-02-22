# To-Do List

This repository contains a task management system with two implementations:
1. **FastAPI-based REST API** for managing tasks programmatically.
2. **Command Line Interface (CLI) Application** for interactive task management.

## Features
- Add, update, view, and delete tasks.
- Tasks have priorities (`low`, `med`, `high`), descriptions, and statuses.
- Tasks are stored in a SQLite database.
- Automatic priority ranking using a min-heap.
- CLI version with an interactive menu.
- REST API version for programmatic interaction.

---

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/task-manager.git
   cd task-manager
   ```
2. Install dependencies:
   ```sh
   pip install fastapi uvicorn pydantic sqlite3 colorama
   ```
3. Run the database initialization (handled automatically when the script runs).

---

## FastAPI REST API Usage

### Running the API Server
Start the FastAPI server with:
```sh
uvicorn api:app --reload
```

### API Endpoints
| Method | Endpoint          | Description                         |
|--------|------------------|-------------------------------------|
| `POST` | `/tasks/`        | Add a new task                     |
| `GET`  | `/tasks/`        | View all tasks                     |
| `PUT`  | `/tasks/{id}`    | Update task status                 |
| `DELETE` | `/tasks/{id}`  | Delete a task                      |

Example: Add a new task using `curl`:
```sh
curl -X POST "http://127.0.0.1:8000/tasks/" -H "Content-Type: application/json" \
-d '{"task_name": "Finish project", "description": "Complete the data science project", "priority": "high"}'
```

---

## CLI Usage
Run the CLI version by executing:
```sh
python cli.py
```

### CLI Options
1. Add a new task
2. View tasks
3. Update a task
4. Delete a task
5. Exit

Example interaction:
```sh
Options:
1) Add Task
2) View Tasks
3) Update Task
4) Delete Task
5) Exit
Choose an option: 1
Enter task name: Complete report
Enter task description: Write final project report
Enter task priority (low, med, high): high
Task, 'Complete report', added successfully.
```

---

## Database Structure
| Column          | Type    | Description                                |
|----------------|--------|--------------------------------------------|
| `id`          | INTEGER | Primary key, auto-incremented task ID     |
| `task_name`   | TEXT    | Name of the task                          |
| `description` | TEXT    | Description of the task                   |
| `priority`    | TEXT    | Task priority (`low`, `med`, `high`)      |
| `priority_ranking` | INTEGER | Automatically updated priority ranking |
| `status`      | TEXT    | Task status (`pending`, `in-progress`, `completed`) |
| `date_added`  | TEXT    | Timestamp when the task was created       |

---

## How It Works
- When a new task is added, it is assigned a priority ranking using a min-heap based on priority and timestamp.
- When a task is updated or deleted, the rankings are recalculated automatically.
- The FastAPI version provides a RESTful way to interact with tasks, while the CLI version is a simple interactive interface.

---

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to your branch (`git push origin feature-name`)
5. Open a Pull Request

---

## License
This project is licensed under the MIT License.

