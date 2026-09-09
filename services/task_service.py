from database import get_connection


def create_task(project_id, task):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO tasks (title, description, status, priority, project_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            task.title,
            task.description,
            task.status.value,
            task.priority.value,
            project_id
        )
    )

    connection.commit()

    task_id = cursor.lastrowid

    connection.close()

    return {
        "id": task_id,
        "title": task.title,
        "description": task.description,
        "status": task.status.value,
        "priority": task.priority.value,
        "project_id": project_id
    }


def get_tasks_for_project(project_id):
    connection = get_connection()

    tasks = connection.execute(
        """
        SELECT *
        FROM tasks
        WHERE project_id = ?
        """,
        (project_id,)
    ).fetchall()

    connection.close()

    return [dict(task) for task in tasks]


def update_task(task_id, task):
    connection = get_connection()

    connection.execute(
        """
        UPDATE tasks
        SET title = ?, description = ?, status = ?, priority = ?
        WHERE id = ?
        """,
        (
            task.title,
            task.description,
            task.status.value,
            task.priority.value,
            task_id
        )
    )

    connection.commit()

    updated_task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    connection.close()

    if updated_task is None:
        return None

    return dict(updated_task)


def delete_task(task_id):
    connection = get_connection()

    task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if task is None:
        connection.close()
        return False

    connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    return True