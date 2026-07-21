from app.screens.welcome_screen import WelcomeWindow


# Stores the currently logged-in user
current_user = None


def start_session(username):
    """
    Creates a user session after successful login.
    """

    global current_user

    current_user = username



def end_session(current_window):
    """
    Logs out the current user.

    Clears the session,
    returns to the Welcome screen,
    and closes the current window.
    """

    global current_user

    # Clear current user session
    current_user = None

    # Return to Welcome screen
    welcome = WelcomeWindow()
    welcome.show()

    # Close Dashboard and sidebar
    current_window.close()



def is_logged_in():
    """
    Checks whether a user has an active session.

    Returns:
        True  -> user is logged in
        False -> no active user
    """

    return current_user is not None
