import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QTextEdit,
    QPushButton,
    QVBoxLayout,  # Creates vertical layout
    QHBoxLayout,  # Creates a horizontal layout
    QWidget,
)

from app.database.flashcards import (
    get_flashcards
)


class FlashcardStudyScreen(QWidget):
    def __init__(self, user_id):
        super().__init__()

        self.setWindowTitle("Study Smart - Flashcards")

        self.user_id = user_id

        self.setFixedSize(1200, 800)

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
        main_layout.setContentsMargins(40, 30, 40, 30)  # (left, top, right, bottom)

        # Space between widgets.
        main_layout.setSpacing(15)

        # --------------------------------
        # Page Title
        # --------------------------------
        self.page_title = QLabel("Studying...")

        # Center the title
        self.page_title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # Get the current font used and change size/make text bold
        title_font = self.page_title.font()
        title_font.setPointSize(24)
        title_font.setBold(True)

        # apply font changes
        self.page_title.setFont(title_font)

        # Place title inside vertical layout
        main_layout.addWidget(self.page_title)

    def connect_buttons(self):
        pass