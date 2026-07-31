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
        CREATE TABLE IF NOT EXISTS decks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
    )

    connection.commit()
    connection.close()

def save_flashcard(user_id, deck_id, term, definition):

    if deck_id is None:
        return False, "You must choose a deck to add the card to"
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

    cursor.execute(
        """
        SELECT id, name
        FROM decks
        WHERE user_id = ? AND name = ?
        """,
        (user_id, name)
    )

    row = cursor.fetchone()
    connection.close()

    if row is None: return None
    return {
        "id": row[0],
        "name": row[1],
    }

# returns all decks for a user_id
def get_decks(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name
        FROM decks
        WHERE user_id = ?
        ORDER BY name ASC
        """,
        (user_id,)
    )

    rows = cursor.fetchall()
    connection.close()

    decks = []
    for row in rows:
        decks.append(
            {
                "id": row[0],
                "name": row[1],
            }
        )
    return decks

def get_flashcards(user_id, deck_id=None):
    connection = get_connection()
    cursor = connection.cursor()

    if deck_id is None:
        cursor.execute(
            """
            SELECT 
                flashcards.id
                flashcards.term
                flashcards.definition
                flashcards.deck_id
                decks.name
            FROM flashcards
            JOIN decks ON flashcards.deck_id = decks.id
            WHERE flashcards.user_id = ?
            ORDER by flashcards.id DESC
            """,
            (user_id,)
        )
    else:
        cursor.execute(
            """
            SELECT
                flashcards.id
                flashcards.term
                flashcards.definition
                flashcards.deck_id
                decks.name
            FROM flashcards
            JOIN decks ON flashcards.deck_id = decks.id
            WHERE flashcards.user_id = ? AND flashcard.deck_id = ?
            ORDER BY flashcards.id DESC
            """,
            (user_id, deck_id)
        )

    rows = cursor.fetchall()
    connection.close()

    flashcards = []
    for row in rows:
        flashcards.append(
            {
                "id": row[0],
                "term": row[1],
                "definition": row[2],
                "deck_id": row[3],
                "deck_name": row[4],
            }
        )
    return flashcards