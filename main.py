import sys
import traceback
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

from app.database.flashcards import create_flashcard_table, create_decks_table
from app.screens.frontpageFE import WelcomeWindow
from app.database.database import create_users_table
from app.database.notes import create_notes_table
from app.database.planner_database import create_planner_table

#traceback exception handling
def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Uncaught exception:\n", tb)

sys.excepthook = excepthook
#init main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        button = QPushButton("hi")
        self.setFixedSize(QSize(300, 300))
        self.setCentralWidget(button)
#database table functions
create_users_table()
create_notes_table()
create_flashcard_table()
create_decks_table()
create_planner_table()
#main window starter
app = QApplication(sys.argv)
window = WelcomeWindow()
window.show()
app.exec()


