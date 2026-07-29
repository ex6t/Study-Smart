import unittest
from unittest.mock import Mock, patch

from app.screens.login_screen import LoginView
from app.screens.settings_screen import SettingsScreen


#TEST TO ENSURE A SUCCESSFUL LOGIN STARTS USER SESSION AND REDIRECTS THE USER
class LoginScreenTests(unittest.TestCase):
    #ARRANGE
    @patch("app.screens.login_screen.start_session")
    @patch(
        "app.screens.login_screen.login_user",
        return_value=(True, "Login successful"),
    )
    def test_user_login(self, login_user_mock, start_session_mock):
        #Create mock login screen
        login_screen = Mock()
        login_screen.username_input.text.return_value = "josh"
        login_screen.password_input.text.return_value = "password123"

        #ACT
        LoginView.login_check(login_screen)

        #ASSERTIONS
        login_user_mock.assert_called_once_with("josh", "password123")
        start_session_mock.assert_called_once_with("josh")
        login_screen.login_redirect.assert_called_once_with("josh")

#TEST TO ENSURE LOGOUT SENDS WINDOW TO END SESSION FOR USER
class SettingsScreenTests(unittest.TestCase):
    #ARRANGE
    @patch("app.screens.settings_screen.end_session")
    def test_user_logout(self, end_session_mock):
        #Create mock settings screen
        settings_screen = Mock()
        current_window = settings_screen.window.return_value

        #ACT
        SettingsScreen.logout_user(settings_screen)

        #ASSERTION
        end_session_mock.assert_called_once_with(current_window)


if __name__ == "__main__":
    unittest.main()
