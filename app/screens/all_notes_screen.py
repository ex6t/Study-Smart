from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.database.notes import (
    delete_note,
    get_notes,
)

from app.widgets.note_card_widget import (
    NoteCardWidget,
)


class AllNotesScreen(QWidget):
    new_note_requested = pyqtSignal()
    edit_note_requested = pyqtSignal(dict)

    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id
        self.notes = []

        self.setup_ui()
        self.connect_buttons()
        self.refresh_notes()

    def setup_ui(self):

        # ----------- Page Styling -----------
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

        sidebar_button_style = """
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

        main_layout = QVBoxLayout(self)
        
        main_layout.setContentsMargins(
            40,
            30,
            40,
            30
        )

        main_layout.setSpacing(15)

        # --------------------------
        # Page Heading
        # --------------------------

        heading_layout = QHBoxLayout()

        self.page_title = QLabel("All Notes")

        title_font = self.page_title.font()
        title_font.setPointSize(24)
        title_font.setBold(True)

        self.page_title.setFont(title_font)

        self.new_note_button = QPushButton(
            "+ New Note"
        )

        self.new_note_button.setStyleSheet(
            sidebar_button_style
        )

        heading_layout.addWidget(
            self.page_title
        )

        heading_layout.addStretch()

        heading_layout.addWidget(
            self.new_note_button
        )

        main_layout.addLayout(
            heading_layout
        )

        # --------------------------
        # Sort Buttons
        # --------------------------

        sort_layout = QHBoxLayout()

        sort_label = QLabel("Sort by:")

        self.sort_title_button = QPushButton(
            "Title"
        )

        self.sort_newest_button = QPushButton(
            "Newest"
        )

        self.sort_oldest_button = QPushButton(
            "Oldest"
        )

        self.sort_title_button.setStyleSheet(
            sidebar_button_style
        )

        self.sort_newest_button.setStyleSheet(
            sidebar_button_style
        )

        self.sort_oldest_button.setStyleSheet(
            sidebar_button_style
        )

        sort_layout.addWidget(sort_label)
        sort_layout.addWidget(
            self.sort_title_button
        )

        sort_layout.addWidget(
            self.sort_newest_button
        )

        sort_layout.addWidget(
            self.sort_oldest_button
        )

        sort_layout.addStretch()

        main_layout.addLayout(
            sort_layout
        )

        # --------------------------
        # Scroll Area
        # --------------------------

        self.scroll_area = QScrollArea()
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background: rgb(240,240,240);
                border: none;
            }

            QWidget {
                background: rgb(240,240,240);
            }
        """)
        self.scroll_area.setWidgetResizable(True)

        self.notes_container = QWidget()
        self.notes_container.setStyleSheet("""
            background-color: rgb(240,240,240);
        """)
        self.scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)

        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background: rgb(240,240,240);
                border: none;
            }

            QScrollArea > QWidget > QWidget {
                background: rgb(240,240,240);
            }
        """)

        self.notes_layout = QVBoxLayout(
            self.notes_container
        )

        self.notes_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        self.notes_layout.setSpacing(18)

        self.scroll_area.setWidget(
            self.notes_container
        )

        main_layout.addWidget(
            self.scroll_area,
            1
        )
    def connect_buttons(self):
        self.new_note_button.clicked.connect(
            self.new_note_requested.emit
        )

        self.sort_title_button.clicked.connect(
            self.sort_by_title
        )

        self.sort_newest_button.clicked.connect(
            self.sort_by_newest
        )

        self.sort_oldest_button.clicked.connect(
            self.sort_by_oldest
        )

    def refresh_notes(self):
        self.notes = get_notes(self.user_id)
        self.display_notes()

    def display_notes(self):
        self.clear_notes_layout()

        if len(self.notes) == 0:
            empty_label = QLabel("No notes found.")

            empty_label.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            empty_label.setStyleSheet("""
                font-size: 16px;
                color: black;
                background-color: rgb(240,240,240);
            """)

            self.notes_layout.addWidget(
                empty_label
            )

            return
        
        
        self.note_cards = []
        for note in self.notes:
            card = NoteCardWidget(note)
            self.note_cards.append(card)
            card.view_requested.connect(
                self.view_note
            )

            card.edit_requested.connect(
                self.edit_note
            )

            card.delete_requested.connect(
                self.confirm_delete_note
            )

            self.notes_layout.addWidget(card)

    def clear_notes_layout(self):
        while self.notes_layout.count():
            item = self.notes_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def sort_by_title(self):
        self.notes.sort(
            key=lambda note: (
                note["title"].lower()
            )
        )

        self.display_notes()

    def sort_by_newest(self):
        self.notes.sort(
            key=lambda note: note.get(
                "updated_at",
                ""
            ),
            reverse=True
        )

        self.display_notes()

    def sort_by_oldest(self):
        self.notes.sort(
            key=lambda note: note.get(
                "updated_at",
                ""
            )
        )

        self.display_notes()

    def view_note(self, note):
        msg = QMessageBox(self)
        msg.setWindowTitle(note["title"])
        msg.setText(note["content"])

        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }

            QLabel {
                color: black;
                background: transparent;
                font-size: 14px;
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

    def edit_note(self, note):
        self.edit_note_requested.emit(note)

    def confirm_delete_note(self, note):
        msg = QMessageBox(self)
        msg.setWindowTitle("Delete Note")
        msg.setText(
            f'Are you sure you want to delete "{note["title"]}"?'
        )

        msg.setIcon(QMessageBox.Icon.Question)

        yes_button = msg.addButton(
            QMessageBox.StandardButton.Yes
        )
        no_button = msg.addButton(
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

        if msg.clickedButton() != yes_button:
            return

        deleted = delete_note(
            note["id"],
            self.user_id
        )

        if deleted:
            self.refresh_notes()

            self.styled_message(
                "Note Deleted",
                "The note was deleted.",
                "info"
            )

        else:
            self.styled_message(
                "Delete Failed",
                "The note could not be deleted.",
                "warning"   
            )
    def styled_message(self, title, text, icon="info"):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)

        if icon == "info":
            msg.setIcon(QMessageBox.Icon.Information)
        elif icon == "warning":
            msg.setIcon(QMessageBox.Icon.Warning)
        elif icon == "critical":
            msg.setIcon(QMessageBox.Icon.Critical)

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

    def scroll_to_note(self, note_id):
        for card in self.note_cards:
            if card.note["id"] == note_id:
                self.scroll_area.ensureWidgetVisible(card)
                break