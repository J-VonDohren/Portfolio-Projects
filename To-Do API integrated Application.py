from Fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import heapq
from datetime import datetime

class TaskCreate(BaseModel):
    task_name: str
    description: str
    priority: str

class TaskUpdate(BaseModel):
    status: str

app = FastAPI()

def get_db_connection():
    conn = sqlite3.connect("todo_list.db")
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the database
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        task_name TEXT NOT NULL,
        priority TEXT NOT NULL,
        priority_ranking INTEGER,
        description TEXT,
        status TEXT DEFAULT "pending",
        date_added TEXT)'''
    )
    conn.commit()
    conn.close()

init_db()

def update_priority_ranking():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, priority, date_added FROM tasks WHERE status != 'completed'")
    tasks = cursor.fetchall()

    priority_map = {'low': 3, 'med': 2, 'high': 1}
    heap = []
    for task in tasks:
        priority_value = priority_map.get(task["priority"].lower(), 3)
        date_value = datetime.strptime(task["date_added"], '%Y-%m-%d %H:%M:%S')
        heapq.heappush(heap, (priority_value, date_value, task["id"]))

    rank = 1
    while heap:
        _, _, task_id = heapq.heappop(heap)
        cursor.execute("UPDATE tasks SET priority_ranking = ? WHERE id = ?", (rank, task_id))
        rank += 1

    cursor.execute("UPDATE tasks SET priority_ranking = NULL WHERE status = 'completed'")
    conn.commit()
    conn.close()

@app.post("/tasks/")
def add_task(task: TaskCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    date_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO tasks (task_name, description, priority, date_added) VALUES (?, ?, ?, ?)", 
                   (task.task_name, task.description, task.priority.lower(), date_added))
    conn.commit()
    conn.close()
    update_priority_ranking()
    return {"message": "Task added successfully"}

@app.get("/tasks/")
def view_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return {"tasks": [dict(task) for task in tasks]}

@app.put("/tasks/{task_id}")
def update_task_status(task_id: int, task: TaskUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (task.status, task_id))
    conn.commit()
    conn.close()
    update_priority_ranking()
    return {"message": "Task updated successfully"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    update_priority_ranking()
    return {"message": "Task deleted successfully"}
