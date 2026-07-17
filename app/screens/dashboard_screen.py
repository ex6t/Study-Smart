from PyQt6.QtWidgets import QWidget, QFrame, QHBoxLayout
from app.widgets.sidebar_widget import SidebarWidget


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Study Smart - Dashboard")
        self.resize(1200, 800)
        self.setup_ui()


    def setup_ui(self):

        main_layout = QHBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = SidebarWidget()

        self.content_frame = QFrame()
        self.content_frame.setStyleSheet(
            "background-color: white;"
        )

        main_layout.addWidget(self.sidebar, 0)
        main_layout.addWidget(self.content_frame, 1)
# THIS MUST BE ALL THE WAY LEFT (not indented)
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("Study Smart")
    window.resize(1200, 800)

    dashboard = Dashboard()
    window.setCentralWidget(dashboard)

    window.show()

    sys.exit(app.exec())