import sys
import traceback
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

from app.database.flashcards import create_flashcard_table
from app.screens.frontpageFE import WelcomeWindow
from app.database.database import create_users_table
from app.database.notes import create_notes_table

def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Uncaught exception:\n", tb)

sys.excepthook = excepthook

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        button = QPushButton("hi")
        self.setFixedSize(QSize(300, 300))
        self.setCentralWidget(button)
create_users_table()
create_notes_table()
create_flashcard_table()
app = QApplication(sys.argv)
window = WelcomeWindow()
window.show()
app.exec()


