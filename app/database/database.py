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


def change_password(user_id, current_password, new_password):
    """
    Changes a user's password after checking the current password.

    Returns:
        (True, message) if the password is changed.
        (False, message) if validation or the database update fails.
    """

    if user_id is None:
        return False, "User account could not be found."

    if current_password == "":
        return False, "Current password cannot be empty."

    if new_password == "":
        return False, "New password cannot be empty."

    if len(new_password) < 8:
        return False, "New password must be at least 8 characters."

    if len(new_password) > 20:
        return False, "New password cannot be more than 20 characters."

    if current_password == new_password:
        return False, "New password must be different from the current password."

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT password
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        )

        result = cursor.fetchone()

        if result is None:
            return False, "User account could not be found."

        if result[0] != current_password:
            return False, "Current password is incorrect."

        cursor.execute(
            """
            UPDATE users
            SET password = ?
            WHERE id = ?
            """,
            (new_password, user_id),
        )

        connection.commit()

        return True, "Password changed successfully."

    except sqlite3.Error:
        connection.rollback()
        return False, "The password could not be changed."

    finally:
        connection.close()


def delete_user_account(user_id, password):
    """
    Deletes a user and every database row connected to that user.

    The deletion is completed as one transaction so that a partial
    account deletion is not saved if a database operation fails.
    """

    if user_id is None:
        return False, "User account could not be found."

    if password == "":
        return False, "Password cannot be empty."

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT password
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        )

        result = cursor.fetchone()

        if result is None:
            return False, "User account could not be found."

        if result[0] != password:
            return False, "Password is incorrect."

        # Find every application table that stores data by user_id.
        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
              AND name != 'users'
            """
        )

        table_names = [row[0] for row in cursor.fetchall()]

        for table_name in table_names:
            safe_table_name = table_name.replace('"', '""')

            cursor.execute(
                f'PRAGMA table_info("{safe_table_name}")'
            )
            column_names = [row[1] for row in cursor.fetchall()]

            if "user_id" in column_names:
                cursor.execute(
                    f'DELETE FROM "{safe_table_name}" WHERE user_id = ?',
                    (user_id,),
                )

        cursor.execute(
            """
            DELETE FROM users
            WHERE id = ?
            """,
            (user_id,),
        )

        if cursor.rowcount == 0:
            connection.rollback()
            return False, "User account could not be found."

        connection.commit()

        return True, "Account and user data deleted successfully."

    except sqlite3.Error:
        connection.rollback()
        return False, "The account could not be deleted."

    finally:
        connection.close()
