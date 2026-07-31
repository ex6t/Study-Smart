from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QCheckBox,
)
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox

class PlannerCardWidget(QWidget):

    edit_requested = pyqtSignal(dict)
    delete_requested = pyqtSignal(dict)
    completed_changed = pyqtSignal(dict, bool)

    def __init__(self, plan):
        super().__init__()

        self.plan = plan
        self.expanded = False

        self.setup_ui()

    def setup_ui(self):

        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 10px;
            }

            QLabel {
                color: black;
                background: transparent;
            }

            QPushButton {
                background-color: rgb(205,220,245);
                color: black;
                border: 1px solid rgb(170,185,210);
                border-radius: 8px;
                padding: 5px 12px;
                font-size: 12px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: rgb(185,205,240);
            }

            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }

            QCheckBox::indicator:unchecked {
                image: url(app/widgets/unchecked_box.png);
            }

            QCheckBox::indicator:checked {
                image: url(app/widgets/checked_box.png);
            }
        """)

        self.setMinimumHeight(120)


        # -----------------------------
        # Main Layout
        # -----------------------------

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            15,
            12,
            15,
            12
        )

        main_layout.setSpacing(10)


        # -----------------------------
        # Header
        # -----------------------------

        header_layout = QHBoxLayout()


        # Expand button

        self.expand_button = QPushButton("▲")

        self.expand_button.clicked.connect(
            self.toggle_expand
        )


        # Title

        self.title_label = QLabel(
            self.plan["title"]
        )

        title_font = QFont()

        title_font.setPointSize(16)
        title_font.setBold(True)

        self.title_label.setFont(
            title_font
        )


        # Date

        self.date_label = QLabel(self.format_date())
        self.date_label.setStyleSheet("""
            color: rgb(90,90,90);
            background: transparent;
            border: none;
        """)

        date_box = QWidget()
        date_box.setStyleSheet("""
            background:white;
            border: 1px solid rgb(180,180,180);
            border-radius:8px;
        """)

        date_layout = QHBoxLayout(date_box)
        date_layout.setContentsMargins(10, 6, 10, 6)
        date_layout.addWidget(self.date_label)

        header_layout.addWidget(self.expand_button)

        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(date_box)


        main_layout.addLayout(
            header_layout
        )


        # -----------------------------
        # Content
        # -----------------------------
        self.content_label = QLabel(self.plan["content"])

        self.content_label.setWordWrap(True)

        self.content_label.setMaximumHeight(self.content_label.fontMetrics().height() + 24)

        self.content_label.setStyleSheet("""
            QLabel {
                background-color: rgb(250,250,250);
                border: 1px solid rgb(220,220,220);
                border-radius: 8px;
                padding: 12px;
                color: black;
            }
        """)

        main_layout.addWidget(self.content_label)
        # -----------------------------
        # Bottom Controls
        # -----------------------------

        bottom_layout = QHBoxLayout()


        self.completed_box = QCheckBox("Mark Complete")
        self.completed_box.setStyleSheet("""background:rgb(240,240,240);""")
        self.completed_box.setChecked(
            bool(self.plan["completed"])
        )
        
        self.completed_box.stateChanged.connect(
            self.completed_changed_event
        )


        bottom_layout.addWidget(
            self.completed_box
        )

        bottom_layout.addStretch()


        self.edit_button = QPushButton(
            "Edit"
        )

        self.delete_button = QPushButton(
            "Delete"
        )


        self.edit_button.clicked.connect(
            self.edit_clicked
        )

        self.delete_button.clicked.connect(
            self.confirm_delete_plan
        )


        bottom_layout.addWidget(
            self.edit_button
        )

        bottom_layout.addWidget(
            self.delete_button
        )


        main_layout.addLayout(
            bottom_layout
        )


    # -----------------------------
    # Expand / Collapse
    # -----------------------------

    def toggle_expand(self):

        self.expanded = not self.expanded

        if self.expanded:

            self.content_label.setMaximumHeight(16777215)

            self.expand_button.setText("▼")

        else:

            self.content_label.setMaximumHeight(self.content_label.fontMetrics().height() + 24)

            self.expand_button.setText("▲")

        self.adjustSize()


    # -----------------------------
    # Button Actions
    # -----------------------------

    def edit_clicked(self):

        self.edit_requested.emit(
            self.plan
        )


    def delete_clicked(self):

        self.delete_requested.emit(self.plan)


    def completed_changed_event(self):

        completed = self.completed_box.isChecked()

        self.completed_changed.emit(
            self.plan,
            completed
        )

    def format_date(self):
            date_value = self.plan.get(
                "created_at",
                ""
            )
    
            if date_value == "":
                return "No date"
    
            try:
                date = datetime.strptime(
                    date_value,
                    "%Y-%m-%d %H:%M:%S"
                )
    
                return date.strftime(
                    "%m/%d/%Y"
                )
    
            except ValueError:
                return str(date_value)

    def confirm_delete_plan(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Delete Plan")
        msg.setText(
            f'Are you sure you want to delete "{self.plan["title"]}"?'
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
            self.delete_requested.emit(self.plan)