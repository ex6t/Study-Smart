from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class FlashcardCardWidget(QWidget):
    view_requested = pyqtSignal(dict)
    edit_requested = pyqtSignal(dict)
    delete_requested = pyqtSignal(dict)

    def __init__(self, flashcard):
        super().__init__()

        self.flashcard = flashcard

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(12)

        heading_layout = QHBoxLayout()

        self.term_label = QLabel(
            self.flashcard["term"]
        )

        term_font = self.term_label.font()
        term_font.setBold(True)
        term_font.setPointSize(14)

        self.term_label.setFont(term_font)
        self.term_label.setStyleSheet("""
            color: black;
            background: transparent;
            border: none;
        """)

        self.deck_label = QLabel(
            self.flashcard.get("deck_name", "")
        )

        self.deck_label.setStyleSheet("""
            color: rgb(90,90,90);
            background: transparent;
            border: none;
        """)

        term_box = QWidget()
        term_box.setStyleSheet("""
            background:white;
            border: 1px solid rgb(180,180,180);
            border-radius:8px;
            """)

        term_layout = QHBoxLayout(term_box)
        term_layout.setContentsMargins(10, 6, 10, 6)
        term_layout.addWidget(self.term_label)

        heading_layout.addWidget(term_box)

        heading_layout.addStretch()

        deck_box = QWidget()
        deck_box.setStyleSheet("""
            background:white;
            border: 1px solid rgb(180,180,180);
            border-radius:8px;
        """)

        deck_layout = QHBoxLayout(deck_box)
        deck_layout.setContentsMargins(10, 6, 10, 6)
        deck_layout.addWidget(self.deck_label)

        heading_layout.addWidget(deck_box)

        main_layout.addLayout(
            heading_layout
        )

        preview = self.flashcard["definition"].strip()

        # Keep only the first 4 actual lines
        preview_lines = preview.splitlines()[:4]
        preview = "\n".join(preview_lines)

        # Also limit very long paragraphs
        if len(preview) > 180:
            preview = preview[:180].rstrip() + "..."
        elif len(self.flashcard["definition"].splitlines()) > 4:
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
                self.flashcard
            )
        )

        self.edit_button.clicked.connect(
            lambda: self.edit_requested.emit(
                self.flashcard
            )
        )

        self.delete_button.clicked.connect(
            lambda: self.delete_requested.emit(
                self.flashcard
            )
        )

        # Leave enough room for the preview and a small gap above the buttons.
        self.setMinimumHeight(200)

        # Card styling
        self.setObjectName("FlashcardCard")

        self.setStyleSheet("""
        #FlashcardCard {
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