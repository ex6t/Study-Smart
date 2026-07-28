import sqlite3
from app.database.database import get_connection

def create_flashcard_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS flashcards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        term TEXT NOT NULL,
        definition TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
    )

    connection.commit()
    connection.close()

def save_flashcard(user_id, term, definition):

    if term.strip() == "":
        return False, "Term cannot be empty"
    if definition.strip() == "":
        return False, "Definition cannot be empty"

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO flashcards (
                user_id,
                term, 
                definition
            )
            VALUES (?, ?, ?)
            """,
            (user_id, term, definition)
        )
        connection.commit()
        return True, "Flashcard saved successfully"
    except sqlite3.Error as e:
        return False, f"Database error: {e}"
    finally:
        connection.close()

