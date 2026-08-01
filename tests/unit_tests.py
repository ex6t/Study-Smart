import unittest
from unittest.mock import Mock, patch

from app.screens.login_screen import LoginView
from app.screens.settings_screen import SettingsScreen
from app.screens.planner_screen import PlannerScreen
from app.screens.all_plans_screen import AllPlansScreen

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
class PlannerScreensTest(unittest.TestCase):
    @patch("app.screens.planner_screen.save_plan",return_value=(True, "Plan Saved"))
    def test_create_plan(self, save_plan_mock):

        planner = Mock()

        planner.user_id = 1
        planner.editing_plan_id = None

        planner.plan_name_input.text.return_value = "Math"

        planner.plan_text_box.toPlainText.return_value = "Study Chapter 5"

        planner.styled_message = Mock()
        planner.reset_plan_form = Mock()
        planner.plan_updated = Mock()

        PlannerScreen.handle_save_plan(planner)

        save_plan_mock.assert_called_once_with(
            1,
            "Math",
            "Study Chapter 5"
        )

        planner.reset_plan_form.assert_called_once()
        planner.plan_updated.emit.assert_called_once()
    
    
    @patch("app.screens.planner_screen.update_plan",return_value=True)
    def test_update_plan(self, update_plan_mock):

        planner = Mock()

        planner.user_id = 1
        planner.editing_plan_id = 25

        planner.plan_name_input.text.return_value = "Updated Plan"
        planner.plan_text_box.toPlainText.return_value = "New Content"

        planner.styled_message = Mock()
        planner.reset_plan_form = Mock()
        planner.plan_updated = Mock()

        PlannerScreen.handle_save_plan(planner)

        update_plan_mock.assert_called_once_with(25,1,"Updated Plan","New Content")

        planner.reset_plan_form.assert_called_once()
        planner.plan_updated.emit.assert_called_once()

class AllPlansScreenTests(unittest.TestCase):

    @patch("app.screens.all_plans_screen.clear_all_plans",
           return_value=(True, "Plans cleared"))
    def test_clear_all_plans(self, clear_all_mock):

        screen = Mock()
        screen.user_id = 1
        screen.refresh_plans = Mock()

        AllPlansScreen.clear_all_plans(screen)

        clear_all_mock.assert_called_once_with(1)
        screen.refresh_plans.assert_called_once()


    def test_delete_plan_signal(self):

        screen = Mock()

        screen.delete_plan_requested = Mock()
        screen.delete_plan_requested.emit = Mock()

        plan = {
            "id": 1,
            "title": "Math",
            "content": "Study"
        }

        screen.delete_plan_requested.emit(plan)

        screen.delete_plan_requested.emit.assert_called_once_with(plan)

if __name__ == "__main__":
    unittest.main()
