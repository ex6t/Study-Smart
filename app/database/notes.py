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
