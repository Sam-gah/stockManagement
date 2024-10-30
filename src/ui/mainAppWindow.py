# src/ui/mainAppWindow.py
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget # type: ignore
from database.db_manager import DatabaseManager
from ui.dashboardPage import DashboardPage
from ui.inventoryPage import InventoryPage
from ui.reportsPage import ReportsPage
from ui.transaction_history_page import TransactionHistoryPage

class MainAppWindow(QMainWindow):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Inventory Management System")
        self.setGeometry(400, 400, 1000, 600)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout with navigation and content
        main_layout = QHBoxLayout(central_widget)

        # Navigation panel
        nav_layout = QVBoxLayout()
        dashboard_button = QPushButton("Dashboard")
        dashboard_button.clicked.connect(lambda: self.set_page(0))
        inventory_button = QPushButton("Inventory")
        inventory_button.clicked.connect(lambda: self.set_page(1))
        reports_button = QPushButton("Reports")
        reports_button.clicked.connect(lambda: self.set_page(2))
        transactions_button = QPushButton("Transactions")
        transactions_button.clicked.connect(lambda: self.set_page(3))

        nav_layout.addWidget(dashboard_button)
        nav_layout.addWidget(inventory_button)
        nav_layout.addWidget(reports_button)
        nav_layout.addWidget(transactions_button)
        main_layout.addLayout(nav_layout)

        # Stacked widget to hold pages
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(DashboardPage())
        self.stacked_widget.addWidget(InventoryPage(self.db_manager))
        self.stacked_widget.addWidget(ReportsPage(self.db_manager))
        self.stacked_widget.addWidget(TransactionHistoryPage(self.db_manager))
        main_layout.addWidget(self.stacked_widget)

    def set_page(self, index):
        """Set the current page in the stacked widget."""
        self.stacked_widget.setCurrentIndex(index)
