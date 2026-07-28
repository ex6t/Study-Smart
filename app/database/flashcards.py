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
        deck_id INTEGER NOT NULL,
        term TEXT NOT NULL,
        definition TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
        FOREIGN KEY (deck_id) REFERENCES decks (id)
        )
        """
    )

    connection.commit()
    connection.close()

def create_decks_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS flashcards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL
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
                id,
                user_id,
                deck_id,
                term, 
                definition
            )
            VALUES (?, ?, ?, ?)
            """,
            (user_id, term, definition)
        )
        connection.commit()
        return True, "Flashcard saved successfully"
    except sqlite3.Error as e:
        return False, f"Database error: {e}"
    finally:
        connection.close()

def save_deck(user_id, name):
    if name.strip() == "":
        return False, "Name cannot be empty"

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO decks (
            user_id, name
            )
            VALUES (?, ?)
            """,
            (user_id, name)
        )
        connection.commit()
        return True, "Deck saved successfully"
    except sqlite3.Error as e:
        return False, f"Database error: {e}"
    finally:
        connection.close()

def get_deck(user_id, name):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute()

def get_flashcards(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            deck_id,
            term,
            definition
        FROM flashcards
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,)
    )

    rows = cursor.fetchall()
    connection.close()
    flashcards = []
    for row in rows:
        flashcards.append(
            {
                "id": row[0],
                "deck_id": row[1],
                "term": row[1],
                "definition": row[2],
            }
        )
    return flashcards

def get_answer(question):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        
        """
    )