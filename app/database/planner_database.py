import sqlite3

from app.database.database import get_connection


def create_planner_table():
    """
    Creates the planner table if it does not already exist.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS planner (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT (datetime('now','localtime')),

            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    connection.commit()
    connection.close()


def save_plan(user_id, title, content):
    """
    Saves a new planner entry for the specified user.
    """

    title = title.strip()
    content = content.strip()

    if title == "":
        return False, "Plan title cannot be empty."

    if content == "":
        return False, "Planner entry cannot be empty."

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO planner (
                user_id,
                title,
                content
            )

            VALUES (?, ?, ?)
            """,
            (
                user_id,
                title,
                content
            ),
        )

        connection.commit()

        return True, "Planner entry saved."

    except sqlite3.Error:
        return False, "Failed to save planner entry."

    finally:
        connection.close()


def load_plans(user_id):
    """
    Returns all planner entries for a user.
    """

    connection = get_connection()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            title,
            content,
            completed,
            created_at

        FROM planner

        WHERE user_id = ?

        ORDER BY created_at DESC
        """,
        (user_id,),
    )

    rows = cursor.fetchall()
    plans = [dict(row) for row in rows]

    connection.close()

    return plans


def delete_plan(plan_id):
    """
    Deletes a single planner entry.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM planner
            WHERE id = ?
            """,
            (plan_id,),
        )

        connection.commit()

        return True, "Planner entry deleted."

    except sqlite3.Error:
        return False, "Failed to delete planner entry."

    finally:
        connection.close()


def clear_all_plans(user_id):
    """
    Deletes all planner entries for a user.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM planner
            WHERE user_id = ?
            """,
            (user_id,),
        )

        connection.commit()

        return True, "All planner entries deleted."

    except sqlite3.Error:
        return False, "Failed to clear planner."

    finally:
        connection.close()

def update_plan(plan_id, user_id, title, content):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            UPDATE planner

            SET title = ?,
                content = ?

            WHERE id = ?
            AND user_id = ?
            """,
            (
                title,
                content,
                plan_id,
                user_id
            )
        )

        connection.commit()

        return True

    except sqlite3.Error:

        return False

    finally:

        connection.close()

def update_completed(plan_id, completed):
    """
    Updates whether a planner entry is completed.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE planner

            SET completed = ?

            WHERE id = ?
            """,
            (completed, plan_id),
        )

        connection.commit()

        return True, "Planner updated."

    except sqlite3.Error:
        return False, "Failed to update planner."

    finally:
        connection.close()


def get_plan(plan_id):
    """
    Returns a single planner entry.
    """

    connection = get_connection()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            user_id,
            title,
            content,
            completed,
            created_at

        FROM planner

        WHERE id = ?
        """,
        (plan_id,),
    )

    plan = cursor.fetchone()

    connection.close()

    return plan


def find_plan_by_title(user_id, title):

    connection = get_connection()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            title,
            content,
            completed,
            created_at

        FROM planner

        WHERE user_id = ?
        AND LOWER(title) LIKE LOWER(?)

        LIMIT 1
        """,
        (
            user_id,
            f"%{title}%"
        ),
    )

    plan = cursor.fetchone()

    connection.close()

    if plan is None:
        return None

    return dict(plan)
