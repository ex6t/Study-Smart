from PyQt6.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout, QStackedWidget, QApplication, QLabel, QMainWindow, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from app.screens.notes_screen import NotesScreen
from app.widgets.sidebar_widget import SidebarWidget
from app.widgets.dashboard_button_widget import DashboardCardWidget
from app.widgets.Searchbar_widget import SearchBarWidget
from app.database.database import get_user_id
from app.screens.all_notes_screen import AllNotesScreen
from app.screens.flashcards_screen import FlashcardsScreen
from app.screens.quizzes_screen import QuizzesScreen
from app.screens.planner_screen import PlannerScreen
from app.screens.all_plans_screen import AllPlansScreen
from app.database.notes import find_note_by_title
from app.database.planner_database import delete_plan, update_completed, find_plan_by_title
from app.screens.settings_screen import SettingsScreen
class Dashboard(QWidget):

    def __init__(self, username):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: rgb(240, 240, 240);
            }
        """)
        self.username = username
        self.user_id = get_user_id(username)
        self.setWindowTitle("Study Smart")
        self.resize(1200, 800)
        self.setup_ui()

        self.connect_button_presses()


    def setup_ui(self):
        #Side bar | QStackedwidget
        main_layout = QHBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        #add sidebar
        self.sidebar = SidebarWidget()

        #add stacked pages
        self.page_stack = QStackedWidget()

        #Create pages
        self.dashboard_home_page = self.create_dashboard_home_page()
        self.notes_page = NotesScreen(self.user_id)

        self.flashcards_page = FlashcardsScreen()
        self.quizzes_page = QuizzesScreen(self.user_id)
        self.planner_page = PlannerScreen(self.user_id)
        self.all_plans_page = AllPlansScreen(self.user_id)
        self.settings_page = SettingsScreen()
        self.all_notes_page = AllNotesScreen(self.user_id)

        #pages added to stack will be indexed in order starting from 0

        #Dashboard = 0
        self.page_stack.addWidget(self.dashboard_home_page)
        #Notes - 1
        self.page_stack.addWidget(self.notes_page)
        #Flashcards - 2
        self.page_stack.addWidget(self.flashcards_page)
        #Quizzes - 3
        self.page_stack.addWidget(self.quizzes_page)
        #Planner - 4
        self.page_stack.addWidget(self.planner_page)
        #Settings - 5
        self.page_stack.addWidget(self.settings_page)
        #All Notes - 6
        self.page_stack.addWidget(self.all_notes_page)
        #All Plans - 7
        self.page_stack.addWidget(self.all_plans_page)
        #start with dashboard page
        self.page_stack.setCurrentWidget(self.dashboard_home_page)

        #sidebar on left side of page
        main_layout.addWidget(self.sidebar)

        #page stack takes rest of space
        main_layout.addWidget(self.page_stack, 1)
        
        
    def create_dashboard_home_page(self):

        dashboard_page = QFrame()
        
        dashboard_page.setStyleSheet(
            "background-color: rgb(240, 240, 240);"
        )
        content_layout = QVBoxLayout(dashboard_page)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(0)

        #Welcome Label
        self.welcome_label = QLabel(f"Welcome, {self.username}!")
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.welcome_label.setFont(font)
        self.welcome_label.setStyleSheet("""color: #2d6cdf; padding-left: 15px;""") #match with front page
        #self.welcome_label.setContentsMargins(50, 0, 0, 0)

        
        # Search Bar
        self.search_bar = SearchBarWidget()
        top_bar_widget = QWidget()
        top_bar_widget.setFixedHeight(60)
        top_bar_layout = QHBoxLayout(top_bar_widget)
        top_bar_layout.setContentsMargins(0, 0, 0, 0)
        top_bar_layout.setSpacing(20)
        
        top_bar_layout.addWidget(self.welcome_label)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.search_bar)

        #Dashboard cards
        self.notes_card = DashboardCardWidget(
        title="Notes",
        button_text="Open"
        )

        self.flashcards_card = DashboardCardWidget(
            title ="Flashcards",
            button_text = "Study"
            )

        self.quizzes_card = DashboardCardWidget(
        title="Quizzes",
        button_text="Start"
        )

        self.planner_card = DashboardCardWidget(
        title="Planner",
        button_text="Open"
        )
        cards_layout = QHBoxLayout()
        cards_layout.setContentsMargins(0, 0, 0, 0)
        cards_layout.setSpacing(20)

        cards_layout.addWidget(self.notes_card, 1)
        cards_layout.addWidget(self.flashcards_card, 1)
        cards_layout.addWidget(self.quizzes_card, 1)
        cards_layout.addWidget(self.planner_card, 1)

                
        content_layout.addWidget(top_bar_widget)
        
        content_layout.addSpacing(35)
        content_layout.addLayout(cards_layout)
        content_layout.addStretch()

        return dashboard_page

    def placeholder_page(self, page_name):
        page = QWidget()
        page.setStyleSheet("""
            QWidget {
                background-color: rgb(240, 240, 240);
                color: black;
            }
        """)
        page_layout = QVBoxLayout(page)
        page_title = QLabel(page_name)

        title_font = page_title.font()
        title_font.setPointSize(24)
        title_font.setBold(True)

        page_title.setFont(title_font)

        page_layout.addWidget(page_title)
        page_layout.addStretch()

        return page
    def connect_button_presses(self):
        self.sidebar.dashboard_button.clicked.connect(self.show_dashboard_page)
        self.sidebar.notes_button.clicked.connect(self.open_all_notes)
        self.sidebar.flashcards_button.clicked.connect(self.show_flashcards_page)
        self.sidebar.quizzes_button.clicked.connect(self.show_quizzes_page)
        self.sidebar.planner_button.clicked.connect(self.open_all_plans)
        self.sidebar.settings_button.clicked.connect(self.show_settings_page)

        self.notes_card.action_button.clicked.connect(self.open_all_notes)
        self.flashcards_card.action_button.clicked.connect(self.show_flashcards_page)
        self.quizzes_card.action_button.clicked.connect(self.show_quizzes_page)
        self.planner_card.action_button.clicked.connect(self.open_all_plans)
        self.planner_page.view_all_plans_button.clicked.connect(self.open_all_plans)
        self.all_plans_page.new_plan_requested.connect(self.show_planner_page)
        self.notes_page.view_all_notes_button.clicked.connect(self.open_all_notes)
        self.all_notes_page.new_note_requested.connect(self.show_notes_page)

        self.all_notes_page.edit_note_requested.connect(self.open_edit_note)
        self.notes_page.note_updated.connect(self.open_all_notes)


        self.all_plans_page.edit_plan_requested.connect(self.open_edit_plan)
        self.all_plans_page.delete_plan_requested.connect(self.delete_plan)
        self.planner_page.plan_updated.connect(self.open_all_plans)
        self.all_plans_page.completed_changed.connect(self.update_completed)
        self.search_bar.search_requested.connect(self.search_dashboard)

    def show_dashboard_page(self):
        self.page_stack.setCurrentWidget(self.dashboard_home_page)
    def show_notes_page(self):
        self.page_stack.setCurrentWidget(self.notes_page)
    def show_flashcards_page(self):
        self.page_stack.setCurrentWidget(self.flashcards_page)
    def show_quizzes_page(self):
        self.page_stack.setCurrentWidget(self.quizzes_page)
    def show_planner_page(self):
        self.page_stack.setCurrentWidget(self.planner_page)
    def show_settings_page(self):
        self.page_stack.setCurrentWidget(self.settings_page)
    def open_all_notes(self):
        self.all_notes_page.refresh_notes()
        self.page_stack.setCurrentWidget(self.all_notes_page)
    def open_all_plans(self):
        self.all_plans_page.refresh_plans()
        self.page_stack.setCurrentWidget(self.all_plans_page)
    def open_edit_note(self, note):
        self.notes_page.load_notes_for_editing(note)
        self.page_stack.setCurrentWidget(self.notes_page)
    def open_edit_plan(self, plan):
        self.planner_page.load_plan_for_editing(plan)
        self.page_stack.setCurrentWidget(self.planner_page)
    def delete_plan(self, plan):
        success, message = delete_plan(plan["id"])
        if success:
            self.open_all_plans()
    def update_completed(self, plan, completed):
        update_completed(plan["id"],int(completed))
        self.open_all_plans()
    def search_dashboard(self, search_text):

        note = find_note_by_title(
            self.user_id,
            search_text
        )

        if note:
            self.open_all_notes()

            self.all_notes_page.scroll_to_note(
            note["id"]
            )

            return


        plan = find_plan_by_title(
            self.user_id,
            search_text
        )

        if plan:
            self.open_all_plans()

            self.all_plans_page.scroll_to_plan(plan["id"])

            return


        msg = QMessageBox(self)
        msg.setWindowTitle("Search")
        msg.setText(f'No note or planner titled "{search_text}" was found.')

        msg.setIcon(
            QMessageBox.Icon.Information
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

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("Study Smart")
    window.resize(1200, 800)

    dashboard = Dashboard()
    window.setCentralWidget(dashboard)

    window.show()

    sys.exit(app.exec())
