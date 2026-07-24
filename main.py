# This is a sample Python script.

# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
import traceback
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from app.screens.frontpageFE import WelcomeWindow
from app.database.database import create_users_table

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
app = QApplication(sys.argv)
window = WelcomeWindow()
window.show()
app.exec()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
