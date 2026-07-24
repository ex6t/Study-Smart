import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from app.screens.frontpageFE import WelcomeWindow
from app.database.database import create_users_table
from app.database.notes import create_notes_table

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        button = QPushButton("hi")
        self.setFixedSize(QSize(300, 300))
        self.setCentralWidget(button)
create_users_table()
create_notes_table()
app = QApplication(sys.argv)
window = WelcomeWindow()
window.show()
app.exec()


