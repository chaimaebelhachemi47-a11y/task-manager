from database import get_connection


def _simulate_email(action, title, due_date, due_time):
    when = f"{due_date} {due_time}".strip() or "no due date"
    print(f"[EMAIL] {action}: '{title}' | due: {when} | "
          f"reminder will be sent 15 min before due time.")


def create_task(title, description, priority,
                category, due_date, due_time):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks
        (title, description, priority,
         category, due_date, due_time)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, description, priority,
          category, due_date, due_time))
    conn.commit()
    conn.close()
    if due_date:
        _simulate_email("Task created", title, due_date, due_time)


def get_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM tasks ORDER BY due_date ASC, due_time ASC")
    tasks = cursor.fetchall()
    conn.close()
    return [dict(task) for task in tasks]


def get_task_by_id(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    conn.close()
    return dict(task) if task else None


def update_task(task_id, title, description,
                priority, category, due_date, due_time):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET title=?, description=?, priority=?,
            category=?, due_date=?, due_time=?
        WHERE id=?
    """, (title, description, priority,
          category, due_date, due_time, task_id))
    conn.commit()
    conn.close()
    if due_date:
        _simulate_email("Task updated", title, due_date, due_time)


def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


def toggle_complete(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET completed = CASE
            WHEN completed = 0 THEN 1 ELSE 0 END
        WHERE id = ?
    """, (task_id,))
    conn.commit()
    conn.close()


def reschedule_task(task_id, new_due_date):
    """Update only the due_date (used by drag-and-drop).
    Returns True if a row was updated, False if no task with that id exists."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET due_date=? WHERE id=?",
        (new_due_date, task_id))
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated


def search_tasks(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM tasks
        WHERE title LIKE ? OR description LIKE ?
        ORDER BY due_date ASC
    """, (f"%{keyword}%", f"%{keyword}%"))
    tasks = cursor.fetchall()
    conn.close()
    return [dict(task) for task in tasks]


def filter_tasks(category=None, priority=None,
                 completed=None,
                 date_from=None, date_to=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM tasks WHERE 1=1"
    params = []
    if category:
        query += " AND category = ?"
        params.append(category)
    if priority:
        query += " AND priority = ?"
        params.append(priority)
    if completed is not None:
        query += " AND completed = ?"
        params.append(completed)
    if date_from:
        query += " AND due_date >= ?"
        params.append(date_from)
    if date_to:
        query += " AND due_date <= ?"
        params.append(date_to)
    query += " ORDER BY due_date ASC"
    cursor.execute(query, params)
    tasks = cursor.fetchall()
    conn.close()
    return [dict(task) for task in tasks]