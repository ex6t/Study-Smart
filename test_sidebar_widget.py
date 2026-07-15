import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QFrame, QHBoxLayout

from app.widgets.sidebar_widget import SidebarWidget


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("Sidebar Test")
    window.resize(1200, 800)

    container = QFrame()
    layout = QHBoxLayout(container)

    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    sidebar = SidebarWidget()

    content = QFrame()
    content.setStyleSheet("background-color: white;")

    layout.addWidget(sidebar)
    layout.addWidget(content)

    window.setCentralWidget(container)

    window.show()

    sys.exit(app.exec())