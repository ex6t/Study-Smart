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
        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            40,
            30,
            40,
            30
        )

        main_layout.setSpacing(15)

        # Page heading
        heading_layout = QHBoxLayout()

        self.page_title = QLabel("All Notes")

        title_font = self.page_title.font()
        title_font.setPointSize(24)
        title_font.setBold(True)

        self.page_title.setFont(title_font)

        self.new_note_button = QPushButton(
            "+ New Note"
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

        # Sorting buttons
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

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.notes_container = QWidget()

        self.notes_layout = QVBoxLayout(
            self.notes_container
        )

        self.notes_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

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
            empty_label = QLabel("Empty")

            empty_label.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            self.notes_layout.addWidget(
                empty_label
            )

            return

        for note in self.notes:
            card = NoteCardWidget(note)

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
        QMessageBox.information(
            self,
            note["title"],
            note["content"]
        )

    def edit_note(self, note):
        self.edit_note_requested.emit(note)

    def confirm_delete_note(self, note):
        answer = QMessageBox.question(
            self,
            "Delete Note",
            (
                f'Are you sure you want to '
                f'delete "{note["title"]}"?'
            ),
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        deleted = delete_note(
            note["id"],
            self.user_id
        )

        if deleted:
            self.refresh_notes()

            QMessageBox.information(
                self,
                "Note Deleted",
                "The note was deleted."
            )

        else:
            QMessageBox.warning(
                self,
                "Delete Failed",
                "The note could not be deleted."
            )
