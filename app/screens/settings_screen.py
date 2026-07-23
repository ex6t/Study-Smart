import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,# Run the PyQt application
    QWidget,     # Create a basic window/widget
    QLabel,      # Display text
    QPushButton, # Create clickable buttons
    QVBoxLayout, # Place widgets vertically
)


class SettingsScreen(QWidget):
    def __init__(self):
        super().__init__()
    
        self.setWindowTitle("Study Smart - Settings")
        # Set window size to 1200 x 800 pixels
        self.setFixedSize(1200, 800)

        self.setup_ui()

    def setup_ui(self):

        # Main layout for the page
        main_layout = QVBoxLayout()

        # Add space around the edges of the window
        main_layout.setContentsMargins(40, 30, 40, 30)

        # Space between widgets
        main_layout.setSpacing(20)

        # -------------------------
        # Page Title
        # -------------------------

        # Create a text label that says "Settings"
        self.page_title = QLabel("Settings")

        # Center the title horizontally
        self.page_title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # Get the title's current font
        title_font = self.page_title.font()
        
        # Make the font size 24
        title_font.setPointSize(24)
        
        # Make the font bold
        title_font.setBold(True)

        # Apply updated font settings
        self.page_title.setFont(title_font)

        # Add title to the layout
        main_layout.addWidget(self.page_title)

        # Push the buttons toward the center of the screen
        main_layout.addStretch()

        # -------------------------
        # Buttons
        # -------------------------

        # Create the logout button
        self.logout_button = QPushButton("Logout")

        # Set the button size
        self.logout_button.setFixedSize(300, 50)

        # Create the change username/password button
        self.change_credentials_button = QPushButton(
            "Change Username/Password"
        )

        # Set the button size
        self.change_credentials_button.setFixedSize(300, 50)

        # Create the delete account button
        self.delete_account_button = QPushButton(
            "Delete Account"
        )

        # Set the button size
        self.delete_account_button.setFixedSize(300, 50)

        # Add logout button to layer and center it
        main_layout.addWidget(
            self.logout_button,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        # Add the change username/password button to layout and center it
        main_layout.addWidget(
            self.change_credentials_button,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        # Add the delete account button to layout and center it
        main_layout.addWidget(
            self.delete_account_button,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
    
        # Add invisible space below the buttons
        main_layout.addStretch()

        # Set the layout for the window
        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = SettingsScreen()
    window.show()

    sys.exit(app.exec())
