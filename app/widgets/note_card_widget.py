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

        heading_layout = QHBoxLayout()

        self.title_label = QLabel(
            self.note["title"]
        )

        title_font = self.title_label.font()
        title_font.setBold(True)
        title_font.setPointSize(14)

        self.title_label.setFont(title_font)

        self.date_label = QLabel(
            self.format_date()
        )

        heading_layout.addWidget(
            self.title_label
        )

        heading_layout.addStretch()

        heading_layout.addWidget(
            self.date_label
        )

        main_layout.addLayout(
            heading_layout
        )

        preview = self.note["content"]

        if len(preview) > 120:
            preview = preview[:120] + "..."

        self.preview_label = QLabel(preview)
        self.preview_label.setWordWrap(True)

        main_layout.addWidget(
            self.preview_label
        )

        button_layout = QHBoxLayout()

        button_layout.addStretch()

        self.view_button = QPushButton("View")
        self.edit_button = QPushButton("Edit")
        self.delete_button = QPushButton("Delete")

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

        # Minimal styling just to separate each card.
        self.setStyleSheet(
            """
            NoteCardWidget {
                border: 1px solid lightgray;
            }
            """
        )

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
