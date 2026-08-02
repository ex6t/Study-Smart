import sys

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QTextEdit,
    QPushButton,
    QVBoxLayout,  # Creates vertical layout
    QHBoxLayout,  # Creates a horizontal layout
    QWidget, QComboBox, QInputDialog,
)

from app.database.flashcards import (
    save_flashcard, get_flashcards, get_decks, save_deck, get_deck, update_flashcard
)


class FlashcardCreationScreen(QWidget):

    flashcard_updated = pyqtSignal()

    def __init__(self, user_id):
        super().__init__()

        self.editing_flashcard_id = None
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

        sidebar_button_style = """
                   QPushButton {
                       background-color: rgb(205,220,245);
                       color: black;
                       border: 1px solid rgb(170,185,210);
                       border-radius: 8px;
                       padding: 6px 14px;
                       font-size: 12px;
                       font-weight: bold;
                   }

                   QPushButton:hover {
                       background-color: rgb(185,205,240);
                   }

                   QPushButton:pressed {
                       background-color: rgb(165,190,230);
                   }
               """

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

        deck_label = QLabel("Deck")
        deck_row = QHBoxLayout()

        self.deck_combo = QComboBox()
        self.deck_combo.setStyleSheet("background-color: white;")
        self.new_deck_button = QPushButton("New Deck")

        deck_row.addWidget(self.deck_combo)
        deck_row.addWidget(self.new_deck_button)

        main_layout.addWidget(deck_label)
        main_layout.addLayout(deck_row)

        self.refresh_decks()

        # --------------------------------
        # Question Input
        # --------------------------------
        term_label = QLabel("Term")

        #Create text box
        self.term_input = QTextEdit()
        self.term_input.setStyleSheet("""
            QTextEdit {
                background-color: white;
                color: black;
                border: 1px solid gray;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        self.term_input.setPlaceholderText(
            "Enter your flashcard term here..."
        )

        # Make the box 150 pixels tall (just a good size to where user can input good amount of text)
        self.term_input.setMinimumHeight(150)

        # Add question label to the page
        main_layout.addWidget(term_label)

        # Add the question text box below the label
        main_layout.addWidget(self.term_input)

        # --------------------------------
        # Answer Input
        # --------------------------------

        # Create a label that says "Answer"
        definition_label = QLabel("Definition")

        # Create a large text box for the answer 
        self.definition_input = QTextEdit()
        self.definition_input.setStyleSheet("""
            QTextEdit {
                background-color: white;
                color: black;
                border: 1px solid gray;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        # Add placeholder text for answer box
        self.definition_input.setPlaceholderText(
            "Enter your flashcard definition here..."
        )

        # Make answer box 150 pixels tall as well 
        self.definition_input.setMinimumHeight(150)

        # Add answer label to the page
        main_layout.addWidget(definition_label)

        # Add answer input box below the label
        main_layout.addWidget(self.definition_input)

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


        self.new_deck_button.setStyleSheet(
            sidebar_button_style
        )
        self.view_flashcards_button.setStyleSheet(
            sidebar_button_style
        )
        self.save_flashcard_button.setStyleSheet(
            sidebar_button_style
        )

        # Apply finished layout to window
        self.setLayout(main_layout)

    def connect_buttons(self):
        self.save_flashcard_button.clicked.connect(self.save_flashcard_pressed)

        self.view_flashcards_button.clicked.connect(self.view_flashcards_pressed)

        self.new_deck_button.clicked.connect(self.new_deck_button_pressed)

    def save_flashcard_pressed(self):
        term = self.term_input.toPlainText().strip()
        definition = self.definition_input.toPlainText().strip()
        deck_id = self.deck_combo.currentData()

        if deck_id == None:
            self.message_label.setText("Please create or select a deck first")
            return
        if term == "":
            self.message_label.setText("Please enter your flashcard term")
            return
        if definition == "":
            self.message_label.setText("Please enter your flashcard definition")
            return

        if self.editing_flashcard_id is None:
            success, message = save_flashcard(self.user_id, deck_id, term, definition)
        else:
            success, message = update_flashcard(self.editing_flashcard_id, deck_id, self.user_id, term, definition)
        self.message_label.setText(message)
        if success:
            self.flashcard_updated.emit()

    def reset_for_new_flashcard(self):
        self.editing_flashcard_id = None

        self.page_title.setText("Create Flashcard")
        self.save_flashcard_button.setText("Save Flashcard")

        self.term_input.clear()
        self.definition_input.clear()

        self.message_label.setText("")

        self.refresh_decks()

    def load_flashcard_for_editing(self, flashcard):
        self.editing_flashcard_id = flashcard["id"]

        self.page_title.setText("Edit Flashcard")
        self.save_flashcard_button.setText("Update Flashcard")

        self.term_input.setPlainText(flashcard["term"])
        self.definition_input.setPlainText(flashcard["definition"])

        self.message_label.setText("")

        # makes sure the deck actually gets changed if its edited over
        self.refresh_decks(deck_id=flashcard["deck_id"])

    def view_flashcards_pressed(self):
        flashcards = get_flashcards(self.user_id)
        for flashcard in flashcards:
            print(flashcard)

    def refresh_decks(self, deck_id=None):
        self.deck_combo.clear()
        decks = get_decks(self.user_id)

        if not decks:
            self.deck_combo.addItem("No decks yet", None)
            return

        for deck in decks:
            self.deck_combo.addItem(deck["deck_name"], deck["deck_id"])

        if deck_id is not None:
            index = self.deck_combo.findData(deck_id)
            if index != -1:
                self.deck_combo.setCurrentIndex(index)

    def new_deck_button_pressed(self):
        name, ok = QInputDialog.getText(
            self, "New Deck", "Deck name:"
        )

        if not ok: return

        success, message = save_deck(self.user_id, name)
        self.message_label.setText(message)

        if success:
            new_deck = get_deck(self.user_id, name)
            self.refresh_decks(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = FlashcardCreationScreen()
    window.show()

    sys.exit(app.exec())
