import sqlite3
import heapq
from datetime import datetime
from colorama import Fore, Style

# Connect to the SQLite database
conn = sqlite3.connect('todo_list.db')
cursor = conn.cursor()

cursor.execute(
    '''CREATE TABLE IF NOT EXISTS 
    tasks (
    id INTEGER PRIMARY KEY,
    task_name TEXT NOT NULL,
    priority TEXT NOT NULL,
    priority_ranking Integer,
    description TEXT,
    status TEXT DEFAULT "pending",
    date_added TEXT)'''
               )
#save the new created table to the database
conn.commit()

def update_priority_ranking():
    #only tasks that arent completed should be selected and ranked for priority
    cursor.execute("SELECT id, priority, date_added FROM tasks WHERE status != 'completed'")
    Not_completed_tasks = cursor.fetchall()

    # Convert priority text to numerical values (lower number = higher priority)
    priority_map = {'low': 3, 'med': 2, 'high': 1}

    heap = []
    for task_id, priority, date_added in Not_completed_tasks:
        priority_value = priority_map.get(priority.lower(), 3)  # Default to 'low' if unknown
        date_value = datetime.strptime(date_added, '%Y-%m-%d %H:%M:%S')  
        heapq.heappush(heap, (priority_value, date_value, task_id))

    # Assign rankings to pending tasks
    rank = 1
    while heap:
        _, _, task_id = heapq.heappop(heap)
        cursor.execute("UPDATE tasks SET priority_ranking = ? WHERE id = ?", (rank, task_id))
        rank += 1

    # Set completed tasks priority ranking to NULL as they should not be ranked
    cursor.execute("UPDATE tasks SET priority_ranking = NULL WHERE status = 'completed'")
    conn.commit()

def add_task(task_name, description, priority):
    date_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
                   INSERT INTO tasks (task_name, description, priority, status, date_added)
                   VALUES (?, ?, ?, 'pending', ?)
                   ''', (task_name, description, priority.lower(), date_added))
    conn.commit()
    update_priority_ranking() # updates the priority ranking according to the new task added
    print(Fore.GREEN + f"Task, '{task_name}', added successfully." + Style.RESET_ALL)

def view_tasks():
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    print("\nCurrent Tasks:")
    for task in tasks:
        print(Fore.CYAN + f"ID: {task[0]} Name: {task[1]}, Status: {task[5]}, Added: {task[6]}" + Style.RESET_ALL)

def update_task_status(task_id, new_status):
    cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (new_status, task_id))
    conn.commit()
    update_priority_ranking()
    print(Fore.YELLOW + f"Task ID {task_id} updated to '{new_status}'." + Style.RESET_ALL)

def delete_task(task_id):
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    update_priority_ranking()
    print(Fore.RED + f"Task ID {task_id} deleted." + Style.RESET_ALL)


# Main loop
while True:
    print("\nOptions: \n1) Add Task \n2) View Tasks \n3) Update Task \n4) Delete Task \n5) Exit")
    choice = input("Choose an option: ")
    if choice == '1':
        task_name = input("Enter task name: ")
        description = input("Enter task description: ")
        priority = input("Enter task priority (low, med, high): ")
        add_task(task_name, description, priority)
    elif choice == '2':
        view_tasks()
    elif choice == '3':
        task_id = input("Enter the ID of the task to update: ")
        new_status = input("Enter new status (pending, in-progress, complete): ")
        update_task_status(task_id, new_status)
    elif choice == '4':
        task_id = input("Enter the ID of the task to delete: ")
        delete_task(task_id)
    elif choice == '5':
        break
    else:
        print("Invalid option. Please try again.")

conn.close()