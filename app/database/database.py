#import bcrypt #to encrypt password later
import sqlite3
from pathlib import Path


# Finds the main Study-Smart project folder.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# The database file will be created in the project folder.
DATABASE_PATH = PROJECT_ROOT / "study_smart.db"


def get_connection():
    """
    Opens and returns a connection to the SQLite database.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    return connection


def create_users_table():
    """
    Creates the users table if it does not already exist.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()
    connection.close()

def username_exists(username):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(

        """

        SELECT id

        FROM users

        WHERE username = ?

        """,

        (username,),

    )

    result = cursor.fetchone()

    connection.close()

    return result is not None

def register_user(username, password):
    """
    Attempts to register a new user.

    Returns:
        (True, message) if registration succeeds.
        (False, message) if registration fails.
    """

    username = username.strip()

    if username == "":
        return False, "Username cannot be empty."

    if password == "":
        return False, "Password cannot be empty."

    #password_encrypt = bcrypt.hashpw(
     #   password.encode("utf-8"),
      #  bcrypt.gensalt(),
       # )

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (username, password)
            VALUES (?, ?)
            """,
            (username, password),#password_encrypt.decode("utf-8")),
        )

        connection.commit()

        return True, "Account created successfully."

    except sqlite3.IntegrityError:
        return False, "That username is already taken."

    finally:
        connection.close()

def login_user(username, password):

    username = username.strip()

    if username == "":
        return False, "Username cannot be empty"
    if password == "":
        return False, "Password cannot be empty"

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT password FROM users WHERE username = ?
            """,
            (username,),
        )

        row = cursor.fetchone()
        if row is None:
            return False, "Invalid username."
        stored_password = row[0]

        if password == stored_password:
            return True, "Login successful, redirecting..."
        else:
            return False, "Invalid password."

    except sqlite3.Error as e:
        return False, "Database error."
    finally:
        connection.close()

#Gets the numeric database ID for the logged in user
def get_user_id(username):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    result = cursor.fetchone()

    connection.close()

    if result is None:
        return None

    return result[0]

