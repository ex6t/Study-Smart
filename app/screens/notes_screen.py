import sys
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QMessageBox,
)
from app.database.notes import save_note, update_note


class NotesScreen(QWidget):
    note_updated = pyqtSignal()
    
    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id

        self.setWindowTitle("Study Smart - New Note")
        self.editing_note_id = None

        #For testing alone - QStackedWidget should resize all pages automatically next to sidebar since we're using layouts.
        self.resize(1200, 800)

        self.setup_ui()
        self.connect_buttons()
        

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                color: black;
            }

            QLineEdit {
                background-color: white;
                color: black;
                border: 1px solid gray;
                border-radius: 5px;
                padding: 5px;
            }

            QTextEdit {
                background-color: white;
                color: black;
                border: 1px solid gray;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        # Main layout for the entire Notes page.
        main_layout = QVBoxLayout()

        # Adds some empty space around the outside of the page.
        main_layout.setContentsMargins(40, 30, 40, 30)

        # Adds spacing between widgets.
        main_layout.setSpacing(15)

        # -------------------------
        # Page title
        # -------------------------
        self.page_title = QLabel("New Note")

        self.page_title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # Make the page title larger without using CSS.
        title_font = self.page_title.font()
        title_font.setPointSize(24)
        title_font.setBold(True)
        self.page_title.setFont(title_font)

        main_layout.addWidget(self.page_title)

        # Note title
        
        title_label = QLabel("Note Title")

        self.note_title_input = QLineEdit()
        self.note_title_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                border: 1px solid gray;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        self.note_title_input.textChanged.connect(self.update_title)
        self.note_title_input.setPlaceholderText(
            "Enter a title for your note..."
        )
        self.note_title_input.setMinimumHeight(40)

        # Ttitle character limit of 100
        self.note_title_input.setMaxLength(100)

        main_layout.addWidget(title_label)
        main_layout.addWidget(self.note_title_input)

        
        # Main note entry box
        notes_label = QLabel("Your Notes")

        self.notes_text_box = QTextEdit()
        self.notes_text_box.setStyleSheet("""
            QTextEdit {
                background-color: white;
                color: black;
                border: 1px solid gray;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        self.notes_text_box.setPlaceholderText(
            "Start writing your notes here..."
        )

        # QTextEdit automatically becomes scrollable once text becomes longer than the visible area.

        # This gives the note box more space than the other widgets.
        main_layout.addWidget(notes_label)
        main_layout.addWidget(self.notes_text_box, 1)

        
        # Message label
        # Later, this can display messages such as: "Note saved successfully."
        self.message_label = QLabel("")

        self.message_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        main_layout.addWidget(self.message_label)

        # Bottom buttons
        button_layout = QHBoxLayout()

        self.view_all_notes_button = QPushButton(
            "View All Notes"
        )

        self.save_notes_button = QPushButton(
            "Save Notes"
        )

        # Put View All Notes on the left.
        button_layout.addWidget(
            self.view_all_notes_button
        )

        # Invisible flexible space between the buttons.
        button_layout.addStretch()

        # Put Save Notes on the right.
        button_layout.addWidget(
            self.save_notes_button
        )

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
    def update_title(self, text):
        if text.strip() == "":
            self.page_title.setText("New Note")
        else:
            self.page_title.setText(text)

    def connect_buttons(self):
        self.save_notes_button.clicked.connect(self.handle_save_note)
    def handle_save_note(self):
        title = self.note_title_input.text().strip()

        content = (self.notes_text_box.toPlainText().strip())

        if title == "":
            QMessageBox.warning(self,"Missing Title","Please enter a title.")
            return

        if content == "":
            QMessageBox.warning(self, "Missing Content","Please enter note content.")
            return

        #For new notes
        if self.editing_note_id is None:
            success, message = save_note(self.user_id, title, content)
            if success:
                QMessageBox.information(self, "Note Saved", message)
                self.reset_note_form()

            else:
                QMessageBox.warning(self, "Save Failed", message)

        #For editing
        else:
            success = update_note(self.editing_note_id, self.user_id, title, content)

            if success:
                QMessageBox.information(self, "Note Updated", "Your note was updated successfully.")
                self.reset_note_form()
                self.note_updated.emit()
            else:
                QMessageBox.information(self, "Update Failed", "The note could not be updated.")


    def reset_note_form(self):
        self.editing_note_id = None
        self.note_title_input.clear()
        self.notes_text_box.clear()

        self.save_notes_button.setText("Save Notes")
        self.page_title.setText("New Note")
        
    def load_notes_for_editing(self, note):
        self.editing_note_id = note["id"]

        self.note_title_input.setText(note["title"])
        self.notes_text_box.setPlainText(note["content"])
        self.save_notes_button.setText("Update Note")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = NotesScreen()
    window.show()

    sys.exit(app.exec())
