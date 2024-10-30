from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel # type: ignore

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome to the Dashboard"))
        # Add any other Dashboard-specific UI elements here
        self.setLayout(layout)
