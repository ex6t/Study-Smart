import sys

from PyQt6.QtWidgets import (
    QApplication, #main application window
    QLabel, #text labels
    QLineEdit, #input boxes
    QPushButton,#push buttons
    QVBoxLayout, #vertical form
    QWidget, #place widgets within the vertical form
)
from PyQt6.QtGui import QFont #used for font control
from PyQt6.QtCore import Qt #used for center alignment flag
from app.database.database import (register_user, username_exists)

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Study Smart - Register")
        self.setFixedSize(1200, 800)

        self.setup_ui()

    def setup_ui(self):
        #Empty Vertical Layout - Login form will be a vertical layout
        layout = QVBoxLayout()

        #Center everything
        layout.setSpacing(15)
        layout.setContentsMargins(400, 150, 400, 150)

        #Register Title - Create Account Centered and Large
        title = QLabel("Create Account")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #Username label
        username_label = QLabel("Username")
        self.username_input = QLineEdit()
        self.username_input.setMaxLength(16)

                #Password Input Box - Will show up hidden as user types
        password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setMaxLength(20)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        

        #Confirm Password - Will show up hidden as user types
        confirm_label = QLabel("Confirm Password")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setMaxLength(20)
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        #Register Button - no action yet
        self.register_button = QPushButton("Sign Up")
        self.register_button.clicked.connect(self.register_check)

        #Error / Success Message - use for later
        self.message_label = QLabel("")

        #----Add everything to Vertical layout widget------

        #create header space and ever spacingh
        layout.addStretch()

        layout.addWidget(title)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)

        layout.addWidget(password_label)
        layout.addWidget(self.password_input)

        layout.addWidget(confirm_label)
        layout.addWidget(self.confirm_password_input)

        layout.addWidget(self.register_button)
        layout.addWidget(self.message_label)

        #create footer space and even spacing
        layout.addStretch()

        self.setLayout(layout)

    def register_check(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if username == "":
            self.message_label.setText(
                "Please enter a username."
            )
            return
        if len(username) < 3:
            self.message_label.setText(
                "Username must be 3 or more characters."
            )
            return

        if password == "":
            self.message_label.setText(
                "Please enter a password."
            )
            return
        if len(password) < 8:
            self.message_label.setText(
                "Password must be at least 8 characters."
            )
            return

        if password != confirm_password:
            self.message_label.setText(
                "Passwords do not match."
            )
            return
        if username_exists(username):
            self.message_label.setText(
                "This username already exists."
            )
            return
        
        #save user in database
        success, message = register_user(
            username,
            password,
        )

        self.message_label.setText(message)

        if success:
            self.username_input.clear()
            self.password_input.clear()
            self.confirm_password_input.clear()

    
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = RegisterView()
    window.show()

    sys.exit(app.exec())
