from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem # type: ignore
from database.db_manager import DatabaseManager

class TransactionHistoryPage(QWidget):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Transactions table
        self.transactions_table = QTableWidget()
        layout.addWidget(self.transactions_table)
        self.setLayout(layout)
        
        self.load_transactions()

    def load_transactions(self):
        """Load transaction history into the table."""
        transactions = self.db_manager.get_transactions()  # Make sure this method exists in your DatabaseManager
        
        headers = ["ID", "Stock ID", "Type", "Quantity Change", 
                   "Previous Quantity", "New Quantity", "Timestamp"]
        self.transactions_table.setColumnCount(len(headers))
        self.transactions_table.setHorizontalHeaderLabels(headers)
        self.transactions_table.setRowCount(len(transactions))
        
        for row, transaction in enumerate(transactions):
            for column, value in enumerate(transaction):
                self.transactions_table.setItem(row, column, QTableWidgetItem(str(value)))
