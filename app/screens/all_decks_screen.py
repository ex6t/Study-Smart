from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.database.flashcards import (
    delete_flashcard,
    get_decks,
    get_flashcards, delete_deck,
)

from app.widgets.flashcard_widget import (
    FlashcardCardWidget,
)


class AllFlashcardsScreen(QWidget):
    new_flashcard_requested = pyqtSignal()
    edit_flashcard_requested = pyqtSignal(dict)

    study_requested = pyqtSignal(object)

    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id
        self.decks = []
        self.flashcards = []
        self.selected_deck_id = None

        self.setup_ui()
        self.connect_buttons()
        self.refresh_flashcards()

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

        self.button_style = """
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

        self.page_title = QLabel("All Flashcards")

        title_font = self.page_title.font()
        title_font.setPointSize(24)
        title_font.setBold(True)

        self.page_title.setFont(title_font)

        self.study_button = QPushButton(
            "Study"
        )

        self.new_flashcard_button = QPushButton(
            "+ New Flashcard"
        )

        self.study_button.setStyleSheet(
            self.button_style
        )

        self.new_flashcard_button.setStyleSheet(
            self.button_style
        )

        heading_layout.addWidget(
            self.page_title
        )

        heading_layout.addStretch()

        heading_layout.addWidget(
            self.study_button
        )

        heading_layout.addWidget(
            self.new_flashcard_button
        )

        main_layout.addLayout(
            heading_layout
        )

        # --------------------------
        # Deck Filter
        # --------------------------

        filter_layout = QHBoxLayout()

        filter_label = QLabel("Deck:")

        self.deck_filter_combo = QComboBox()

        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.deck_filter_combo)
        filter_layout.addStretch()

        main_layout.addLayout(filter_layout)

        # --------------------------
        # Scroll Area
        # --------------------------

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
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

        self.scroll_container = QWidget()

        self.scroll_layout = QVBoxLayout(
            self.scroll_container
        )

        self.scroll_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        self.scroll_layout.setSpacing(12)

        self.scroll_area.setWidget(
            self.scroll_container
        )

        main_layout.addWidget(
            self.scroll_area,
            1
        )

    def connect_buttons(self):
        self.new_flashcard_button.clicked.connect(
            self.new_flashcard_requested.emit
        )

        self.study_button.clicked.connect(
            self.study_button_pressed
        )

        self.deck_filter_combo.currentIndexChanged.connect(
            self.deck_filter_changed
        )

    def study_button_pressed(self):
        self.study_requested.emit(self.selected_deck_id)

    def refresh_flashcards(self):
        self.decks = get_decks(self.user_id)
        self.flashcards = get_flashcards(self.user_id)

        self.load_deck_filter()
        self.display_flashcards()

    def load_deck_filter(self):
        previous_selection = self.selected_deck_id

        self.deck_filter_combo.blockSignals(True)
        self.deck_filter_combo.clear()

        self.deck_filter_combo.addItem("All Decks", None)

        for deck in self.decks:
            self.deck_filter_combo.addItem(deck["deck_name"], deck["deck_id"])

        index = self.deck_filter_combo.findData(previous_selection)
        if index != -1:
            self.deck_filter_combo.setCurrentIndex(index)
            self.selected_deck_id = previous_selection
        else:
            self.deck_filter_combo.setCurrentIndex(0)
            self.selected_deck_id = None

        self.deck_filter_combo.blockSignals(False)

    def deck_filter_changed(self):
        self.selected_deck_id = self.deck_filter_combo.currentData()
        self.display_flashcards()

    def display_flashcards(self):
        self.clear_scroll_layout()

        if not self.decks:
            empty_label = QLabel(
                "No decks yet\n\nClick 'New Flashcard' to create a deck and your first card"
            )

            empty_label.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            empty_label.setStyleSheet("""
                font-size: 16px;
                color: rgb(120,120,120);
                padding: 80px;
            """)

            self.scroll_layout.addWidget(empty_label)
            return

        decks_to_show = self.decks
        if self.selected_deck_id is not None:
            decks_to_show = [
                deck for deck in self.decks
                if deck["deck_id"] == self.selected_deck_id
            ]

        self.flashcard_cards = []

        for deck in decks_to_show:
            self.add_deck_section(deck)

        self.scroll_layout.addStretch()

    def add_deck_section(self, deck):
        deck_cards = [
            flashcard for flashcard in self.flashcards
            if flashcard["deck_id"] == deck["deck_id"]
        ]

        deck_cards.sort(key=lambda flashcard: flashcard["term"].lower())

        header_row = QHBoxLayout()

        header_label = QLabel(
            f'{deck["deck_name"]} ({len(deck_cards)})'
        )

        header_font = header_label.font()
        header_font.setPointSize(15)
        header_font.setBold(True)

        header_label.setFont(header_font)

        deck_study_button = QPushButton("Study this deck")
        deck_study_button.setStyleSheet(self.button_style)
        deck_study_button.clicked.connect(
            lambda checked=False, deck_id=deck["deck_id"]: self.study_requested.emit(deck_id)
        )

        deck_delete_button = QPushButton("Delete this deck")
        deck_delete_button.setStyleSheet(self.button_style)
        deck_delete_button.clicked.connect(
            lambda checked=False, deck_id=deck["deck_id"]: self.confirm_delete_deck(deck)
        )

        header_row.addWidget(header_label)
        header_row.addStretch()
        header_row.addWidget(deck_study_button)
        header_row.addWidget(deck_delete_button)

        self.scroll_layout.addLayout(header_row)

        if not deck_cards:
            empty_deck_label = QLabel("No flashcards in this deck yet.")

            empty_deck_label.setStyleSheet(
                "color: rgb(120,120,120); font-size: 12px; padding-left: 4px;"
            )

            self.scroll_layout.addWidget(empty_deck_label)
            return

        for flashcard in deck_cards:
            card = FlashcardCardWidget(flashcard)
            self.flashcard_cards.append(card)

            card.view_requested.connect(self.view_flashcard)
            card.edit_requested.connect(self.edit_flashcard)
            card.delete_requested.connect(self.confirm_delete_flashcard)

            self.scroll_layout.addWidget(card)

    def clear_scroll_layout(self):
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()
            else:
                # header_row is a layout, not a widget
                layout = item.layout()
                if layout is not None:
                    while layout.count():
                        sub_item = layout.takeAt(0)
                        sub_widget = sub_item.widget()
                        if sub_widget is not None:
                            sub_widget.deleteLater()

    # --------------------------------------------------
    # Actions
    # --------------------------------------------------

    def view_flashcard(self, flashcard):
        msg = QMessageBox(self)
        msg.setWindowTitle(flashcard["term"])
        msg.setText(flashcard["definition"])

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

    def edit_flashcard(self, flashcard):
        self.edit_flashcard_requested.emit(flashcard)

    def confirm_delete_flashcard(self, flashcard):
        msg = QMessageBox(self)
        msg.setWindowTitle("Delete Flashcard")
        msg.setText(
            f'Are you sure you want to delete "{flashcard["term"]}"?'
        )

        msg.setIcon(QMessageBox.Icon.Question)

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

        if msg.clickedButton() != yes_button:
            return

        deleted = delete_flashcard(
            flashcard["id"],
            self.user_id
        )

        if deleted:
            self.refresh_flashcards()

            self.styled_message(
                "Flashcard Deleted",
                "The flashcard was deleted.",
                "info"
            )
        else:
            self.styled_message(
                "Delete Failed",
                "The flashcard could not be deleted.",
                "warning"
            )

    def confirm_delete_deck(self, deck):
        msg = QMessageBox(self)
        msg.setWindowTitle("Delete Deck")
        msg.setText(
            f'Are you sure you want to delete "{deck["deck_name"]}"?'
            f'\nThis will also delete all of its associated flashcards.'
        )

        msg.setIcon(QMessageBox.Icon.Question)

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

        if msg.clickedButton() != yes_button:
            return

        success, message = delete_deck(
            self.user_id,
            deck["deck_id"]
        )

        if success:
            self.refresh_flashcards()

            self.styled_message(
                "Deck Deleted",
                message,
                "info"
            )
        else:
            self.styled_message(
                "Delete Failed",
                message,
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

    def scroll_to_flashcard(self, flashcard_id):
        for card in self.flashcard_cards:
            if card.flashcard["id"] == flashcard_id:
                self.scroll_area.ensureWidgetVisible(card)
                break