import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout
)

from app.widgets.dashboard_button_widget import DashboardCardWidget


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("Dashboard Card Test")
    window.resize(1200, 800)

    # Central widget
    central_widget = QWidget()
    central_widget.setStyleSheet("""
    background-color: rgb(240, 240, 240);
    """)

    
    layout = QHBoxLayout(central_widget)

    layout.setContentsMargins(30, 30, 30, 30)
    layout.setSpacing(20)

    # Test one card
    card = DashboardCardWidget(
        title="placeholder",
        button_text="Placeholder"
    )

    layout.addWidget(card)

    window.setCentralWidget(central_widget)

    window.show()

    sys.exit(app.exec())