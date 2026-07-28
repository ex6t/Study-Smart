import sqlite3
from app.database.database import get_connection
from datetime import datetime

#Create the notes table tied to user
def create_notes_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )

    connection.commit()
    connection.close()
#create the save notes function
def save_note(user_id, title, content):
    connection = get_connection()
    cursor = connection.cursor()

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute(
        """
        INSERT INTO notes (
            user_id,
            title,
            content,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user_id,
            title,
            content,
            current_time,
            current_time
        )
    )

    connection.commit()
    connection.close()

    return True, "Note saved successfully."

#get saved notes using the user's id
def get_notes(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            title,
            content,
            created_at,
            updated_at
        FROM notes
        WHERE user_id = ?
        ORDER BY updated_at DESC
        """,
        (user_id,)
    )

    rows = cursor.fetchall()
    connection.close()
    notes = []
    for row in rows:
        notes.append(
            {
                "id": row[0],
                "title": row[1],
                "content": row[2],
                "created_at": row[3],
                "updated_at": row[4],
            }
        )
    return notes

#delete note from user
def delete_note(note_id, user_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        DELETE FROM notes
        WHERE id = ? AND user_id = ?
        """,
        (note_id, user_id)
    )
    connection.commit()

    deleted = cursor.rowcount > 0

    connection.close()

    return deleted

def update_note(note_id, user_id, title, content):
    connection = get_connection()
    cursor = connection.cursor()

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute(
        """
        UPDATE notes
        SET title = ?,
            content = ?,
            updated_at = ?
        WHERE id = ?
          AND user_id = ?
        """,
        (
            title,
            content,
            current_time,
            note_id,
            user_id
        )
    )

    connection.commit()

    note_was_updated = cursor.rowcount > 0

    connection.close()

    return note_was_updated
