from PyQt6.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout, QStackedWidget, QApplication, QLabel, QMainWindow
from app.widgets.sidebar_widget import SidebarWidget
from app.widgets.dashboard_button_widget import DashboardCardWidget
from app.widgets.Searchbar_widget import SearchBarWidget
class Dashboard(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Study Smart - Dashboard")
        self.resize(1200, 800)
        self.setup_ui()


    def setup_ui(self):
        #Side bar | QStackedwidget
        main_layout = QHBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        #add sidebar
        self.sidebar = SidebarWidget()

        #add stacked pages
        self.page_stack = QStackedWidget()
        
        self.content_frame = QFrame()
        self.content_frame.setStyleSheet(
            "background-color: rgb(240, 240, 240);"
        )
        self.content_layout = QVBoxLayout(self.content_frame)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(20)

        # Search Bar
        self.search_bar = SearchBarWidget()
        top_bar_layout = QHBoxLayout()
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

        self.calendar_card = DashboardCardWidget(
        title="Calendar",
        button_text="View"
        )
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        cards_layout.addWidget(self.notes_card)
        cards_layout.addWidget(self.flashcards_card)
        cards_layout.addWidget(self.quizzes_card)
        cards_layout.addWidget(self.calendar_card)  
        
        self.content_layout.addLayout(top_bar_layout)
        self.content_layout.addSpacing(30)
        self.content_layout.addLayout(cards_layout)
        self.content_layout.addStretch()

        main_layout.addWidget(self.sidebar, 0)
        main_layout.addWidget(self.content_frame, 1)


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
