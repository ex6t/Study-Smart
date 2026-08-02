import sys
import unittest
from unittest.mock import Mock, patch

from PyQt6.QtWidgets import QApplication, QLabel

from app.screens.flashcards_screen import FlashcardCreationScreen
from app.screens.frontpageFE import WelcomeWindow
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

class FlashcardCreationTests(unittest.TestCase):

    @patch("app.screens.flashcards_screen.save_flashcard",
           return_value=(True, "Flashcards saved successfully"),
           )
    def test_create_flashcard(self, save_flashcard_mock):
        screen = Mock()
        screen.user_id = 1
        screen.editing_flashcard_id = None

        screen.term_input.toPlainText.return_value = "What is the capital of California?"
        screen.definition_input.toPlainText.return_value = "Sacramento"
        screen.deck_combo.currentData.return_value = 3

        screen.message_label = Mock()
        screen.flashcard_updated = Mock()

        FlashcardCreationScreen.save_flashcard_pressed(screen)

        save_flashcard_mock.assert_called_once_with(
            1, 3, "What is the capital of California?", "Sacramento"
        )

        screen.flashcard_updated.emit.assert_called_once()

    def test_delete_flashcard(self):
        card = Mock()

        card.delete_requested = Mock()
        card.delete_requested.emit = Mock()

        flashcard = {
            "id": 7,
            "term": "What is the capital of California?",
            "definition": "Sacramento",
            "deck_id": 3,
            "deck_name": "Geography",
        }

        card.delete_requested.emit(flashcard)

        card.delete_requested.emit.assert_called_once_with(flashcard)


class ScreenInitializationTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication(sys.argv)

    @patch("app.screens.flashcards_screen.get_decks", return_value=[])
    def test_flashcards_screen_initialization(self, get_decks_mock):
        screen = FlashcardCreationScreen(user_id=1)

        self.assertEqual(screen.windowTitle(), "Study Smart - Flashcards")
        self.assertEqual(screen.width(), 1200)
        self.assertEqual(screen.height(), 800)
        self.assertEqual(screen.page_title.text(), "Create Flashcard")
        self.assertEqual(
            screen.term_input.placeholderText(),
            "Enter your flashcard term here...",
        )
        self.assertEqual(
            screen.definition_input.placeholderText(),
            "Enter your flashcard definition here...",
        )
        self.assertEqual(screen.view_flashcards_button.text(), "View Flashcards")
        self.assertEqual(screen.save_flashcard_button.text(), "Save Flashcard")
        self.assertEqual(screen.message_label.text(), "")

        screen.close()

    def test_welcome_window_initialization(self):
        screen = WelcomeWindow()
        screen.show()

        self.assertEqual(screen.windowTitle(), "Study Smart")
        self.assertEqual(screen.width(), 1200)
        self.assertEqual(screen.height(), 800)

        labels = screen.findChildren(QLabel)
        self.assertTrue(
            any(label.text() == "Welcome to Study Smart" for label in labels)
        )
        self.assertEqual(screen.signup_button.text(), "Sign Up")
        self.assertEqual(screen.login_button.text(), "Log In")
        self.assertTrue(screen.signup_button.isVisible())
        self.assertTrue(screen.login_button.isVisible())

        screen.close()

if __name__ == "__main__":
    unittest.main()
