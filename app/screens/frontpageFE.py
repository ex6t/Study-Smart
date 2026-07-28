import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout
)
from app.screens.register_screen import RegisterWindow
from app.screens.login_screen import LoginView
from app.database.database import create_users_table
 
 
class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__() #runs QMainWindow's own setup code first 
        self.setWindowTitle("Study Smart")
        self.resize(1200, 800)#starting size of the window 
 
        central = QWidget()
        central.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.setCentralWidget(central) #window's main content area 

        #stacks widgets vertically (top to bottom) inside "central"
        main_layout = QVBoxLayout(central)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)#center the text horizontally
 
        # Welcome text
        welcome_label = QLabel("Welcome to Study Smart")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        welcome_label.setStyleSheet("""
            color: #2d6cdf;
            font-weight: bold;
            font-size: 30px;
        """)
        # Buttons row
        button_row = QHBoxLayout() #stack widgets side by side (left to right)
        self.signup_button = QPushButton("Sign Up") #clickable button
        self.signup_button.clicked.connect(self.open_register)
        self.login_button = QPushButton("Log In") #clickable button
        self.login_button.clicked.connect(self.open_login)

        #button customization

        button_style="""
            QPushButton {
                background-color: rgb(205,220,245);
                color: black;
                border: 1px solid rgb(170,185,210);
                border-radius: 8px;
                font-size: 12px;
                font-weight: bold;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: rgb(185,205,240);
            }
            QPushButton:pressed {
                background-color: rgb(165,190,230);
            }
        """

        self.signup_button.setStyleSheet(button_style) #apply style to sign up 
        self.login_button.setStyleSheet(button_style) #apply style to log in 

        button_row.addWidget(self.signup_button)#place sign up button in the row 
        button_row.addWidget(self.login_button) #place log in button next to it
 
        main_layout.addWidget(welcome_label)#add the welcome text to the main vertical layout
        main_layout.addSpacing(40)
        main_layout.addLayout(button_row)#add the whole button row below the text 
 
        # Buttons don't do anything yet - functionality added later
    def open_register(self):
        self.register = RegisterWindow()
        self.register.show()
        self.close()
    def open_login(self):
        self.login = LoginView()
        self.login.show()
        self.close()
 
 
if __name__ == "__main__": #only run the code if someone is running this file directly 
    create_users_table()
    app = QApplication(sys.argv)
    window = WelcomeWindow()
    window.show()
    sys.exit(app.exec()) #keeps the program running 
