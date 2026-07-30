import sys

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QLineEdit,
)

from app.database.planner_database import (
     save_plan,
     update_plan,
)


class PlannerScreen(QWidget):

    plan_updated = pyqtSignal()

    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id
        self.editing_plan_id = None

        self.setWindowTitle("Study Smart - Study Planner")

        # For standalone testing
        self.resize(1200, 800)

        self.setup_ui()
        self.connect_buttons()

    def setup_ui(self):

        self.setStyleSheet("""
            QWidget {
                background-color: rgb(240,240,240);
                color: black;
            }

            QTextEdit {
                background-color: white;
                color: black;
                border: 1px solid gray;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        # ---------------------------------
        # Main Layout
        # ---------------------------------

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            40,
            30,
            40,
            30
        )

        main_layout.setSpacing(15)

        # ---------------------------------
        # Page Title
        # ---------------------------------

        self.page_title = QLabel("New Study Plan")
        self.page_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_font = self.page_title.font()
        title_font.setPointSize(24)
        title_font.setBold(True)

        self.page_title.setFont(title_font)

        main_layout.addWidget(self.page_title)

        self.plan_name_label = QLabel("Plan Name")
        self.plan_name_input = QLineEdit()

        self.plan_name_input.setPlaceholderText(
            "Example: Math Midterm"
        )

        self.plan_name_input.setMinimumHeight(40)

        self.plan_name_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                border: 1px solid gray;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        main_layout.addWidget(self.plan_name_label)
        main_layout.addWidget(self.plan_name_input)

        # ---------------------------------
        # Planner Label
        # ---------------------------------

        planner_label = QLabel("Study Plan")

        main_layout.addWidget(planner_label)

        # ---------------------------------
        # Planner Text Box
        # ---------------------------------

        self.plan_text_box = QTextEdit()

        self.plan_text_box.setPlaceholderText(
            "Example: Study Flashcards"
            "Math Midterm\n"
            "- Read Chapter 5\n"
            "- Complete practice quiz\n"
            "- Review flashcards\n"
            "- Meet with study group Thursday"
        )

        main_layout.addWidget(
            self.plan_text_box,
            1
        )

        # ---------------------------------
        # Message Label
        # ---------------------------------

        self.message_label = QLabel("")

        self.message_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        main_layout.addWidget(
            self.message_label
        )

        # ---------------------------------
        # Buttons
        # ---------------------------------

        button_layout = QHBoxLayout()

        self.view_all_plans_button = QPushButton(
            "View All Plans"
        )

        self.save_plan_button = QPushButton(
            "Save Plan"
        )

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

        self.view_all_plans_button.setStyleSheet(
            button_style
        )

        self.save_plan_button.setStyleSheet(
            button_style
        )

        self.view_all_plans_button.setFixedSize(
            170,
            40
        )

        self.save_plan_button.setFixedSize(
            170,
            40
        )

        button_layout.addWidget(
            self.view_all_plans_button
        )

        button_layout.addStretch()

        button_layout.addWidget(
            self.save_plan_button
        )

        main_layout.addLayout(
            button_layout
        )

        self.setLayout(main_layout)

    # ---------------------------------
    # Connect Buttons
    # ---------------------------------

    def connect_buttons(self):

        self.save_plan_button.clicked.connect(
            self.handle_save_plan
        )

    # ---------------------------------
    # Save Plan
    # ---------------------------------

    def handle_save_plan(self):

        title = self.plan_name_input.text().strip()
        content = self.plan_text_box.toPlainText().strip()

        if title == "":
            self.styled_message(
            "Missing Plan Name",
            "Please enter a plan name.",
            "warning"
            )
            return
        if content == "":
            self.styled_message(
                "Missing Plan",
                "Please enter a study plan.",
                "warning"
            )
            return

        # ------------------------------------------------
        # Database code will go here
        # ------------------------------------------------

        if self.editing_plan_id is None:

            success, message = save_plan(
            self.user_id,
            title,
            content
        )

            if success:

                self.styled_message(
                    "Plan Saved",
                    message,
                    "info"
                )

                self.reset_plan_form()

                self.plan_updated.emit()

            else:

                self.styled_message(
                    "Save Failed",
                    message,
                    "warning"
                )

        else:

            success = update_plan(
                self.editing_plan_id,
                self.user_id,
                title,
                content
            )

            if success:

                self.styled_message(
                    "Plan Updated",
                    "Your study plan was updated successfully.",
                    "info"
                )

                self.reset_plan_form()

                self.plan_updated.emit()

            else:

                self.styled_message(
                    "Update Failed",
                    "Unable to update study plan.",
                    "warning"
                )

    # ---------------------------------
    # Reset Form
    # ---------------------------------

    def reset_plan_form(self):

        self.editing_plan_id = None
        self.plan_name_input.clear()
        self.plan_text_box.clear()

        self.save_plan_button.setText(
            "Save Plan"
        )

        self.page_title.setText(
            "New Study Plan"
        )

    # ---------------------------------
    # Load Existing Plan
    # ---------------------------------

    def load_plan_for_editing(self, plan):

        self.editing_plan_id = plan["id"]

        self.plan_name_input.setText(plan["title"])
        self.plan_text_box.setPlainText(plan["content"])

        self.save_plan_button.setText("Update Plan")

        self.page_title.setText("Edit Study Plan")

    # ---------------------------------
    # Styled Message Box
    # ---------------------------------

    def styled_message(
        self,
        title,
        text,
        icon="info"
    ):

        msg = QMessageBox(self)

        msg.setWindowTitle(title)

        msg.setText(text)

        if icon == "info":
            msg.setIcon(
                QMessageBox.Icon.Information
            )

        elif icon == "warning":
            msg.setIcon(
                QMessageBox.Icon.Warning
            )

        elif icon == "critical":
            msg.setIcon(
                QMessageBox.Icon.Critical
            )

        msg.setStyleSheet("""
            QWidget {
                background-color: white;
            }

            QLabel {
                color: black;
            }

            QPushButton {
                background-color: rgb(205,220,245);
                color: black;
                border: 1px solid rgb(170,185,210);
                border-radius: 8px;
                padding: 6px 14px;
                font-size: 12px;
                font-weight: bold;
                min-width: 80px;
            }

            QPushButton:hover {
                background-color: rgb(185,205,240);
            }
        """)

        msg.exec()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = PlannerScreen(user_id=1)

    window.show()

    sys.exit(app.exec())