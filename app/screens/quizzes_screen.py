import sys

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class QuizzesScreen(QWidget):
    """
    Front-end screen for building a quiz from a flashcard deck.

    The signals and helper methods are ready for future flashcard and
    quiz backend code. This file does not load or save database data.
    """

    import_deck_requested = pyqtSignal()
    quiz_start_requested = pyqtSignal(str, int, bool)
    answer_submitted = pyqtSignal(str)
    next_question_requested = pyqtSignal()

    def __init__(self, user_id=None):
        super().__init__()

        # Kept for future user-specific flashcard deck loading.
        self.user_id = user_id

        self.setWindowTitle("Study Smart - Quizzes")
        self.resize(1200, 800)

        self.setup_ui()
        self.connect_buttons()

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: rgb(240, 240, 240);
                color: black;
            }

            QLabel,
            QCheckBox {
                background: transparent;
            }

            QFrame#setupPanel,
            QFrame#quizPanel,
            QFrame#questionCard {
                background-color: white;
                border: 2px solid rgb(215, 215, 215);
                border-radius: 12px;
            }

            QComboBox,
            QSpinBox,
            QLineEdit {
                background-color: white;
                color: black;
                border: 1px solid gray;
                border-radius: 5px;
                padding: 7px;
                min-height: 24px;
            }

            QComboBox:focus,
            QSpinBox:focus,
            QLineEdit:focus {
                border: 1px solid rgb(90, 130, 200);
            }

            QPushButton {
                background-color: rgb(205, 220, 245);
                color: black;
                border: 1px solid rgb(170, 185, 210);
                border-radius: 8px;
                padding: 8px 14px;
                font-size: 12px;
                font-weight: bold;
                min-height: 24px;
            }

            QPushButton:hover {
                background-color: rgb(185, 205, 240);
            }

            QPushButton:pressed {
                background-color: rgb(165, 190, 230);
            }

            QPushButton:disabled {
                background-color: rgb(225, 225, 225);
                color: rgb(135, 135, 135);
                border: 1px solid rgb(200, 200, 200);
            }

            QProgressBar {
                background-color: rgb(235, 235, 235);
                border: 1px solid rgb(200, 200, 200);
                border-radius: 6px;
                min-height: 12px;
                max-height: 12px;
                text-align: center;
            }

            QProgressBar::chunk {
                background-color: rgb(165, 190, 230);
                border-radius: 5px;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(15)

        # Page heading
        self.page_title = QLabel("Quizzes")
        self.page_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_font = self.page_title.font()
        title_font.setPointSize(24)
        title_font.setBold(True)
        self.page_title.setFont(title_font)

        self.page_subtitle = QLabel(
            "Create a typed-answer quiz from one of your flashcard decks."
        )
        self.page_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_subtitle.setStyleSheet(
            "color: rgb(90, 90, 90); font-size: 13px;"
        )

        main_layout.addWidget(self.page_title)
        main_layout.addWidget(self.page_subtitle)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        self.setup_panel = self.create_setup_panel()
        self.quiz_panel = self.create_quiz_panel()

        content_layout.addWidget(self.setup_panel)
        content_layout.addWidget(self.quiz_panel, 1)

        main_layout.addLayout(content_layout, 1)

    def create_setup_panel(self):
        panel = QFrame()
        panel.setObjectName("setupPanel")
        panel.setMinimumWidth(260)
        panel.setMaximumWidth(310)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        setup_title = QLabel("Quiz Setup")
        setup_title_font = setup_title.font()
        setup_title_font.setPointSize(18)
        setup_title_font.setBold(True)
        setup_title.setFont(setup_title_font)

        setup_description = QLabel(
            "Choose an existing flashcard deck or import one "
            "before starting your quiz."
        )
        setup_description.setWordWrap(True)
        setup_description.setStyleSheet(
            "color: rgb(90, 90, 90);"
        )

        deck_label = QLabel("Flashcard Deck")
        deck_label.setStyleSheet("font-weight: bold;")

        self.deck_selector = QComboBox()
        self.deck_selector.addItem("Select a flashcard deck...")

        self.import_deck_button = QPushButton(
            "Import Flashcard Deck"
        )

        deck_help = QLabel(
            "Imported and saved decks will appear in the list above."
        )
        deck_help.setWordWrap(True)
        deck_help.setStyleSheet(
            "color: rgb(110, 110, 110); font-size: 11px;"
        )

        question_count_label = QLabel("Number of Questions")
        question_count_label.setStyleSheet("font-weight: bold;")

        self.question_count_input = QSpinBox()
        self.question_count_input.setRange(1, 100)
        self.question_count_input.setValue(10)
        self.question_count_input.setSuffix(" questions")

        self.shuffle_questions_box = QCheckBox(
            "Shuffle question order"
        )
        self.shuffle_questions_box.setChecked(True)

        self.start_quiz_button = QPushButton("Start Quiz")
        self.start_quiz_button.setEnabled(False)

        layout.addWidget(setup_title)
        layout.addWidget(setup_description)
        layout.addSpacing(8)
        layout.addWidget(deck_label)
        layout.addWidget(self.deck_selector)
        layout.addWidget(self.import_deck_button)
        layout.addWidget(deck_help)
        layout.addSpacing(8)
        layout.addWidget(question_count_label)
        layout.addWidget(self.question_count_input)
        layout.addWidget(self.shuffle_questions_box)
        layout.addStretch()
        layout.addWidget(self.start_quiz_button)

        return panel

    def create_quiz_panel(self):
        panel = QFrame()
        panel.setObjectName("quizPanel")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        progress_layout = QHBoxLayout()

        self.progress_label = QLabel("Question Preview")
        progress_font = self.progress_label.font()
        progress_font.setPointSize(16)
        progress_font.setBold(True)
        self.progress_label.setFont(progress_font)

        self.score_label = QLabel("Score: 0")
        self.score_label.setStyleSheet(
            "color: rgb(90, 90, 90); font-weight: bold;"
        )

        progress_layout.addWidget(self.progress_label)
        progress_layout.addStretch()
        progress_layout.addWidget(self.score_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 10)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)

        question_heading = QLabel("Flashcard Question")
        question_heading.setStyleSheet("font-weight: bold;")

        self.question_card = QFrame()
        self.question_card.setObjectName("questionCard")
        self.question_card.setMinimumHeight(150)

        question_layout = QVBoxLayout(self.question_card)
        question_layout.setContentsMargins(20, 20, 20, 20)

        self.question_text = QLabel(
            "Select a flashcard deck and start a quiz. "
            "The question side of each flashcard will appear here."
        )
        self.question_text.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.question_text.setWordWrap(True)
        self.question_text.setStyleSheet(
            "background: transparent; border: none; font-size: 17px;"
        )

        question_layout.addStretch()
        question_layout.addWidget(self.question_text)
        question_layout.addStretch()

        answer_label = QLabel("Your Answer")
        answer_label.setStyleSheet("font-weight: bold;")

        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText(
            "Type the flashcard answer here..."
        )
        self.answer_input.setReadOnly(True)

        self.feedback_label = QLabel(
            "Answer feedback will appear here."
        )
        self.feedback_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.feedback_label.setWordWrap(True)
        self.feedback_label.setStyleSheet(
            "color: rgb(110, 110, 110); min-height: 32px;"
        )

        button_layout = QHBoxLayout()

        self.submit_answer_button = QPushButton(
            "Submit Answer"
        )
        self.submit_answer_button.setEnabled(False)

        self.next_question_button = QPushButton(
            "Next Question"
        )
        self.next_question_button.setEnabled(False)

        button_layout.addWidget(self.submit_answer_button)
        button_layout.addStretch()
        button_layout.addWidget(self.next_question_button)

        layout.addLayout(progress_layout)
        layout.addWidget(self.progress_bar)
        layout.addSpacing(5)
        layout.addWidget(question_heading)
        layout.addWidget(self.question_card, 1)
        layout.addWidget(answer_label)
        layout.addWidget(self.answer_input)
        layout.addWidget(self.feedback_label)
        layout.addLayout(button_layout)

        return panel

    def connect_buttons(self):
        self.deck_selector.currentIndexChanged.connect(
            self.update_start_button
        )

        self.import_deck_button.clicked.connect(
            lambda: self.import_deck_requested.emit()
        )

        self.start_quiz_button.clicked.connect(
            self.request_quiz_start
        )

        self.answer_input.returnPressed.connect(
            self.submit_current_answer
        )

        self.submit_answer_button.clicked.connect(
            self.submit_current_answer
        )

        self.next_question_button.clicked.connect(
            lambda: self.next_question_requested.emit()
        )

    def update_start_button(self):
        deck_is_selected = self.deck_selector.currentIndex() > 0
        self.start_quiz_button.setEnabled(deck_is_selected)

    def request_quiz_start(self):
        if self.deck_selector.currentIndex() <= 0:
            return

        self.quiz_start_requested.emit(
            self.deck_selector.currentText(),
            self.question_count_input.value(),
            self.shuffle_questions_box.isChecked(),
        )

    def submit_current_answer(self):
        answer = self.answer_input.text().strip()

        if answer == "":
            self.feedback_label.setText(
                "Please type an answer before submitting."
            )
            self.feedback_label.setStyleSheet(
                "color: rgb(160, 90, 35); min-height: 32px;"
            )
            return

        self.answer_submitted.emit(answer)

    # The methods below can be called by future backend code.
    def set_flashcard_decks(self, deck_names):
        self.deck_selector.blockSignals(True)
        self.deck_selector.clear()
        self.deck_selector.addItem("Select a flashcard deck...")
        self.deck_selector.addItems(deck_names)
        self.deck_selector.setCurrentIndex(0)
        self.deck_selector.blockSignals(False)

        self.update_start_button()

    def show_question(self, question, current_number, total):
        self.progress_label.setText(
            f"Question {current_number} of {total}"
        )
        self.progress_bar.setRange(0, total)
        self.progress_bar.setValue(current_number)
        self.question_text.setText(question)

        self.answer_input.clear()
        self.answer_input.setReadOnly(False)
        self.answer_input.setFocus()

        self.feedback_label.setText(
            "Type your answer, then select Submit Answer."
        )
        self.feedback_label.setStyleSheet(
            "color: rgb(110, 110, 110); min-height: 32px;"
        )

        self.submit_answer_button.setEnabled(True)
        self.next_question_button.setEnabled(False)

    def show_answer_feedback(self, message, is_correct):
        if is_correct:
            color = "rgb(45, 125, 70)"
        else:
            color = "rgb(180, 65, 65)"

        self.feedback_label.setText(message)
        self.feedback_label.setStyleSheet(
            f"color: {color}; font-weight: bold; min-height: 32px;"
        )

        self.answer_input.setReadOnly(True)
        self.submit_answer_button.setEnabled(False)
        self.next_question_button.setEnabled(True)

    def update_score(self, score):
        self.score_label.setText(f"Score: {score}")

    def show_quiz_results(self, score, total):
        self.progress_label.setText("Quiz Complete")
        self.progress_bar.setRange(0, total)
        self.progress_bar.setValue(total)
        self.question_text.setText(
            f"You answered {score} out of {total} questions correctly."
        )

        self.answer_input.clear()
        self.answer_input.setReadOnly(True)
        self.feedback_label.setText(
            "Choose a deck to start another quiz."
        )
        self.feedback_label.setStyleSheet(
            "color: rgb(45, 125, 70); font-weight: bold; "
            "min-height: 32px;"
        )

        self.submit_answer_button.setEnabled(False)
        self.next_question_button.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QuizzesScreen()
    window.set_flashcard_decks(
        [
            "Biology Chapter 1",
            "Python Vocabulary",
        ]
    )
    window.show()

    sys.exit(app.exec())
