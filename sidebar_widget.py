from PyQt6.QtWidgets import QWidget, QFrame, QVBoxLayout


class SidebarWidget(QWidget):

    SIDEBAR_WIDTH = 280
    SIDEBAR_COLOR = "rgb(165, 190, 230)"

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):

        # Make the widget itself transparent
        self.setStyleSheet("background-color: transparent;")

        layout = QVBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sidebar = QFrame()

        self.sidebar.setFixedWidth(self.SIDEBAR_WIDTH)

        self.sidebar.setStyleSheet(
            f"background-color: {self.SIDEBAR_COLOR};"
        )

        layout.addWidget(self.sidebar)