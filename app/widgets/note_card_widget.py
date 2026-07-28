from datetime import datetime

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class NoteCardWidget(QWidget):
    view_requested = pyqtSignal(dict)
    edit_requested = pyqtSignal(dict)
    delete_requested = pyqtSignal(dict)

    def __init__(self, note):
        super().__init__()

        self.note = note

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(12)

        heading_layout = QHBoxLayout()

        self.title_label = QLabel(
            self.note["title"]
        )

        title_font = self.title_label.font()
        title_font.setBold(True)
        title_font.setPointSize(14)

        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("""
            color: black;
            background: transparent;
            border: none;
        """)

        self.date_label = QLabel(
            self.format_date()
        )

        self.date_label.setStyleSheet("""
            color: rgb(90,90,90);
            background: transparent;
            border: none;
        """)

        title_box = QWidget()
        title_box.setStyleSheet("""
            background:white;
            border: 1px solid rgb(180,180,180);
            border-radius:8px;
            """)

        title_layout = QHBoxLayout(title_box)
        title_layout.setContentsMargins(10,6,10,6)
        title_layout.addWidget(self.title_label)

        heading_layout.addWidget(title_box)

        heading_layout.addStretch()

        date_box = QWidget()
        date_box.setStyleSheet("""
        background:white;
        border: 1px solid rgb(180,180,180);
        border-radius:8px;
        """)

        date_layout = QHBoxLayout(date_box)
        date_layout.setContentsMargins(10,6,10,6)
        date_layout.addWidget(self.date_label)

        heading_layout.addWidget(date_box)

        main_layout.addLayout(
            heading_layout
        )

        preview = self.note["content"].strip()

        # Keep only the first 4 actual lines
        preview_lines = preview.splitlines()[:4]
        preview = "\n".join(preview_lines)

        # Also limit very long paragraphs
        if len(preview) > 180:
            preview = preview[:180].rstrip() + "..."
        elif len(self.note["content"].splitlines()) > 4:
            preview += "\n..."

        self.preview_label = QLabel(preview)
        self.preview_label.setWordWrap(True)

        # Prevent the preview from making the card taller
        self.preview_label.setFixedHeight(80)
        self.preview_label.setStyleSheet("""
            color: rgb(40,40,40);
            background: white;
            border: 1px solid rgb(180,180,180);
            border-radius: 8px;
            padding: 10px;
        """)
        main_layout.addWidget(
            self.preview_label
        )

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 4, 0, 0)

        button_layout.addStretch()

        self.view_button = QPushButton("View")
        self.edit_button = QPushButton("Edit")
        self.delete_button = QPushButton("Delete")

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

        self.view_button.setStyleSheet(button_style)
        self.edit_button.setStyleSheet(button_style)
        self.delete_button.setStyleSheet(button_style)

        button_layout.addWidget(
            self.view_button
        )

        button_layout.addWidget(
            self.edit_button
        )

        button_layout.addWidget(
            self.delete_button
        )

        main_layout.addLayout(
            button_layout
        )

        self.view_button.clicked.connect(
            lambda: self.view_requested.emit(
                self.note
            )
        )

        self.edit_button.clicked.connect(
            lambda: self.edit_requested.emit(
                self.note
            )
        )

        self.delete_button.clicked.connect(
            lambda: self.delete_requested.emit(
                self.note
            )
        )
        # Leave enough room for the preview and a small gap above the buttons.
        self.setMinimumHeight(200)

        # Card styling
        self.setObjectName("NoteCard")

        self.setStyleSheet("""
        #NoteCard {
            background-color: white;
            border: 1px solid rgb(190,190,190);
            border-radius: 12px;
        }

        QLabel {
            color: black;
            background: transparent;
            border: none;
        }
        """)

    def format_date(self):
        date_value = self.note.get(
            "updated_at",
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
