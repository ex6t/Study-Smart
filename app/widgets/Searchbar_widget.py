from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QSizePolicy
)


class SearchBarWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QHBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)

        self.search_bar = QLineEdit()

        self.search_bar.setPlaceholderText("Search...")

        self.search_bar.setMinimumWidth(300)
        self.search_bar.setFixedHeight(40)

        # Allow the search bar to grow if the window gets wider
        self.search_bar.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        self.search_bar.setStyleSheet("""
            QLineEdit{
                background-color:white;
                border:2px solid rgb(215,215,215);
                color: gray;
                border-radius:10px;
                padding-left:12px;
                font-size:14px;
            }

            QLineEdit:focus{
                border:2px solid rgb(165,190,230);
            }
        """)

        layout.addWidget(self.search_bar)