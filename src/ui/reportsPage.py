from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel # type: ignore

from database.db_manager import DatabaseManager

class ReportsPage(QWidget):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db_manager = db_manager  # Store the db_manager for later use
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Reports Page"))
        # Add any other reporting-specific UI elements here
        self.setLayout(layout)
