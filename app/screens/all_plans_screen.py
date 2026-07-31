from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
)

from app.database.planner_database import (load_plans, clear_all_plans)
from app.widgets.planner_widget import PlannerCardWidget
from PyQt6.QtWidgets import QMessageBox



class AllPlansScreen(QWidget):

    new_plan_requested = pyqtSignal()
    edit_plan_requested = pyqtSignal(dict)
    delete_plan_requested = pyqtSignal(dict)
    completed_changed = pyqtSignal(dict, bool)

    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id

        self.setup_ui()

        # Eventually this will load plans
        self.refresh_plans()

    def setup_ui(self):

        # ------------------------------------
        # Page Styling
        # ------------------------------------

        self.setStyleSheet("""
            QWidget {
                background-color: rgb(240,240,240);
                color: black;
            }

            QLabel {
                color: black;
            }

            QScrollArea {
                border: none;
                background: rgb(240,240,240);
            }

            QScrollArea > QWidget > QWidget {
                background: rgb(240,240,240);
            }
        """)

        button_style = """
            QPushButton {
                background-color: rgb(205,220,245);
                color: black;
                border: 1px solid rgb(170,185,210);
                border-radius: 8px;
                padding: 6px 14px;
                font-size: 12px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: rgb(185,205,240);
            }

            QPushButton:pressed {
                background-color: rgb(165,190,230);
            }
        """

        # ------------------------------------
        # Main Layout
        # ------------------------------------

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            40,
            30,
            40,
            30
        )

        main_layout.setSpacing(15)

        # ------------------------------------
        # Header
        # ------------------------------------

        heading_layout = QHBoxLayout()

        self.page_title = QLabel("Study Planner")

        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)

        self.page_title.setFont(title_font)

        self.new_plan_button = QPushButton("+ New Plan")

        self.new_plan_button.setStyleSheet(button_style)

        heading_layout.addWidget(self.page_title)
        heading_layout.addStretch()
        heading_layout.addWidget(self.new_plan_button)

        main_layout.addLayout(heading_layout)

        # ------------------------------------
        # Top Buttons
        # ------------------------------------

        top_button_layout = QHBoxLayout()

        self.clear_all_button = QPushButton("Clear All")

        self.clear_all_button.setStyleSheet(button_style)

        top_button_layout.addWidget(self.clear_all_button)
        top_button_layout.addStretch()

        main_layout.addLayout(top_button_layout)

        # ------------------------------------
        # Scroll Area
        # ------------------------------------

        self.scroll_area = QScrollArea()

        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget()

        self.scroll_layout = QVBoxLayout(self.scroll_widget)

        self.scroll_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        self.scroll_layout.setSpacing(15)

        self.scroll_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.scroll_area.setWidget(self.scroll_widget)

        main_layout.addWidget(self.scroll_area)

        # ------------------------------------
        # Connections
        # ------------------------------------

        self.new_plan_button.clicked.connect(self.new_plan_requested.emit)
        self.clear_all_button.clicked.connect(self.confirm_clear_plans)
    # --------------------------------------------------
    # Refresh Planner List
    # --------------------------------------------------

    def refresh_plans(self):

        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        plans = load_plans(self.user_id)

        if not plans:

            empty = QLabel(
                "No study plans yet.\n\nClick '+ New Plan' to create one."
            )

            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)

            empty.setStyleSheet("""
                font-size:16px;
                color:rgb(120,120,120);
                padding:80px;
            """)

            self.scroll_layout.addWidget(empty)

            return
        self.plan_cards = []
        for plan in plans:

            card = PlannerCardWidget(plan)
            self.plan_cards.append(card)
            card.edit_requested.connect(self.edit_plan_requested.emit)
            card.delete_requested.connect(self.delete_plan_requested.emit)
            card.completed_changed.connect(self.completed_changed.emit)
            self.scroll_layout.addWidget(card)
        self.scroll_layout.addStretch()


    def clear_all_plans(self):

        success, message = clear_all_plans(self.user_id)

        if success:
            self.refresh_plans()

    def confirm_clear_plans(self):

        msg = QMessageBox(self)
        msg.setWindowTitle("Clear All Plans")
        msg.setText(
            "Are you sure you want to clear all plans?"
        )

        yes_button = msg.addButton(
            QMessageBox.StandardButton.Yes
        )

        msg.addButton(
            QMessageBox.StandardButton.No
        )

        msg.setStyleSheet("""
            QWidget {
                background-color: white;
            }

            QLabel {
                color: black;
                background: white;
            }

            QPushButton {
                background-color: rgb(205,220,245);
                color: black;
                border: 1px solid rgb(170,185,210);
                border-radius: 8px;
                padding: 6px 14px;
                font-size: 12px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: rgb(185,205,240);
            }

            QPushButton:pressed {
                background-color: rgb(165,190,230);
            }
        """)

        msg.exec()

        if msg.clickedButton() == yes_button:
            self.clear_all_plans()

    def scroll_to_plan(self, plan_id):
        for card in self.plan_cards:
            if card.plan["id"] == plan_id:
                self.scroll_area.ensureWidgetVisible(card)
                break
