import sys

from PyQt6.QtWidgets import (
    QApplication, #main application window
    QLabel, #text labels
    QLineEdit, #input boxes
    QPushButton,#push buttons
    QVBoxLayout, #vertical form
    QWidget, #place widgets within the vertical form
    QHBoxLayout,
)
from PyQt6.QtGui import QFont #used for font control
from PyQt6.QtCore import Qt, QTimer#used for center alignment flag
from app.database.database import (
    register_user,
    username_exists,
    create_users_table,
)



class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Study Smart - Register")
        self.setFixedSize(1200, 800)

        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: rgb(240, 240, 240);
                color: black;
            }
        """)
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
        username_label = QLabel("Username(max 16 characters)")
        self.username_input = QLineEdit()
        self.username_input.setMaxLength(16)
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                border: 1px solid gray;
                border-radius: 5px;
                padding: 5px;
            }
        """)

                #Password Input Box - Will show up hidden as user types
        password_label = QLabel("Password(max 20 characters)")
        self.password_input = QLineEdit()
        self.password_input.setMaxLength(20)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                border: 1px solid gray;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        #Confirm Password - Will show up hidden as user types
        confirm_label = QLabel("Confirm Password")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setMaxLength(20)
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                border: 1px solid gray;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        #Register Button - no action yet
        self.register_button = QPushButton("Sign Up")
        self.register_button.clicked.connect(self.register_check)
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(205,220,245);
                color: black;
                border: 1px solid rgb(170,185,210);
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: rgb(185,205,240);
                color: black;
            }

            QPushButton:pressed {
                background-color: rgb(165,190,230);
                color: black;
            }
        """)

        #Already have an account button
        self.login_button = QPushButton("Already have an account? Log In")
        self.login_button.clicked.connect(self.open_login)
        

        #Error / Success Message - use for later
        self.message_label = QLabel("")

        #----Add everything to Vertical layout widget------

        #create header space and ever spacing
        layout.addStretch()

        layout.addWidget(title)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)

        layout.addWidget(password_label)
        layout.addWidget(self.password_input)

        layout.addWidget(confirm_label)
        layout.addWidget(self.confirm_password_input)

        layout.addWidget(self.register_button)

        #makes sure the text for already have account button is sized correctly
        login_button_layout = QHBoxLayout()
        login_button_layout.addStretch()
        login_button_layout.addWidget(self.login_button)
        login_button_layout.addStretch()

        layout.addLayout(login_button_layout)

        layout.addWidget(self.message_label)

        self.login_button.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            color: rgb(70, 165, 250);
            border: none;
            font-size: 14px;
            font-weight: bold;
            text-align: center;
        }

        QPushButton:hover {
            color: rgb(90, 130, 200);                            
            text-decoration: underline;
        }

        QPushButton:pressed {
            color: rgb(90, 130, 200);
        }
    """)
        self.login_button.adjustSize()
        self.login_button.setFixedWidth(self.login_button.width() + 20)
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
    #redirects user to login window if username and password created successfully
        if success:
            self.message_label.setStyleSheet("""
            color: black;
            font-size: 14px;
            font-weight: bold;
        """)
            self.message_label.setText("Account created successfully!")
            self.register_button.setEnabled(False)
            QTimer.singleShot(2000, self.open_login)

#takes user to login window
    def open_login(self):
        from app.screens.login_screen import LoginView
        self.login_window = LoginView()
        self.login_window.show()
        self.close()

if __name__ == "__main__":
    create_users_table()   # Create the users table if it doesn't exist

    app = QApplication(sys.argv)

    window = RegisterWindow()
    window.show()

    sys.exit(app.exec())