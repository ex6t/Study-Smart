from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QFrame,
    QSizePolicy,
)

class DashboardCardWidget(QWidget):

    CARD_WIDTH = 220
    CARD_HEIGHT = 220

    def __init__(self, title, button_text):
        super().__init__()

        self.title = title
        self.button_text = button_text

        self.setup_ui()

    def setup_ui(self):

        # Set the size of the entire widget
        #self.setFixedSize(self.CARD_WIDTH, self.CARD_HEIGHT)

        self.setMinimumSize(180, 220)
        self.setMaximumHeight(220)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Main layout (holds the card frame)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ==========================
        # Card Frame
        # ==========================

        self.card_frame = QFrame()

        self.card_frame.setStyleSheet("""
            QFrame {
                background-color: White;
                border: 2px solid rgb(215, 215, 215);
                border-radius: 12px;
            }
        """)

        main_layout.addWidget(self.card_frame)

        # Layout inside the card
        layout = QVBoxLayout(self.card_frame)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        '''
        # ==========================
        # Icon Placeholder
        # ==========================
        
        self.icon_label = QLabel("Icon")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setFixedHeight(70)

        self.icon_label.setStyleSheet("""
            QLabel {
                background-color: rgb(200, 200, 200);
                border: none;
                color: black;
                border-radius: 8px;
                font-size: 16px;
            }
        """)
        '''
        # ==========================
        # Title
        # ==========================

        self.title_label = QLabel(self.title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_label.setStyleSheet("""
            QLabel {
                background: transparent;
                border: none;
                color: black;
                font-size: 18px;
                font-weight: bold;
            }
        """)

        # ==========================
        # Statistics Area
        # ==========================

        self.statistics_frame = QFrame()
        self.statistics_frame.setMinimumHeight(80)

        self.statistics_frame.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
            }
        """)

        # ==========================
        # Action Button
        # ==========================

        self.action_button = QPushButton(self.button_text)

        self.action_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(205,220,245);
                border: 1px solid rgb(170,185,210);
                color: black;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 8px;
            }

            QPushButton:hover {
                background-color: rgb(185,205,240);
            }

            QPushButton:pressed {
                background-color: rgb(165,190,230);
            }
        """)

        # ==========================
        # Add Widgets
        # ==========================

        #layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.statistics_frame)
        layout.addStretch()
        layout.addWidget(self.action_button)
