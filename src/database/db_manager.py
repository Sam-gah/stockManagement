import sqlite3
from typing import List, Optional, Tuple

class DatabaseManager:
    def __init__(self, db_path: str = "stock.db"):
        """Initialize database connection."""
        self.db_path = db_path
        self._create_tables()
    
    def _create_tables(self) -> None:
        """Create necessary tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create stock table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stock (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    location TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    cost REAL NOT NULL,
                    min_stock INTEGER NOT NULL,
                    manufacturer TEXT,
                    specs TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create transactions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    stock_id INTEGER,
                    transaction_type TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    previous_quantity INTEGER NOT NULL,
                    new_quantity INTEGER NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (stock_id) REFERENCES stock (id)
                )
            """)
            
            conn.commit()

    def add_stock(self, name: str, category: str, location: str, 
              quantity: int, cost: float, min_stock: int,
              manufacturer: Optional[str] = None, specs: Optional[str] = None) -> Tuple[bool, str]:

        """Add new stock item."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO stock (name, category, location, quantity, cost, 
                                     min_stock, manufacturer, specs)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (name, category, location, quantity, cost, 
                      min_stock, specs))
                 # Check if all parameters are provided
                if None in [name, category, location, quantity, cost, min_stock]:
                    return False, "All fields are required"

                print(f"Inserting stock: {name}, {category}, {location}, {quantity}, {cost}, {min_stock}, {manufacturer}, {specs}")
                # Log transaction
                stock_id = cursor.lastrowid
                cursor.execute("""
                    INSERT INTO transactions (stock_id, transaction_type, 
                                           quantity, previous_quantity, new_quantity)
                    VALUES (?, 'ADD', ?, ?)
                """, (stock_id, quantity, quantity))
                
                conn.commit()
                return True, "Stock added successfully"
        except sqlite3.Error as e:
            return False, f"Error adding stock: {str(e)}"
        print(f"Inserting stock: {name}, {category}, {location}, {quantity}, {cost}, {min_stock}, {manufacturer}, {specs}")


    def update_quantity(self, stock_id: int, quantity_change: int) -> Tuple[bool, str]:
        """Update stock quantity."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get current quantity
                cursor.execute("SELECT quantity FROM stock WHERE id = ?", (stock_id,))
                current_quantity = cursor.fetchone()[0]
                new_quantity = current_quantity + quantity_change
                
                if new_quantity < 0:
                    return False, "Insufficient stock"
                
                # Update stock
                cursor.execute("""
                    UPDATE stock 
                    SET quantity = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (new_quantity, stock_id))
                
                # Log transaction
                cursor.execute("""
                    INSERT INTO transactions (stock_id, transaction_type, 
                                           quantity, previous_quantity, new_quantity)
                    VALUES (?, ?, ?, ?, ?)
                """, (stock_id, 'UPDATE', quantity_change, 
                      current_quantity, new_quantity))
                
                conn.commit()
                return True, "Quantity updated successfully"
        except sqlite3.Error as e:
            return False, f"Error updating quantity: {str(e)}"
    
    def get_stock(self, search_term: str = None) -> List[Tuple]:
        """Get stock items, optionally filtered by search term."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if search_term:
                    cursor.execute("""
                        SELECT * FROM stock 
                        WHERE name LIKE ? OR category LIKE ? OR location LIKE ?
                    """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
                else:
                    cursor.execute("SELECT * FROM stock")
                
                return cursor.fetchall()
        except sqlite3.Error:
            return []

    def get_low_stock_items(self) -> List[Tuple]:
        """Get items where quantity is below min_stock."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM stock 
                    WHERE quantity <= min_stock
                """)
                return cursor.fetchall()
        except sqlite3.Error:
            return []

    def get_transactions(self) -> List[Tuple]:
        """Fetch transaction history from the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, stock_id, transaction_type, quantity, 
                           previous_quantity, new_quantity, timestamp 
                    FROM transactions
                    ORDER BY timestamp DESC
                """)
                return cursor.fetchall()
        except sqlite3.Error:
            return []
