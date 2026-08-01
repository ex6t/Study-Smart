import random

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.database.flashcards import get_decks, get_flashcards


class ClickableCardFrame(QFrame):
    clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)


class StudyFlashcardsScreen(QWidget):

    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id
        self.decks = []
        self.cards = []
        self.current_index = 0
        self.showing_answer = False

        self.setup_ui()
        self.connect_buttons()

        self.refresh_decks()

    def setup_ui(self):

        self.setStyleSheet("""
            QWidget {
                background-color: rgb(240,240,240);
                color: black;
            }

            QLabel {
                color: black;
            }
        """)

        self.button_style = """
            QPushButton {
                background-color: rgb(205,220,245);
                color: black;
                border: 1px solid rgb(170,185,210);
                border-radius: 8px;
                padding: 8px 18px;
                font-size: 13px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: rgb(185,205,240);
            }

            QPushButton:pressed {
                background-color: rgb(165,190,230);
            }

            QPushButton:disabled {
                background-color: rgb(225,225,225);
                color: rgb(160,160,160);
                border: 1px solid rgb(205,205,205);
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

        self.page_title = QLabel("Study Flashcards")

        title_font = self.page_title.font()
        title_font.setPointSize(24)
        title_font.setBold(True)

        self.page_title.setFont(title_font)

        heading_layout.addWidget(self.page_title)
        heading_layout.addStretch()

        deck_label = QLabel("Deck:")
        self.deck_combo = QComboBox()

        heading_layout.addWidget(deck_label)
        heading_layout.addWidget(self.deck_combo)

        main_layout.addLayout(heading_layout)

        # --------------------------
        # Progress
        # --------------------------

        self.progress_label = QLabel("0 / 0")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_label.setStyleSheet("""
            color: rgb(90,90,90);
            font-size: 13px;
        """)

        main_layout.addWidget(self.progress_label)

        # --------------------------
        # Flip Card
        # --------------------------

        main_layout.addStretch()

        self.card_frame = ClickableCardFrame()
        self.card_frame.setFixedHeight(280)
        self.card_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid rgb(190,190,190);
                border-radius: 16px;
            }
        """)

        card_layout = QVBoxLayout(self.card_frame)
        card_layout.setContentsMargins(40, 30, 40, 30)

        self.side_label = QLabel("TERM")
        self.side_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.side_label.setStyleSheet("""
            color: rgb(140,140,140);
            font-size: 12px;
            font-weight: bold;
            letter-spacing: 1px;
        """)

        self.card_text_label = QLabel("")
        self.card_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.card_text_label.setWordWrap(True)

        card_text_font = self.card_text_label.font()
        card_text_font.setPointSize(18)
        card_text_font.setBold(True)
        self.card_text_label.setFont(card_text_font)

        self.hint_label = QLabel("Click the card to flip")
        self.hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hint_label.setStyleSheet("""
            color: rgb(160,160,160);
            font-size: 11px;
        """)

        card_layout.addWidget(self.side_label)
        card_layout.addStretch()
        card_layout.addWidget(self.card_text_label)
        card_layout.addStretch()
        card_layout.addWidget(self.hint_label)

        main_layout.addWidget(self.card_frame)

        main_layout.addStretch()

        # --------------------------
        # Navigation
        # --------------------------

        nav_layout = QHBoxLayout()

        self.previous_button = QPushButton("< Previous")
        self.flip_button = QPushButton("Flip")
        self.next_button = QPushButton("Next >")
        self.shuffle_button = QPushButton("Shuffle")

        for button in (
            self.previous_button,
            self.flip_button,
            self.next_button,
            self.shuffle_button,
        ):
            button.setStyleSheet(self.button_style)

        nav_layout.addWidget(self.previous_button)
        nav_layout.addWidget(self.flip_button)
        nav_layout.addWidget(self.next_button)
        nav_layout.addStretch()
        nav_layout.addWidget(self.shuffle_button)

        main_layout.addLayout(nav_layout)

    def connect_buttons(self):
        self.deck_combo.currentIndexChanged.connect(self.deck_changed)

        self.card_frame.clicked.connect(self.flip_card)
        self.flip_button.clicked.connect(self.flip_card)

        self.previous_button.clicked.connect(self.previous_card)
        self.next_button.clicked.connect(self.next_card)
        self.shuffle_button.clicked.connect(self.shuffle_cards)

    # --------------------------------------------------
    # Loading
    # --------------------------------------------------

    def refresh_decks(self, deck_id=None):
        # An explicit deck_id (e.g. from "Study this deck" on the list
        # screen) takes priority over whatever was previously selected.
        target_selection = deck_id if deck_id is not None else self.deck_combo.currentData()

        self.decks = get_decks(self.user_id)

        self.deck_combo.blockSignals(True)
        self.deck_combo.clear()

        for deck in self.decks:
            self.deck_combo.addItem(deck["deck_name"], deck["deck_id"])

        if not self.decks:
            self.deck_combo.blockSignals(False)
            self.cards = []
            self.update_card_display()
            return

        index = self.deck_combo.findData(target_selection)
        if index == -1:
            index = 0

        self.deck_combo.setCurrentIndex(index)
        self.deck_combo.blockSignals(False)

        self.load_cards_for_deck(self.deck_combo.currentData())

    def deck_changed(self):
        deck_id = self.deck_combo.currentData()
        self.load_cards_for_deck(deck_id)

    def load_cards_for_deck(self, deck_id):
        if deck_id is None:
            self.cards = []
        else:
            self.cards = get_flashcards(self.user_id, deck_id)

        self.current_index = 0
        self.showing_answer = False

        self.update_card_display()

    def update_card_display(self):
        has_decks = len(self.decks) > 0
        has_cards = len(self.cards) > 0

        self.previous_button.setEnabled(has_cards)
        self.next_button.setEnabled(has_cards)
        self.flip_button.setEnabled(has_cards)
        self.shuffle_button.setEnabled(has_cards)

        if not has_decks:
            self.side_label.setText("")
            self.card_text_label.setText(
                "Please create a deck"
            )
            self.hint_label.setText("")
            self.progress_label.setText("0 / 0")
            return

        if not has_cards:
            self.side_label.setText("")
            self.card_text_label.setText(
                "This deck has no flashcards yet."
            )
            self.hint_label.setText("")
            self.progress_label.setText("0 / 0")
            return

        card = self.cards[self.current_index]

        if self.showing_answer:
            self.side_label.setText("DEFINITION")
            self.card_text_label.setText(card["definition"])
        else:
            self.side_label.setText("TERM")
            self.card_text_label.setText(card["term"])

        self.hint_label.setText("Click the card to flip")

        self.progress_label.setText(
            f"{self.current_index + 1} / {len(self.cards)}"
        )

    def flip_card(self):
        if not self.cards:
            return

        self.showing_answer = not self.showing_answer
        self.update_card_display()

    def next_card(self):
        if not self.cards:
            return

        self.current_index = (self.current_index + 1) % len(self.cards)
        self.showing_answer = False
        self.update_card_display()

    def previous_card(self):
        if not self.cards:
            return

        self.current_index = (self.current_index - 1) % len(self.cards)
        self.showing_answer = False
        self.update_card_display()

    def shuffle_cards(self):
        if not self.cards:
            return

        random.shuffle(self.cards)
        self.current_index = 0
        self.showing_answer = False
        self.update_card_display()