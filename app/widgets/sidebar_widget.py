from PyQt6.QtWidgets import (QWidget, QFrame, QVBoxLayout, QPushButton, QLabel)
from PyQt6.QtCore import Qt


class SidebarWidget(QWidget):

    SIDEBAR_WIDTH = 280
    SIDEBAR_COLOR = "rgb(165, 190, 230)"

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def create_sidebar_button(self, text):
        """Creates a sidebar button with consistent styling."""

        button = QPushButton(text)
        button.setFixedHeight(50)

        button.setStyleSheet("""
            QPushButton {
                background-color: rgb(235, 242, 252);
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: rgb(240, 240, 240);
            }

            QPushButton:pressed {
                background-color: rgb(220, 220, 220);
            }
        """)

        return button

    def setup_ui(self):

        # Make the widget itself transparent
        self.setStyleSheet("background-color: transparent;")

        # Main Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Sidebar Frame
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(self.SIDEBAR_WIDTH)

        self.sidebar.setStyleSheet(
            f"background-color: {self.SIDEBAR_COLOR};"
        )

        # Sidebar Layout
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(15)

        # Title
        self.title = QLabel("Study Smart")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            background: transparent;
            border: none;
        """)

        sidebar_layout.addWidget(self.title)

        # Space before Dashboard button
        sidebar_layout.addSpacing(50)

        # Dashboard Button
        self.dashboard_button = self.create_sidebar_button("Dashboard")
        sidebar_layout.addWidget(self.dashboard_button)

        sidebar_layout.addSpacing(25)

        self.notes_button = self.create_sidebar_button("Notes")
        sidebar_layout.addWidget(self.notes_button)

        sidebar_layout.addSpacing(25)

        self.flashcards_button = self.create_sidebar_button("Flashcards")
        sidebar_layout.addWidget(self.flashcards_button)

        sidebar_layout.addSpacing(25)

        self.quizzes_button = self.create_sidebar_button("Quizzes")
        sidebar_layout.addWidget(self.quizzes_button)

        # Push Settings button to bottom
        sidebar_layout.addStretch()

        # Settings Button
        self.settings_button = self.create_sidebar_button("Settings")
        sidebar_layout.addWidget(self.settings_button)

        # Add sidebar to widget
        layout.addWidget(self.sidebar)
