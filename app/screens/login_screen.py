import sys

from PyQt6.QtWidgets import (
    QApplication,  # main application window
    QLabel,  # text labels
    QLineEdit,  # input boxes
    QPushButton,  # push buttons
    QVBoxLayout,  # vertical form
    QWidget,  # place widgets within the vertical form
)
from PyQt6.QtGui import QFont  # used for font control
from PyQt6.QtCore import Qt  # used for center alignment flag

# sorry josh i bummed all the code off you

class LoginView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Study Smart - Login")
        self.setFixedSize(1200, 800)

        self.setup_ui()

    def setup_ui(self):
        # Empty Vertical Layout - Login form will be a vertical layout
        layout = QVBoxLayout()

        # Center everything
        layout.setSpacing(15)
        layout.setContentsMargins(400, 150, 400, 150)

        # Login Title - Create Account Centered and Large
        title = QLabel("Login")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Username label
        username_label = QLabel("Username")
        self.username_input = QLineEdit()

        # Password Input Box - Will show up hidden as user types
        # removed max length checks, feels redundant otherwise
        password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # login button
        self.login_button = QPushButton("Login")

        # Error / Success Message - use for later
        self.message_label = QLabel("")

        # if we have extra time.
        # not sure how we would do this without an actual web service, but seems almost mandatory
        # self.forgot_password_button = QPushButton("Forgot password?")

        # will redirect to register_screen later.
        # linking these two screens should probably be one user story, tbh
        self.register_button = QPushButton("Sign Up")
        self.register_button.setFixedSize(150, 30)

        # ----Add everything to Vertical layout widget------

        # create header space and ever spacingh
        layout.addStretch()

        layout.addWidget(title)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)

        layout.addWidget(password_label)
        layout.addWidget(self.password_input)

        # layout.addWidget(self.forgot_password_button)

        layout.addWidget(self.login_button)
        layout.addWidget(self.message_label)

        layout.addWidget(self.register_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # create footer space and even spacing
        layout.addStretch()



        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = LoginView()
    window.show()

    sys.exit(app.exec())
