from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QHBoxLayout, QPushButton ,QDialog # type: ignore
from ui.addStock import AddStockDialog # type: ignore
from database.db_manager import DatabaseManager

class InventoryPage(QWidget):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search for items...")
        search_bar.textChanged.connect(self.search_items)
        layout.addWidget(search_bar)

        self.stock_table = QTableWidget()
        layout.addWidget(self.stock_table)

        button_layout = QHBoxLayout()
        add_button = QPushButton("Add Item")
        add_button.clicked.connect(self.add_stock_item)
        button_layout.addWidget(add_button)

        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.load_inventory)
        button_layout.addWidget(refresh_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.load_inventory()

    def load_inventory(self):
        """Load all items into the inventory table."""
        stock_items = self.db_manager.get_stock()

        self.stock_table.clear()
        headers = ["ID", "Name", "Category", "Location", "Quantity", "Cost", "Min Stock", "Manufacturer", "Specs", "Created At", "Updated At"]
        self.stock_table.setColumnCount(len(headers))
        self.stock_table.setHorizontalHeaderLabels(headers)
        self.stock_table.setRowCount(len(stock_items))

        for row, item in enumerate(stock_items):
            for column, value in enumerate(item):
                self.stock_table.setItem(row, column, QTableWidgetItem(str(value)))

    def add_stock_item(self):
        """Open dialog to add a new stock item."""
        dialog = AddStockDialog(self.db_manager)
        if dialog.exec_() == QDialog.Accepted:
            self.load_inventory()

    def search_items(self, search_term):
        """Search items based on a term."""
        stock_items = self.db_manager.get_stock(search_term)
        self.stock_table.setRowCount(len(stock_items))

        for row, item in enumerate(stock_items):
            for column, value in enumerate(item):
                self.stock_table.setItem(row, column, QTableWidgetItem(str(value)))
