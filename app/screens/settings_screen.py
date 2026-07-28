import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from app.database.session import end_session


class SettingsScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Study Smart - Settings")
        self.setFixedSize(1200, 800)

        self.setup_ui()

    def setup_ui(self):

        # -------------------------
        # Styling
        # -------------------------
        self.setStyleSheet("""
            QWidget {
                background-color: rgb(240, 240, 240);
                color: black;
            }

            QLabel {
                color: black;
            }

            QPushButton {
                background-color: rgb(205,220,245);
                color: black;
                border: 1px solid rgb(170,185,210);
                border-radius: 8px;
                padding: 8px;
                font-size: 12px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: rgb(185,205,240);
            }

            QPushButton:pressed {
                background-color: rgb(165,190,230);
            }
        """)

        # Main layout for the page
        main_layout = QVBoxLayout()

        # Add space around the edges of the window
        main_layout.setContentsMargins(40, 30, 40, 30)

        # Space between widgets
        main_layout.setSpacing(20)

        # -------------------------
        # Page Title
        # -------------------------

        heading_layout = QHBoxLayout()

        self.page_title = QLabel("Settings")

        title_font = self.page_title.font()
        title_font.setPointSize(24)
        title_font.setBold(True)
        self.page_title.setFont(title_font)

        heading_layout.addWidget(self.page_title)
        heading_layout.addStretch()

        main_layout.addLayout(heading_layout)
        # Push the buttons toward the center of the screen
        main_layout.addStretch()
        # -------------------------
        # Buttons
        # -------------------------

        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout_user)
        self.logout_button.setFixedSize(300, 50)

        self.change_credentials_button = QPushButton(
            "Change Username/Password"
        )
        self.change_credentials_button.setFixedSize(300, 50)

        self.delete_account_button = QPushButton(
            "Delete Account"
        )
        self.delete_account_button.setFixedSize(300, 50)

        main_layout.addWidget(
            self.logout_button,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        main_layout.addWidget(
            self.change_credentials_button,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        main_layout.addWidget(
            self.delete_account_button,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        main_layout.addStretch()

        self.setLayout(main_layout)

    def logout_user(self):
        end_session(self.window())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = SettingsScreen()
    window.show()

    sys.exit(app.exec())
