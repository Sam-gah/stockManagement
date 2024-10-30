# src/ui/addStock.py
from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox, QPushButton, QMessageBox # type: ignore
from database.db_manager import DatabaseManager

class AddStockDialog(QDialog):
    """Dialog for adding new stock items."""
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Add Stock Item")
        layout = QFormLayout()

        # Input fields
        self.name_input = QLineEdit()
        layout.addRow("Name:", self.name_input)

        self.category_input = QLineEdit()
        layout.addRow("Category:", self.category_input)

        self.location_input = QLineEdit()
        layout.addRow("Location:", self.location_input)

        self.quantity_input = QSpinBox()
        layout.addRow("Quantity:", self.quantity_input)

        self.cost_input = QDoubleSpinBox()
        self.cost_input.setPrefix("$")
        layout.addRow("Cost:", self.cost_input)

        self.min_stock_input = QSpinBox()
        layout.addRow("Min Stock:", self.min_stock_input)

        self.manufacturer_input = QLineEdit()
        layout.addRow("Manufacturer:", self.manufacturer_input)

        self.specs_input = QLineEdit()
        layout.addRow("Specifications:", self.specs_input)

        # Submit button
        submit_button = QPushButton("Add Item")
        submit_button.clicked.connect(self.submit_item)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def submit_item(self):
        # Collect data
        name = self.name_input.text()
        category = self.category_input.text()
        location = self.location_input.text()
        quantity = self.quantity_input.value()
        cost = self.cost_input.value()
        min_stock = self.min_stock_input.value()
        manufacturer = self.manufacturer_input.text()
        specs = self.specs_input.text()

        # Call the add_stock method in DatabaseManager
        success, message = self.db_manager.add_stock(
            name, category, location, quantity, cost, min_stock, manufacturer, specs
        )

        # Feedback
        if success:
            self.accept()  # Closes the dialog
        else:
            QMessageBox.warning(self, "Error", message)
