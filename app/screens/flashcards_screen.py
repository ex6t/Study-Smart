import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QTextEdit,
    QPushButton,
    QVBoxLayout, # Creates vertical layout
    QHBoxLayout, # Creates a horizontal layout
    QWidget,
)

from app.database.flashcards import (
    save_flashcard, get_flashcards
)


class FlashcardsScreen(QWidget):
    def __init__(self, user_id):
        super().__init__()

        self.setWindowTitle("Study Smart - Flashcards")

        self.user_id = user_id

        self.setFixedSize(1200, 800)

        # Calls the function that creates all widgets
        self.setup_ui()
        self.connect_buttons()

    def setup_ui(self):
        # Main page layout
        main_layout = QVBoxLayout()

        self.setStyleSheet("""
                    QWidget {
                        background-color: rgb(240,240,240);
                        color: black;
                    }

                    QLabel {
                        color: black;
                    }

                    QScrollArea {
                        border: none;
                        background: rgb(240,240,240);
                    }

                    QScrollArea > QWidget > QWidget {
                        background: rgb(240,240,240);
                    }
                """)

        # Add spacing around the page.
        main_layout.setContentsMargins(40, 30, 40, 30)#(left, top, right, bottom)

        # Space between widgets.
        main_layout.setSpacing(15)

        # --------------------------------
        # Page Title
        # --------------------------------
        self.page_title = QLabel("Create Flashcard")

        #Center the title 
        self.page_title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        
        #Get the current font used and change size/make text bold
        title_font = self.page_title.font()
        title_font.setPointSize(24)
        title_font.setBold(True)
        
        #apply font changes
        self.page_title.setFont(title_font)
        
        #Place title inside vertical layout
        main_layout.addWidget(self.page_title)

        # --------------------------------
        # Question Input
        # --------------------------------
        question_label = QLabel("Question")

        #Create text box
        self.question_input = QTextEdit()
        self.question_input.setPlaceholderText(
            "Enter your flashcard question here..."
        )

        # Make the box 150 pixels tall (just a good size to where user can input good amount of text)
        self.question_input.setMinimumHeight(150)

        # Add question label to the page
        main_layout.addWidget(question_label)

        # Add the question text box below the label
        main_layout.addWidget(self.question_input)

        # --------------------------------
        # Answer Input
        # --------------------------------

        # Create a label that says "Answer"
        answer_label = QLabel("Answer")

        # Create a large text box for the answer 
        self.answer_input = QTextEdit()

        # Add placeholder text for answer box
        self.answer_input.setPlaceholderText(
            "Enter your flashcard answer here..."
        )

        # Make answer box 150 pixels tall as well 
        self.answer_input.setMinimumHeight(150)

        # Add answer label to the page
        main_layout.addWidget(answer_label)

        # Add answer input box below the label
        main_layout.addWidget(self.answer_input)

        # --------------------------------
        # Message Label
        # --------------------------------
        # Placeholder for future use (message pop up showing the flashcard was saved successfully)
        self.message_label = QLabel("")

        # Center the message text 
        self.message_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # Add message label to the layout
        main_layout.addWidget(self.message_label)

        # --------------------------------
        # Bottom Buttons
        # --------------------------------

        # Create a horizontal layout
        button_layout = QHBoxLayout()

        # Create button labeled "View Flashcards"
        self.view_flashcards_button = QPushButton(
            "View Flashcards"
        )

        # Create button labeled "Save Flashcard"
        self.save_flashcard_button = QPushButton(
            "Save Flashcard"
        )

        # Place View Flashcards button on the left side
        button_layout.addWidget(
            self.view_flashcards_button
        )

        # Add invisible space which pushes save button to the right
        button_layout.addStretch()

        # Place Save Flashcard button to the right side
        button_layout.addWidget(
            self.save_flashcard_button
        )

        # Add horizontal button layout to main vertical layout
        main_layout.addLayout(button_layout)

        # Apply finished layout to window
        self.setLayout(main_layout)

    def connect_buttons(self):
        self.save_flashcard_button.clicked.connect(self.save_flashcard_pressed)

        self.view_flashcards_button.clicked.connect(self.view_flashcards_pressed)

    def save_flashcard_pressed(self):
        question = self.question_input.toPlainText().strip()
        answer = self.answer_input.toPlainText().strip()

        if question == "":
            self.message_label.setText("Please enter your flashcard question")
            return
        if answer == "":
            self.message_label.setText("Please enter your flashcard answer")
            return

        success, message = save_flashcard(self.user_id, question, answer)
        self.message_label.setText(message)


    def view_flashcards_pressed(self):
        flashcards = get_flashcards(self.user_id)
        for flashcard in flashcards:
            print(flashcard)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = FlashcardsScreen()
    window.show()

    sys.exit(app.exec())
