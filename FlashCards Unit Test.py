import unittest # Import Python's built in unit testing framework
import sys
from PyQt6.QtWidgets import QApplication

from flashcards_screen import FlashcardsScreen


class TestFlashcardsScreen(unittest.TestCase):
    # Create a test class for the FlashcardsScreen
    # Any method beginning with "test_" will be automatically executed as a unit test
    @classmethod
    def setUpClass(cls):
        # Runs once before all tests
        # Creates a QApplication instance
        cls.app = QApplication.instance()

        if cls.app is None:
             # If no application exists, create one
            cls.app = QApplication(sys.argv)

    def setUp(self):
        # Runs before each test
        # Create a fresh FlashcardsScreen window for testing
        self.window = FlashcardsScreen()

    def tearDown(self): #Cleans the WelcomeWindow that was opened for testing so that the next test starts fresh
        self.window.close()

    def test_flashcards_screen_initialization(self):
       
        # Unit test that verifies that the Flashcards screen initializes correctly
        # Checks that the user interface elements are as expected 

        # Check that the window title is correct
        self.assertEqual(
            self.window.windowTitle(),
            "Study Smart - Flashcards"
        )
        # Check that the window size is correct
        self.assertEqual(self.window.width(), 1200)
        self.assertEqual(self.window.height(), 800)

        # Check page title
        self.assertEqual(
            self.window.page_title.text(),
            "Create Flashcard"
        )

        # Check question input
        self.assertEqual(
            self.window.question_input.placeholderText(),
            "Enter your flashcard question here..."
        )

        self.assertEqual(
            self.window.question_input.minimumHeight(),
            150
        )

        # Check answer input
        self.assertEqual(
            self.window.answer_input.placeholderText(),
            "Enter your flashcard answer here..."
        )

        self.assertEqual(
            self.window.answer_input.minimumHeight(),
            150
        )

        # Check buttons
        self.assertEqual(
            self.window.view_flashcards_button.text(),
            "View Flashcards"
        )

        self.assertEqual(
            self.window.save_flashcard_button.text(),
            "Save Flashcard"
        )

        # Check that the message label is empty when the screen first opens
        self.assertEqual(
            self.window.message_label.text(),
            ""
        )


if __name__ == "__main__":
    unittest.main() #Run the unit test when this file is executed directly
